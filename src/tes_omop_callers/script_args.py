from datetime import date
import json
import shlex
from typing import Annotated, Literal, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


# Generics
# --------
class BaseArg[T](BaseModel):
    """
    Base class for a script argument of type T
    """

    argument_name: str
    value: T


class SimpleArg[T](BaseArg[T]):
    """
    Generic class for rendering script arguments where the value can be rendered as its string representation
    """

    def render(self) -> str:
        if self.value is not None:
            return f"--{self.argument_name}={self.value}"
        else:
            return ""


class JsonSerialisedArg[T](BaseArg[T]):
    """
    Generic class for rendering script arguments where the value can be rendered using its shell-quoted json representation
    """

    def render(self) -> str:
        if self.value is not None:
            return f"--{self.argument_name}={shlex.quote(json.dumps(self.value))}"
        else:
            return ""


# Flag for boolean
# ----------------
class Flag(BaseArg[bool]):
    """
    A class for script arguments that are a flag, i.e. present if true, absent if false
    """

    def render(self) -> str:
        if self.value:
            return f"--{self.argument_name}"
        else:
            return ""


# List of args
# ------------
class PositionalList[T](BaseArg[T]):
    """
    Generic class for a script argument that is positional and has no flag preceding it
    """

    argument_name: str = ""
    value: T


class PositionalStrings(PositionalList[list[str]]):
    """
    A class for positional arguments that are described with python strings
    """

    def render(self) -> str:
        return " ".join(self.value)


# Simple args
# -----------
class StringArg(SimpleArg[str | None]): ...


class MonthArg(SimpleArg[Annotated[int, Field(gt=0, le=12)] | None]): ...


class WeekdayArg(SimpleArg[Annotated[int, Field(gt=0, le=7)] | None]): ...


class EndArg(SimpleArg[Literal["observation_period_end_date", "event_end_date"] | int]):
    argument_name: str = "end"


# Specific args
# -------------
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


class DatePair(BaseModel):
    argument_name: str
    start_date: date
    end_date: date

    def render(self) -> str:
        return f"--{self.argument_name}={self.start_date},{self.end_date}"
