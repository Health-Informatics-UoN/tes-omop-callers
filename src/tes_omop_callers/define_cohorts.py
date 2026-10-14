from typing import Literal

from .base import OMOPScriptTask
from .script_args import (
    ConceptSet,
    ConceptSetArg,
    EndArg,
    Flag,
    RequiredObservationArg,
)


class DefineConceptCohort(OMOPScriptTask):
    """
    Specification for adding a concept set cohort table
    """

    def __init__(
        self,
        cohort_name: str,
        concept_set: dict[str, list[int]],
        all_occurrences: bool = False,
        end_definition: Literal["observation_period_end_date", "event_end_date"]
        | int = "observation_period_end_date",
        required_observation: tuple[int, int] = (0, 0),
    ) -> None:
        """
        Parameters
        ----------
        cohort_name: str
            The name of the cohort
        concept_set: dict[str, list[int]]
            A dictionary where the key is the name of a concept set and the value is a list of OMOP concept_ids
        all_occurrences: bool
            Include all occurrences of events in the cohort. Otherwise, only includes the first
        end_definition: Literal["observation_period_end_date", "event_end_date"] | int
            Which column to use for the cohort end date. Default is "observation_period_end_date"
        required_observation: tuple[int, int]
            Pair of days of required observation time prior and post index, e.g. "0,0" [default: 0,0]
        """
        self.script_path = "inst/scripts/defineConceptCohortSet.R"
        self.cohort_name = cohort_name
        self.cohorts = [cohort_name]
        checked_concept_sets = [
            ConceptSet(name=k, concept_ids=v) for k, v in concept_set.items()
        ]
        self.arguments = [
            ConceptSetArg(concept_sets=checked_concept_sets),
            Flag(argument_name="alloccurrences", value=all_occurrences),
            EndArg(value=end_definition),
            RequiredObservationArg(
                prior=required_observation[0], post=required_observation[1]
            ),
        ]

    def render(self):
        rendered_args = [arg.render() for arg in self.arguments]
        rendered_args = " ".join([arg for arg in rendered_args if arg != ""])
        return f"Rscript {self.script_path} {self.cohort_name} {rendered_args}"
