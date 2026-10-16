from tes_omop_callers.base import OMOPScriptTask
from tes_omop_callers.script_args import (
    Flag,
    JsonSerialisedArg,
    MonthArg,
    MonthDayArg,
    StringArg,
)


class AddCharacteristics(OMOPScriptTask):
    """
    Specification for the addCharacteristics script which adds characteristics to an existing cohort table
    """

    def __init__(
        self,
        cohort_name: str,
        index_date: str = "cohort_start_date",
        add_age: bool = False,
        age_group: list[tuple[int, int]] | None = None,
        age_name: str = "age",
        missing_month: int | None = None,
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
        """
        Parameters
        ----------
        cohort_name: str
            The name of the cohort table to which characteristics are added
        index_date: str
            The Date column to use as index. Defaults to "cohort_start_date"
        add_age: bool
            Add age at index date. Defaults to False,
        age_group: list[tuple[int, int]] | None
            An optional list of age groups, for example [[0, 17], [18, 30]]
        age_name: str
            Name for the age column. Defaults to "age"
        missing_month: int | None
            Month assumed if missing
        missing_day: int | None
            Day of the week assumed if missing
        age_impose_month: bool
            Impose missing month to ageMissingMonth
        age_impose_day: bool
            Impose missing day to ageMissingDay
        add_sex: bool
            Add sex
        add_prior_observation: bool
            Whether to add days of prior observation
        add_future_observation: bool
            Whether to add days of future observation
        add_in_observation: bool
            Add the in observation flag
        in_observation_window: list[tuple[int, int]] | None
            Window for in-observation
        complete_interval: bool
            Require complete interval for in-observation
        use_demographics: bool
            Whether to use addDemographics to add characteristics
        """
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
            MonthDayArg(argument_name="ageMissingDay", value=missing_day),
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

    def render(self) -> str:
        rendered_args = [arg.render() for arg in self.arguments]
        rendered_args = " ".join([arg for arg in rendered_args if arg != ""])
        return f"Rscript {self.script_path} {self.cohort_name} {rendered_args}"
