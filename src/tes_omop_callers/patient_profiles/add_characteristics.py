from tes_omop_callers.base import OMOPScriptTask
from tes_omop_callers.script_args import (
    Flag,
    JsonSerialisedArg,
    MonthArg,
    StringArg,
    WeekdayArg,
)


class AddCharacteristics(OMOPScriptTask):
    def __init__(
        self,
        cohort_name: str,
        index_date: str = "cohort_start_date",
        add_age: bool = False,
        age_group: list[tuple[int, int]] | None = None,
        age_name: str = "age",
        missing_month: int = 1,
        missing_day: int | None = None,
        age_impose_month: bool = False,
        age_impose_day: bool = False,
        add_sex: bool = False,
        add_prior_observation: bool = False,
        add_future_observation: bool = False,
        add_in_observation: bool = False,
        in_observation_window: list[tuple[int, int]] | None = None,
        complete_interval: bool = False,
        use_demographics: bool = False,
    ) -> None:
        if in_observation_window is None:
            in_observation_window = [(0, 0)]
        if age_group is None:
            age_group = [(0, 150)]
        self.script_path = "inst/scripts/addCharacteristics.R"
        self.cohort_name = cohort_name
        self.arguments = [
            StringArg(argument_name="indexDate", value=index_date),
            Flag(argument_name="addAge", value=add_age),
            JsonSerialisedArg[list[tuple[int, int]]](
                argument_name="ageGroup", value=age_group
            ),
            StringArg(argument_name="ageName", value=age_name),
            MonthArg(argument_name="ageMissingMonth", value=missing_month),
            WeekdayArg(argument_name="ageMissingDay", value=missing_day),
            Flag(argument_name="ageImposeMonth", value=age_impose_month),
            Flag(argument_name="ageImposeDay", value=age_impose_day),
            Flag(argument_name="addSex", value=add_sex),
            Flag(argument_name="addPriorObservation", value=add_prior_observation),
            Flag(argument_name="addFutureObservation", value=add_future_observation),
            Flag(argument_name="addInObservation", value=add_in_observation),
            JsonSerialisedArg[list[tuple[int, int]]](
                argument_name="inObservationWindow", value=in_observation_window
            ),
            Flag(argument_name="completeInterval", value=complete_interval),
            Flag(argument_name="useDemographics", value=use_demographics),
        ]

    def render_shell(self) -> str:
        rendered_args = [arg.render() for arg in self.arguments]
        rendered_args = " ".join([arg for arg in rendered_args if arg != ""])
        return f"Rscript {self.script_path} {self.cohort_name} {rendered_args}"
