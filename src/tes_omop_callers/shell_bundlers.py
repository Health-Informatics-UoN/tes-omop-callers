from typing import Any, Protocol

from .base import Executor, OMOPScriptTask, TaskBundler
from .cohort_clean_up import CleanUpCohortTable


class ShellBundler(TaskBundler, Protocol):
    """
    Protocol for a task bundler that renders tasks as a single shell command
    """

    image: str
    tasks: list[OMOPScriptTask]

    def render_shell(self) -> str:
        shell_string = self.tasks[0].render()

        for task in self.tasks[1:]:
            if task.must_run:
                shell_string += f"; {task.render()}"
            else:
                shell_string += f" && {task.render()}"

        return shell_string

    def render_executor(self) -> dict[str, Any]:
        executor = Executor(
            image=self.image, command=["bin/sh", "-c", self.render_shell()]
        )
        return executor.model_dump()


class CohortShellBundler(ShellBundler):
    """
    A ShellBundler for a list of tasks, some of which create cohort tables that need to be cleaned up at the end.
    This tracks the cohort tables created and creates a task at the end to drop those tables.
    """

    def __init__(self, image: str, tasks: list[OMOPScriptTask]):
        self.image = image
        self.tasks = tasks
        cohorts: set[str] = set()
        cohorts.update(
            *[set(task.cohorts) for task in tasks if task.cohorts is not None]
        )
        self.cohorts = list(cohorts)
        if len(self.cohorts) > 0:
            self.tasks.append(CleanUpCohortTable(cohort_table_names=self.cohorts))
