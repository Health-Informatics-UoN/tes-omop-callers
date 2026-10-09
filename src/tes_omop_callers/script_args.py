import json
import shlex
from typing import Annotated, Any, Generic, Literal, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class SimpleArg(BaseModel):
    argument_name: str
    value: Any

    def render(self) -> str:
        if self.value is not None:
            return f"--{self.argument_name}={self.value}"
        else:
            return ""


class Flag(BaseModel):
    argument_name: str
    value: bool

    def render(self) -> str:
        if self.value:
            return f"--{self.argument_name}"
        else:
            return ""


class StringArg(SimpleArg):
    value: str | None


class JsonSerialisedArg(BaseModel, Generic[T]):
    argument_name: str
    value: T

    def render(self) -> str:
        return f"--{self.argument_name}={shlex.quote(json.dumps(self.value))}"


class MonthArg(SimpleArg):
    value: Annotated[int, Field(gt=0, le=12)]


class WeekdayArg(SimpleArg):
    value: Annotated[int, Field(gt=0, le=7)] | None


class EndArg(SimpleArg):
    argument_name: str = "end"
    value: Literal["observation_period_end_date", "event_end_date"] | int


class RequiredObservationArg(BaseModel):
    argument_name: str = "requiredObservation"
    prior: int = 0
    post: int = 0

    def render(self) -> str:
        return f"--{self.argument_name}='[{self.prior},{self.post}]'"


class ConceptSet(BaseModel):
    name: str
    concept_ids: list[int]


class ConceptSetArg(BaseModel):
    argument_name: str = "conceptSet"
    concept_sets: list[ConceptSet]

    def render(self) -> str:
        concept_set_dict = {cs.name: cs.concept_ids for cs in self.concept_sets}
        return f"--{self.argument_name}={shlex.quote(json.dumps(concept_set_dict))}"
