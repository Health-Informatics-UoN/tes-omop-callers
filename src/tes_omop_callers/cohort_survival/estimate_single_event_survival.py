from math import inf
from typing import Annotated
from pydantic import Field
from tes_omop_callers.builders.build_script_task import ArgDescription, build_omop_script_task
from tes_omop_callers.script_args import JsonSerialisedArg, SimpleArg, Flag


args = [
    ArgDescription(
        python_arg_name="target_cohort_table",
        argument_name="targetCohortTable",
        arg_class=SimpleArg[str],
    ),
    ArgDescription(
        python_arg_name="outcome_cohort_table",
        argument_name="outcomeCohortTable",
        arg_class=SimpleArg[str],
    ),
    ArgDescription(
        python_arg_name="output_path",
        argument_name="outputPath",
        arg_class=SimpleArg[str],
        default="outputs/single-event-survival.csv",
    ),
    ArgDescription(
        python_arg_name="target_cohort_id",
        argument_name="targetCohortId",
        arg_class=SimpleArg[str | int | None],
    ),
    ArgDescription(
        python_arg_name="outcome_cohort_id",
        argument_name="outcomeCohortId",
        arg_class=SimpleArg[str | int | None],
    ),
    ArgDescription(
        python_arg_name="outcome_date_variable",
        argument_name="outcomeDateVariable",
        arg_class=SimpleArg[str],
        default="cohort_start_date",
    ),
    ArgDescription(
        python_arg_name="outcome_washout",
        argument_name="outcomeWashout",
        arg_class=SimpleArg[Annotated[int, Field(ge=0)]],
    ),
    ArgDescription(
        python_arg_name="censor_on_cohort_exit",
        argument_name="censorOnCohortExit",
        arg_class=Flag,
        default=False
        ),
    ArgDescription(
        python_arg_name="weight",
        argument_name="weight",
        arg_class=SimpleArg[str|None],
        ),
    ArgDescription(
        python_arg_name="followup_days",
        argument_name="followUpDays",
        arg_class=SimpleArg[Annotated[int, Field(ge=1)]],
        default=inf
        ),
    ArgDescription(
            python_arg_name="strata",
            argument_name="strata",
            arg_class=JsonSerialisedArg[list[str|list[str]]|None],
            ),
    ArgDescription(
            python_arg_name="event_gap",
            argument_name="eventGap",
            arg_class=SimpleArg[Annotated[int, Field(ge=1)]],
            default=30
            ),
    ArgDescription(
            python_arg_name="estimate_gap",
            argument_name="estimateGap",
            arg_class=SimpleArg[Annotated[int, Field(ge=1)]],
            default=1
            ),
    ArgDescription(
            python_arg_name="restricted_mean_followup",
            argument_name="restrictedMeanFollowUp",
            arg_class=SimpleArg[int|None]
            ),
    ArgDescription(
            python_arg_name="minimum_survival_days",
            argument_name="minimumSurvivalDays",
            arg_class=SimpleArg[Annotated[int, Field(ge=1)]],
            default=1
            )
]

docstring = """
Estimate survival for a single event of interest

Parameters:
  targetCohortTable: str
	Name of the cohort table containing the target cohorts. The table must be present in cdm and contain standard OMOP cohort columns.
  outcomeCohortTable: str
	Name of the cohort table containing the outcome cohorts. The table must be present in cdm and contain standard OMOP cohort columns.
  outputPath: str
	Path for saving the survival table as a csv [default: outputs/single-event-survival.csv]
  targetCohortId: str | int | None
	Target cohorts to include. It can either be a cohort_definition_id value or a cohort_name. Multiple ids are allowed. If not provided, all non-empty cohorts in targetCohortTable are used.
  outcomeCohortId: str | int | None
    Outcome cohorts to include. It can either be a cohort_definition_id value or a cohort_name. Multiple ids are allowed. If not provided, all outcome cohorts in outcomeCohortTable are used.
  outcomeDateVariable: str
	Variable containing the outcome event date. This is usually cohort_start_date, but another date column in the outcome cohort can be used.  [default: cohort_start_date]
  outcomeWashout: int
	Number of days before target cohort entry used to exclude people with a prior outcome. Inf excludes people with any prior outcome before index; 0 applies no pre-index washout. [default: Inf]
  censorOnCohortExit: bool
    If True, an individual\'s follow up will be censored at their target cohort exit date. [default: False]
  censorOnDate: bool
	If True, an individual\'s follow up will be censored at the given date. This can be a scalar Date or the name of a date column in the target cohort table.
  weight: str
	If provided, the name of a numeric column in the target cohort table containing observation weights to use in the Kaplan-Meier estimation.
  followUpDays: int
	Number of days to follow up individuals (lower bound 1, upper bound Inf). Follow-up is censored at this value. [default: Inf]
  strata: list[str|list[str]]
	An optional list of target cohort column names to stratify by. Each element can be one column name or a list of column names for a combined stratum, for example the input could be ["sex", ["age_group", "sex"]].
  eventGap: int
	Days between time points for which to report survival events, which are grouped into the specified intervals. [default: 30]
  estimateGap: int
	Days between time points for which to report survival estimates. First day will be day zero with risk estimates provided for times up to the end of follow-up, with a gap in days equivalent to estimateGap. [default: 1]
  restrictedMeanFollowUp: int
	Number of days of follow-up to use when calculating restricted mean survival. See Details.
  minimumSurvivalDays: int
	Minimum number of days required for the main cohort to contribute to the analysis. [default: 1]

Returns:
    An OMOPScriptTask for estimating single event survival
"""

EstimateSingleEventSurvival = build_omop_script_task(
        name="EstimateSingleEventSurvival",
        script_path="inst/scripts/estimateSingleEventSurvival.R",
        argument_descriptions=args,
        must_run=False,
        docstring=docstring
        )
