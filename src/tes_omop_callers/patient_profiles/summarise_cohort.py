from typing import Any, Literal

from ..builders.build_script_task import ArgDescription, build_omop_script_task
from ..script_args import JsonSerialisedArg, SimpleArg
from tes_omop_callers import script_args


class RLogicalArg(SimpleArg[Literal["TRUE", "FALSE"]]): ...


args = [
    ArgDescription(
        python_arg_name="output_path",
        argument_name="outputPath",
        arg_class=SimpleArg[str],
        default="outputs/cohort_summary.csv",
    ),
    ArgDescription(
        python_arg_name="group",
        argument_name="group",
        arg_class=SimpleArg[str | None],
    ),
    ArgDescription(
        python_arg_name="include_overall_group",
        argument_name="includeOverallGroup",
        arg_class=RLogicalArg,
        default="TRUE",
    ),
    ArgDescription(
        python_arg_name="strata",
        argument_name="strata",
        arg_class=JsonSerialisedArg[list[str] | None],
        default=None,
    ),
    ArgDescription(
        python_arg_name="include_overall_strata",
        argument_name="includeOverallStrata",
        arg_class=RLogicalArg,
        default="TRUE",
    ),
    ArgDescription(
        python_arg_name="variables",
        argument_name="variables",
        arg_class=JsonSerialisedArg[list[str]],
        default=[],
    ),
    ArgDescription(
        python_arg_name="estimates",
        argument_name="estimates",
        arg_class=JsonSerialisedArg[list[str]],
        default=["count", "percentage"],
    ),
    ArgDescription(
        python_arg_name="counts",
        argument_name="counts",
        arg_class=RLogicalArg,
        default="TRUE",
    ),
    ArgDescription(
        python_arg_name="weights",
        argument_name="weights",
        arg_class=JsonSerialisedArg[list[str] | None],
    ),
    ArgDescription(
        python_arg_name="custom_estimates",
        argument_name="customEstimates",
        arg_class=JsonSerialisedArg[dict[str, Any]],
        default={},
    ),
]
docstring = """
Summarise a cohort after feature generation using the PatientProfiles standard API.

Usage:

Parameters
----------
  -h --help                     Show this screen
  --version                     Show version
  --output-path=<output_path>   Path to write the summary csv to [default: outputs/cohort_summary.csv]
  --group=<group>               Optional group variable name
  --includeOverallGroup=<logical>  Include overall group [default: TRUE]
  --strata=<json>               JSON vector/list of strata variable names [default: []]
  --includeOverallStrata=<logical> Include overall strata [default: TRUE]
  --variables=<json>            JSON vector/list of variables to summarise [default: []]
  --estimates=<json>            JSON vector/list of estimates to calculate [default: ["count","percentage"]]
  --counts=<logical>            Include record/subject counts [default: TRUE]
  --weights=<json>              Optional weights variable name(s) or NULL [default: NULL]
  --customEstimates=<json>      Optional custom estimates config [default: {}]
"""

SummariseCohort = build_omop_script_task(
        name="SummariseCohort",
        script_path="inst/scripts/summariseCohort.R",
        argument_descriptions=args,
        must_run=False
        )
