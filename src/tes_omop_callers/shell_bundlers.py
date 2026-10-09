from typing import Any, Protocol

from .base import Executor, OMOPScriptTask, TaskBundler
from .cohort_clean_up import CleanUpCohortTable


class ShellBundler(TaskBundler, Protocol):
    image: str
    tasks: list[OMOPScriptTask]

    def render_shell(self) -> str:
        shell_string = self.tasks[0].render()
        
        for task in self.tasks[1:]:
            if task.must_run:
                shell_string += f"; {task.render()}"
            else:
                shell_string += f"&& {task.render()}"

        return shell_string

    def render_executor(self) -> dict[str, Any]:
        executor = Executor(
            image=self.image, command=["bin/sh", "-c", self.render_shell()]
        )
        return executor.model_dump()


class CohortShellBundler(ShellBundler):
    def init(self, image: str, tasks: list[OMOPScriptTask]):
        self.image = image
        self.tasks = tasks
        cohorts: set[str] = set()
        for task in tasks:
            if task.cohorts is not None:
                cohorts.union(set(task.cohorts))
        if len(cohorts) > 0:
            self.tasks.append(CleanUpCohortTable(cohort_table_names=list(cohorts)))
