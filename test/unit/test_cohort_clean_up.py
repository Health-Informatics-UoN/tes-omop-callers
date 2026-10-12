from tes_omop_callers.cohort_clean_up import CleanUpCohortTable


def test_clean_up():
    task = CleanUpCohortTable(["test_cohort_1", "test_cohort_2"])
    assert (
        task.render()
        == "Rscript inst/scripts/cleanUpCohortTables.R test_cohort_1 test_cohort_2"
    )
