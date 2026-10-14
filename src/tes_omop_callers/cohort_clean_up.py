from tes_omop_callers.base import OMOPScriptTask
from tes_omop_callers.script_args import PositionalStrings


class CleanUpCohortTable(OMOPScriptTask):
    """
    A specification for the R script arguments used to clean up the temporary tables used in an analysis
    """

    def __init__(
        self, cohort_table_names: list[str], script_path: str | None = None
    ) -> None:
        """
        Parameters
        ----------
        cohort_table_names: list[str]
            The names of cohort tables to be dropped
        script_path: str | None
            The path of the cleanup script. If None, defaults to the OMOP R tools path
        """
        if script_path is None:
            self.script_path = "inst/scripts/cleanUpCohortTables.R"
        else:
            self.script_path = script_path
        self.arguments = [PositionalStrings(value=cohort_table_names)]
        self.must_run = True

    def render(self) -> str:
        return f"Rscript {self.script_path} {self.arguments[0].render()}"
