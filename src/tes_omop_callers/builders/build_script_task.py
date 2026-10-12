from typing import Any

from pydantic import BaseModel, create_model
from ..base import OMOPScriptTask
from ..script_args import BaseArg


class ArgDescription(BaseModel):
    python_arg_name: str
    argument_name: str
    arg_class: type[BaseArg]
    default: Any | None = None

    def build_arg(self) -> type[BaseArg]:
        return create_model(self.argument_name, __base__=(self.arg_class))


class ConcreteScriptTask(OMOPScriptTask):
    def render(self) -> str:
        rendered_args = [arg.render() for arg in self.arguments]
        rendered_args = " ".join([arg for arg in rendered_args if arg != ""])
        return f"Rscript {self.script_path} {rendered_args}"


def build_omop_script_task(
    name: str,
    script_path: str,
    argument_descriptions: list[ArgDescription],
    must_run: bool,
    docstring: str | None = None,
):
    def new_init(self, **kwargs) -> None:
        self.script_path = script_path
        self.arguments = []
        for arg in argument_descriptions:
            val = kwargs.get(arg.python_arg_name, arg.default)
            self.arguments.append(
                arg.build_arg()(argument_name=arg.argument_name, value=val)
            )
        for k in kwargs:
            arg = next(
                (desc for desc in argument_descriptions if desc.python_arg_name == k),
                None,
            )
            if arg is None:
                raise TypeError(f"Argument {k} is not valid for {name}")
        self.must_run = must_run

    return type(
        name, (ConcreteScriptTask,), {"__init__": new_init, "__doc__": docstring}
    )
