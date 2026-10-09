from typing import Literal

# try:
#     import marimo as mo
# except ImportError:
#     mo = None

from .script_args import (
    ConceptSet,
    ConceptSetArg,
    EndArg,
    Flag,
    RequiredObservationArg,
)
from .base import ScriptArg

DEFINE_CONCEPT_COHORT_TEMPLATE = """
## Define Concept Cohort

**Cohort name** {cohort_name}

**Concept set** {concept_set}

**All Occurrences** {all_occurrences}

**End** {end}

**Required Observation** {required_observation}
"""

class DefineConceptCohort:
    args: list[ScriptArg]

    def __init__(
        self,
        cohort_name: str,
        concept_set: dict[str, list[int]],
        all_occurrences: bool = False,
        end_definition: Literal["observation_period_end_date", "event_end_date"]
        | int = "observation_period_end_date",
        required_observation: tuple[int, int] = (0, 0),
    ) -> None:
        self.script_path = "inst/scripts/defineConceptCohort.R"
        self.cohort_name = cohort_name
        checked_concept_sets = [
            ConceptSet(name=k, concept_ids=v) for k, v in concept_set.items()
        ]
        self.args = [
            Flag(argument_name="allOccurrences", value=all_occurrences),
            EndArg(value=end_definition),
            RequiredObservationArg(
                prior=required_observation[0], post=required_observation[1]
            ),
            ConceptSetArg(concept_sets=checked_concept_sets),
        ]

    def render_shell(self) -> str:
        rendered_args = " ".join([arg.render() for arg in self.args])
        return f"Rscript {self.script_path} {self.cohort_name} {rendered_args}"

    # def marimo_form(self):
    #     if mo is not None:
    #         return (
    #             mo.md(
    #                 DEFINE_CONCEPT_COHORT_TEMPLATE
    #                 )
    #             .batch(
    #                 cohort_name = mo.ui.text(),
    #                 all_occurrences = self.args[0].marimo_widget(),
    #                 end = self.args[1].marimo_widget(),
    #                 required_observation = self.args[2].marimo_widget(),
    #                 concept_set = self.args[3].marimo_widget(),
    #                 )
    #             .form()
    #         )
    #
    #     else:
    #         raise ImportError
