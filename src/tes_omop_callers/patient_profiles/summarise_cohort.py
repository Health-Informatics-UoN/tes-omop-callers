from typing import Any, Literal

from ..builders.build_script_task import ArgDescription, build_omop_script_task
from ..builders.docstring import build_docstring
from ..script_args import JsonSerialisedArg, SimpleArg


class RLogicalArg(SimpleArg[Literal["TRUE", "FALSE"]]): ...


args = [
    ArgDescription(
        python_arg_name="output_path",
        argument_name="outputPath",
        arg_class=SimpleArg[str],
        default="outputs/cohort_summary.csv",
        description="Path to write the summary csv to",
    ),
    ArgDescription(
        python_arg_name="group",
        argument_name="group",
        arg_class=SimpleArg[str | None],
        description="Optional group variable name",
    ),
    ArgDescription(
        python_arg_name="include_overall_group",
        argument_name="includeOverallGroup",
        arg_class=RLogicalArg,
        default="TRUE",
        description="Include overall group",
    ),
    ArgDescription(
        python_arg_name="strata",
        argument_name="strata",
        arg_class=JsonSerialisedArg[list[str] | None],
        default=[],
        description="JSON vector/list of strata variable names",
    ),
    ArgDescription(
        python_arg_name="include_overall_strata",
        argument_name="includeOverallStrata",
        arg_class=RLogicalArg,
        default="TRUE",
        description="Include overall strata ",
    ),
    ArgDescription(
        python_arg_name="variables",
        argument_name="variables",
        arg_class=JsonSerialisedArg[list[str]],
        default=[],
        description="list of variables to summarise",
    ),
    ArgDescription(
        python_arg_name="estimates",
        argument_name="estimates",
        arg_class=JsonSerialisedArg[list[str]],
        default=["count", "percentage"],
        description="list of estimates to calculate",
    ),
    ArgDescription(
        python_arg_name="counts",
        argument_name="counts",
        arg_class=RLogicalArg,
        default="TRUE",
        description="Include record/subject counts",
    ),
    ArgDescription(
        python_arg_name="weights",
        argument_name="weights",
        arg_class=JsonSerialisedArg[list[str] | None],
        description="Optional weights variable name(s)",
    ),
    ArgDescription(
        python_arg_name="custom_estimates",
        argument_name="customEstimates",
        arg_class=JsonSerialisedArg[dict[str, Any]],
        default={},
        description="Optional custom estimates config",
    ),
]

description = "Summarise a cohort after feature generation using the PatientProfiles standard API."
returns_description = "An OMOPScriptTask for summarising a cohort"

docstring = build_docstring(description, args, returns_description)

SummariseCohort = build_omop_script_task(
    name="SummariseCohort",
    script_path="inst/scripts/summariseCohort.R",
    argument_descriptions=args,
    docstring=docstring,
    must_run=False,
)
