from pydantic import BaseModel


class CleanUpCohortTable(BaseModel):
    script_path: str = "inst/scripts/cleanUpCohortTables.R"
    cohort_table_name: str

    def render(self) -> str:
        return f"Rscript {self.script_path} {self.cohort_table_name}"
