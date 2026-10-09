from typing import Any

from .base import Executor, OMOPScriptTask, TaskBundler
from .cohort_clean_up import CleanUpCohortTable


class ShellBundler(TaskBundler):
    image: str
    tasks: list[OMOPScriptTask]

    def render_shell(self):
        return " ".join([task.render() for task in self.tasks])

    def render_executor(self) -> dict[str, Any]:
        executor = Executor(
            image=self.image, command=["bin/sh", "-c", self.render_shell()]
        )
        return executor.model_dump()


class CohortShellBundler(ShellBundler):
    def init(self, image: str, tasks: list[OMOPScriptTask]):
        self.image = image
        self.tasks = tasks
        cohorts = []
        for task in tasks:
            if task.cohorts is not None:
                cohorts = [*cohorts, *task.cohorts]
        if len(cohorts) > 0:
            self.tasks.append(CleanUpCohortTable(cohort_table_names=cohorts))
