from typing import Any, Protocol

from pydantic import BaseModel


class ScriptArg(Protocol):
    argument_name: str

    def render(self) -> str: ...


class OMOPScriptTask(Protocol):
    script_path: str
    arguments: list[ScriptArg]
    cohorts: list[str] | None = None
    must_run: bool = False

    def render(self) -> str:
        return ""


class Executor(BaseModel):
    image: str
    command: list[str]


class TaskBundler(Protocol):
    image: str
    tasks: list[OMOPScriptTask]

    def render_executor(self) -> dict[str, Any]: ...
