from tes_omop_callers.cohort_survival.estimate_competing_event_survival import args
from tes_omop_callers.builders.docstring import build_docstring


def test_docstring_correct():
    description = "Estimate time-to-event probabilities for one or more target cohorts when an event of interest can be precluded by a competing outcome."
    return_description = "An OMOPScriptTask for estimating competing event survival"
    assert (
        build_docstring(description, args, return_description)
        == """Estimate time-to-event probabilities for one or more target cohorts when an event of interest can be precluded by a competing outcome.

Parameters
----------
target_cohort_table: str
	Name of the cohort table containing the target cohorts. The table must be present in cdm and contain standard OMOP cohort columns.
outcome_cohort_table: str
	Name of the cohort table containing the outcome of interest.
target_cohort_id: list[str] | list[int] | None = None
	Target cohorts to include. It can either be a cohort_definition_id value or a cohort_name. Multiple ids are allowed. If omitted, all non-empty cohorts in targetCohortTable are used.
outcome_cohort_id: list[str] | list[int] | None = None
	Outcome cohorts to include. It can either be a cohort_definition_id value or a cohort_name. Multiple ids are allowed. If omitted, all outcome cohorts in outcomeCohortTable are used.
outcome_date_variable: str = cohort_start_date
	Variable containing the outcome event date. This is usually "cohort_start_date", but another date column in the outcome cohort can be used.
outcome_washout: int = inf
	Number of days before target cohort entry used to exclude people with a prior outcome. Inf excludes people with any prior outcome before index; 0 applies no pre-index washout.
censor_on_cohort_exit: bool = False
\tIf active, an individual\'s follow up will be censored at their target cohort exit date.
censor_on_date: datetime.date | str | None = None
	If specified, an individual\'s follow up will be censored at the given date. This can be a scalar Date or the name of a date column in the target cohort table.
weight: str | None = None
	If specified, the name of a numeric column in the target cohort table containing observation weights.
followup_days: int = inf
	Number of days to follow up individuals (lower bound 1, upper bound Inf). Follow-up is censored at this value.
strata: list[str | list[str]] | None = None
	A list of target cohort column names to stratify by. Each element can be one column name or a character vector of column names for a combined stratum, for example list("sex", c("age_group", "sex")).
event_gap: int = 30
	Days between time points for which to report survival events, which are grouped into the specified intervals.
estimate_gap: int = 1
	Days between time points for which to report survival estimates. First day will be day zero with risk estimates provided for times up to the end of follow-up, with a gap in days equivalent to estimateGap.
restricted_mean_followup: int | None = None
	Number of days of follow-up to use when calculating restricted mean summaries. See Details.
minimum_survival_days: int = 1
	Minimum number of days required for the main cohort to contribute to the analysis.
competing_outcome_cohort_table: str
	Name of the cohort table containing the competing outcome.
competing_outcome_cohort_id: list[str] | list[int] | None = None
	Competing outcome cohorts to include. It can either be a cohort_definition_id value or a cohort_name. Multiple ids are allowed. If omitted, all competing outcome cohorts in competingOutcomeCohortTable are used.
competing_outcome_date_variable: str = cohort_start_date
	Variable containing the competing outcome event date.
competing_outcome_washout: int = inf
	Number of days before target cohort entry used to exclude people with a prior competing outcome. Inf excludes people with any prior competing outcome before index; 0 applies no pre-index washout.
output_path: str = outputs/competing-event-survival.csv
	Path for saving the survival table as a csv

Returns
-------
An OMOPScriptTask for estimating competing event survival
"""
    )
