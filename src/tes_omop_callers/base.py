from typing import Any, Protocol

from pydantic import BaseModel


class ScriptArg(Protocol):
    """
    Protocol for describing an argument of a command-line script
    """
    argument_name: str

    def render(self) -> str: ...


class OMOPScriptTask(Protocol):
    """
    Protocol for a script called from the command-line
    """
    script_path: str
    arguments: list[ScriptArg]
    cohorts: list[str] | None = None
    must_run: bool = False

    def render(self) -> str:
        return ""


class Executor(BaseModel):
    """
    Model for an Executor attribute of a TES message.
    Calling Executor.model_dump_json() will make a compliant description, unless you put nonsense in the attributes!

    Attributes
    ----------
    image: str
        The url for a container image used for the task
    command: list[str]
        The commands passed to the container
    """
    image: str
    command: list[str]


class TaskBundler(Protocol):
    """
    Protocol for bundling tasks together in a single Executor

    Attributes
    ----------
    image: str
        The url for a container image used for the task
    tasks: list[OMOPScriptTask]
        A list of OMOPScriptTask which can render commands for the container
    """
    image: str
    tasks: list[OMOPScriptTask]

    def render_executor(self) -> dict[str, Any]: ...
