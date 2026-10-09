from tes_omop_callers.base import OMOPScriptTask
from tes_omop_callers.script_args import PositionalStrings


class CleanUpCohortTable(OMOPScriptTask):
    def __init__(
            self,
            cohort_table_names: list[str],
            script_path: str | None = None
            ) -> None:
        if script_path is None:
            self.script_path = "inst/scripts/cleanUpCohortTables.R"
        else:
            self.script_path = script_path
        self.arguments = [PositionalStrings(value=cohort_table_names)]
        

    def render(self) -> str:
        return f"Rscript {self.script_path} {self.arguments[0].render()}"
