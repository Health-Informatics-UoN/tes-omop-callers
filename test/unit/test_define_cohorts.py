import pytest
from tes_omop_callers.define_cohorts import DefineConceptCohort

@pytest.fixture
def single_cohort_task():
    return DefineConceptCohort("test_cohort", concept_set={"diabetes": [201254, 201826]})

def test_cohorts_surfaced(single_cohort_task):
    assert single_cohort_task.cohorts == ["test_cohort"]

def test_define_concept_cohort_defaults(single_cohort_task):
    assert single_cohort_task.render() == (
            "Rscript "
            "inst/scripts/defineConceptCohortSet.R test_cohort "
            "--conceptSet='{\"diabetes\": [201254, 201826]}' "
            "--end=observation_period_end_date "
            "--requiredObservation='[0,0]'"
            )
