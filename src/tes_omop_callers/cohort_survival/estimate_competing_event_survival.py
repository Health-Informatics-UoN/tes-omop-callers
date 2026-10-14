from math import inf
from typing import Annotated

from pydantic import Field

from ..builders.build_script_task import ArgDescription, build_omop_script_task
from ..builders.docstring import build_docstring
from ..script_args import JsonSerialisedArg, SimpleArg
from .arg_descriptions import cohort_survival_common_args

args = [
    *cohort_survival_common_args,
    ArgDescription(
        python_arg_name="competing_outcome_cohort_table",
        argument_name="competingOutcomeCohortTable",
        arg_class=SimpleArg[str],
        description="Name of the cohort table containing the competing outcome.",
    ),
    ArgDescription(
        python_arg_name="competing_outcome_cohort_id",
        argument_name="competingOutcomeCohortId",
        arg_class=JsonSerialisedArg[list[str] | list[int] | None],
        description="Competing outcome cohorts to include. It can either be a cohort_definition_id value or a cohort_name. Multiple ids are allowed. If omitted, all competing outcome cohorts in competingOutcomeCohortTable are used.",
    ),
    ArgDescription(
        python_arg_name="competing_outcome_date_variable",
        argument_name="competingOutcomeDateVariable",
        arg_class=SimpleArg[str],
        default="cohort_start_date",
        description="Variable containing the competing outcome event date.",
    ),
    ArgDescription(
        python_arg_name="competing_outcome_washout",
        argument_name="competingOutcomeWashout",
        default=inf,
        arg_class=SimpleArg[Annotated[int, Field(ge=0)]],
        description="Number of days before target cohort entry used to exclude people with a prior competing outcome. Inf excludes people with any prior competing outcome before index; 0 applies no pre-index washout.",
    ),
    ArgDescription(
        python_arg_name="output_path",
        argument_name="outputPath",
        arg_class=SimpleArg[str],
        default="outputs/competing-event-survival.csv",
        description="Path for saving the survival table as a csv",
    ),
]

description = "Estimate time-to-event probabilities for one or more target cohorts when an event of interest can be precluded by a competing outcome."
return_description = "An OMOPScriptTask for estimating competing event survival"

docstring = build_docstring(description, args, return_description)

EstimateCompetingEventSurvival = build_omop_script_task(
    name="EstimateCompetingEventSurvival",
    script_path="inst/scripts/estimateCompetingEventSurvial.R",
    argument_descriptions=args,
    must_run=False,
    docstring=docstring,
)
