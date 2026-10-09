from tes_omop_callers.define_cohorts import DefineConceptCohort

def test_define_concept_cohort_defaults():
    task = DefineConceptCohort("test_cohort", concept_set={"diabetes": [201254, 201826]})
    assert task.render() == (
            "Rscript "
            "inst/scripts/defineConceptCohortSet.R test_cohort "
            "--conceptSet='{\"diabetes\": [201254, 201826]}' "
            "--end=observation_period_end_date "
            "--requiredObservation='[0,0]'"
            )
