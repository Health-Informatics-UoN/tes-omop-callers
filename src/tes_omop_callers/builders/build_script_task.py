from typing import Any

from pydantic import BaseModel, create_model
from ..base import OMOPScriptTask
from ..script_args import BaseArg


class ArgDescription(BaseModel):
    """
    A description of an argument used to build arguments for building a task.

    Attributes
    ----------
    python_arg_name: str
        The name of the argument to use in python. This will become one of the init parameters of a task built with the ArgDescription
    argument_name: str
        The command-line argument name rendered when the task is generated
    arg_class: type[BaseArg]
        The class of argument used to render this argument in the command-line
    default: Any | None = None
        A default value for the argument
    """

    python_arg_name: str
    argument_name: str
    arg_class: type[BaseArg]
    default: Any | None = None
    description: str | None = None

    def build_arg(self) -> type[BaseArg]:
        return create_model(self.argument_name, __base__=(self.arg_class))

    def build_docstring(self) -> str:
        return_type = self.arg_class.model_fields["value"].annotation
        return_type_str = str(return_type)
        return_type_repr = (
            return_type_str[8:-2] if "class" in return_type_str else return_type_str
        )
        if self.default is None:
            if "None" in return_type_str:
                return_representation = f"{return_type_repr} = None"
            else:
                return_representation = f"{return_type_repr}"
        else:
            return_representation = f"{return_type_repr} = {self.default}"
        return f"{self.python_arg_name}: {return_representation}\n\t{self.description}"


class ConcreteScriptTask(OMOPScriptTask):
    """
    A barebones concrete implementation of the OMOPScriptTask protocol used for generating tasks
    """

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
) -> type[OMOPScriptTask]:
    """
    Builds a new class for a task, using the list of ArgDescription to set kwargs.

    Parameters
    ----------
    name: str
        A name for the class. This will be how python reports the class; it will be `abc.<name>` in any stack traces, etc.
    script_path: str
        The path of the script used for the task in the destination
    argument_descriptions: list[ArgDescription]
        A list of ArgDescription which describe the command-line arguments, which become the init args of the generated class
    must_run: bool
        Whether the task must run if bundled with other scripts
    docstring: str | None = None
        An optional docstring for the generated class

    Returns
    -------
    type[OMOPScriptTask]
        A class for the task, instances of which will render commands as the arguments are specified
    """

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
