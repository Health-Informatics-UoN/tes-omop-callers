from datetime import date
from math import inf
from typing import Annotated

from pydantic import Field

from ..builders.build_script_task import ArgDescription
from ..script_args import Flag, JsonSerialisedArg, SimpleArg

# I know this could be a proper registry, but I'm a big fan of KISS, and I am very stupid, so it will be very simple.
cohort_survival_common_args = [
    ArgDescription(
        python_arg_name="target_cohort_table",
        argument_name="targetCohortTable",
        arg_class=SimpleArg[str],
        description="Name of the cohort table containing the target cohorts. The table must be present in cdm and contain standard OMOP cohort columns.",
    ),
    ArgDescription(
        python_arg_name="outcome_cohort_table",
        argument_name="outcomeCohortTable",
        arg_class=SimpleArg[str],
        description="Name of the cohort table containing the outcome of interest.",
    ),
    ArgDescription(
        python_arg_name="target_cohort_id",
        argument_name="targetCohortId",
        arg_class=JsonSerialisedArg[list[str] | list[int] | None],
        description="Target cohorts to include. It can either be a cohort_definition_id value or a cohort_name. Multiple ids are allowed. If omitted, all non-empty cohorts in targetCohortTable are used.",
    ),
    ArgDescription(
        python_arg_name="outcome_cohort_id",
        argument_name="outcomeCohortId",
        arg_class=JsonSerialisedArg[list[str] | list[int] | None],
        description="Outcome cohorts to include. It can either be a cohort_definition_id value or a cohort_name. Multiple ids are allowed. If omitted, all outcome cohorts in outcomeCohortTable are used.",
    ),
    ArgDescription(
        python_arg_name="outcome_date_variable",
        argument_name="outcomeDateVariable",
        arg_class=SimpleArg[str],
  default="cohort_start_date",
        description='Variable containing the outcome event date. This is usually "cohort_start_date", but another date column in the outcome cohort can be used.'
    ),
    ArgDescription(
        python_arg_name="outcome_washout",
        argument_name="outcomeWashout",
        arg_class=SimpleArg[Annotated[int, Field(ge=0)]],
        default=inf,
	    description="Number of days before target cohort entry used to exclude people with a prior outcome. Inf excludes people with any prior outcome before index; 0 applies no pre-index washout."
    ),
    ArgDescription(
        python_arg_name="censor_on_cohort_exit",
        argument_name="censorOnCohortExit",
        arg_class=Flag,
        default=False,
        description="If active, an individual\'s follow up will be censored at their target cohort exit date."
    ),
    ArgDescription(
        python_arg_name="censor_on_date",
        argument_name="censorOnDate",
        arg_class=SimpleArg[date|str|None],
        default=None,
        description="If specified, an individual\'s follow up will be censored at the given date. This can be a scalar Date or the name of a date column in the target cohort table."
        ),
    ArgDescription(
        python_arg_name="weight",
        argument_name="weight",
        arg_class=SimpleArg[str | None],
        description="If specified, the name of a numeric column in the target cohort table containing observation weights."
    ),
    ArgDescription(
        python_arg_name="followup_days",
        argument_name="followUpDays",
        arg_class=SimpleArg[Annotated[int, Field(ge=1)]],
        default=inf,
        description="Number of days to follow up individuals (lower bound 1, upper bound Inf). Follow-up is censored at this value."
    ),
    ArgDescription(
        python_arg_name="strata",
        argument_name="strata",
        arg_class=JsonSerialisedArg[list[str | list[str]] | None],
        description='A list of target cohort column names to stratify by. Each element can be one column name or a character vector of column names for a combined stratum, for example list("sex", c("age_group", "sex")).'
    ),
    ArgDescription(
        python_arg_name="event_gap",
        argument_name="eventGap",
        arg_class=SimpleArg[Annotated[int, Field(ge=1)]],
        default=30,
        description="Days between time points for which to report survival events, which are grouped into the specified intervals."
    ),
    ArgDescription(
        python_arg_name="estimate_gap",
        argument_name="estimateGap",
        arg_class=SimpleArg[Annotated[int, Field(ge=1)]],
        default=1,
        description="Days between time points for which to report survival estimates. First day will be day zero with risk estimates provided for times up to the end of follow-up, with a gap in days equivalent to estimateGap."
    ),
    ArgDescription(
        python_arg_name="restricted_mean_followup",
        argument_name="restrictedMeanFollowUp",
        arg_class=SimpleArg[int | None],
        description="Number of days of follow-up to use when calculating restricted mean summaries. See Details."
    ),
    ArgDescription(
        python_arg_name="minimum_survival_days",
        argument_name="minimumSurvivalDays",
        arg_class=SimpleArg[Annotated[int, Field(ge=1)]],
        default=1,
        description="Minimum number of days required for the main cohort to contribute to the analysis."
    ),
]
