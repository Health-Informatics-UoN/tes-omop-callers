from typing import Any, Protocol

from pydantic import BaseModel


class ScriptArg(Protocol):
    argument_name: str

    def render(self) -> str: ...

    def marimo_widget(self) -> Any: ...


# class OMOPScriptTask(BaseModel):
#     script_path: str
#     arguments: list[ScriptArg]
#
#     def render(self) -> str: return ""


class Executor(BaseModel):
    image: str
    command: list[str]

# class TaskBundler(Protocol):
#     image: str
#     tasks: list[OMOPScriptTask]
#
#     def render_executor(self) -> dict[str, Any]: ...


# class ShellBundler(BaseModel, TaskBundler):
#     image: str
#
#     def render_shell(self):
#         return " ".join([task.render() for task in self.tasks])
#
#     def render_executor(self) -> dict[str, Any]:
#         executor = Executor(
#             image=self.image, command=["bin/sh", "-c", self.render_shell()]
#         )
#         return executor.model_dump()
