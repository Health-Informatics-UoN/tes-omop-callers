import json
import shlex
from typing import Annotated, Any, Generic, Literal, TypeVar, override

from pydantic import BaseModel, Field

try:
    import marimo as mo
except ImportError:
    mo = None

# from .widgets.marimo import default_marimo_widgets

T = TypeVar("T")


class SimpleArg(BaseModel):
    argument_name: str
    value: Any

    def render(self) -> str:
        if self.value is not None:
            return f"--{self.argument_name}={self.value}"
        else:
            return ""

    # def marimo_widget(self):
    #     try:
    #         model_json = self.model_json_schema()
    #         properties = model_json["properties"]["value"]
    #         default_marimo_widgets[type(self.value)](
    #             {**properties},
    #             label=self.argument_name,
    #         )
    #     except KeyError as e:
    #         raise e
    #     except ImportError as e:
    #         raise e


class Flag(BaseModel):
    argument_name: str
    value: bool

    def render(self) -> str:
        if self.value:
            return f"--{self.argument_name}"
        else:
            return ""

    # def marimo_widget(self):
    #     if mo is not None:
    #         return mo.ui.switch(value=self.value, label=self.argument_name)
    #     else:
    #         raise ImportError(
    #             "The marimo group needs to be installed to use their widgets"
    #         )


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

    # @override
    # def marimo_widget(self):  # noqa
    #     if mo is not None:
    #         return mo.ui.dropdown(
    #             options=["observation_period_end_date", "event_end_date"],
    #             label=self.argument_name,
    #         )
    #     else:
    #         raise ImportError(
    #             "The marimo group needs to be installed to use their widgets"
    #         )


class RequiredObservationArg(BaseModel):
    argument_name: str = "requiredObservation"
    prior: int = 0
    post: int = 0

    def render(self) -> str:
        return f"--{self.argument_name}='[{self.prior},{self.post}]'"

    # def marimo_widget(self):
    #     if mo is not None:
    #         return mo.hstack(
    #             [
    #                 mo.md(self.argument_name),
    #                 mo.ui.number(start=0, step=1, label="Prior"),
    #                 mo.ui.number(start=0, step=1, label="post"),
    #             ]
    #         )
    #     else:
    #         raise ImportError(
    #             "The marimo group needs to be installed to use their widgets"
    #         )


class ConceptSet(BaseModel):
    name: str
    concept_ids: list[int]

    # @staticmethod
    # def marimo_widget():
    #     if mo is not None:
    #         return mo.hstack(
    #             [mo.ui.text(label="Name"), mo.ui.text(label="Concept IDs")]
    #         )
    #     else:
    #         raise ImportError


class ConceptSetArg(BaseModel):
    argument_name: str = "conceptSet"
    concept_sets: list[ConceptSet]

    def render(self) -> str:
        concept_set_dict = {cs.name: cs.concept_ids for cs in self.concept_sets}
        return f"--{self.argument_name}={shlex.quote(json.dumps(concept_set_dict))}"

    # def marimo_widget(self):
    #     if mo is not None:
    #         return mo.hstack([mo.md("Concept sets"), ConceptSet.marimo_widget()])
    #     else:
    #         raise ImportError
