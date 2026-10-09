from tes_omop_callers.base import ScriptArg
from tes_omop_callers.script_args import (
    Flag,
    JsonSerialisedArg,
    MonthArg,
    StringArg,
    WeekdayArg,
)


class AddCharacteristics:
    args: list[ScriptArg]

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
        self.args = [
            #  --indexDate=<date_col>        Date column to use as index [default: cohort_start_date]
            StringArg(argument_name="indexDate", value=index_date),
            #  --addAge                      Add age at index date
            Flag(argument_name="addAge", value=add_age),
            #  --ageGroup=<json>             JSON list of age groups [default: [[0,150]]]
            JsonSerialisedArg[list[tuple[int, int]]](
                argument_name="ageGroup", value=age_group
            ),
            #  --ageName=<name>              Name for the age column [default: age]
            StringArg(argument_name="ageName", value=age_name),
            #  --ageMissingMonth=<m>         Month assumed if missing [default: NULL]
            MonthArg(argument_name="ageMissingMonth", value=missing_month),
            #  --ageMissingDay=<d>           Day assumed if missing [default: NULL]
            WeekdayArg(argument_name="ageMissingDay", value=missing_day),
            #  --ageImposeMonth              Impose missing month to ageMissingMonth
            Flag(argument_name="ageImposeMonth", value=age_impose_month),
            #  --ageImposeDay                Impose missing day to ageMissingDay
            Flag(argument_name="ageImposeDay", value=age_impose_day),
            #  --addSex                      Add sex
            Flag(argument_name="addSex", value=add_sex),
            #  --addPriorObservation         Add days of prior observation
            Flag(argument_name="addPriorObservation", value=add_prior_observation),
            #  --addFutureObservation        Add days of future observation
            Flag(argument_name="addFutureObservation", value=add_future_observation),
            #  --addInObservation            Add in-observation flag
            Flag(argument_name="addInObservation", value=add_in_observation),
            #  --inObservationWindow=<win>   Window for in-observation [default: 0,0]
            JsonSerialisedArg[list[tuple[int, int]]](
                argument_name="inObservationWindow", value=in_observation_window
            ),
            #  --completeInterval            Require complete interval for in-observation
            Flag(argument_name="completeInterval", value=complete_interval),
            #  --useDemographics             Use add
            Flag(argument_name="useDemographics", value=use_demographics),
        ]

    def render_shell(self) -> str:
        rendered_args = " ".join([arg.render() for arg in self.args])
        return f"Rscript {self.script_path} {self.cohort_name} {rendered_args}"
