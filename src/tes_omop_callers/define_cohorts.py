from typing import Literal

from .base import ScriptArg
from .script_args import (
    ConceptSet,
    ConceptSetArg,
    EndArg,
    Flag,
    RequiredObservationArg,
)


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
