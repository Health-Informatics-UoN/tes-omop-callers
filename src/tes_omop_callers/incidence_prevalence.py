from datetime import date
from typing import Annotated, Literal

from pydantic import Field

from tes_omop_callers.base import OMOPScriptTask
from tes_omop_callers.script_args import DatePair, Flag, JsonSerialisedArg, SimpleArg, StringArg

IMInterval = Literal["years", "months", "quarters", "weeks", "overall"]
IMTimePoint = Literal["start", "middle", "end"] # This is a bit of a guess, I can see "start", and "middle" in the docs

class IncidencePrevalence(OMOPScriptTask):
    def __init__(
        self,
        denominator_cohort_name: str,
        outcome_cohort_name: str,
        denominator_cohort_date_range: tuple[date, date] | None = None,
        denominator_age_group: list[tuple[int, int]] = [(0, 150)],
        denominator_both_off: bool = False,
        denominator_male: bool = False,
        denominator_female: bool = False,
        denominator_days_prior_observation: Annotated[int, Field(ge=0)] = 1,
        requirement_interactions: bool = False,
        estimate_incident_output_path: str | None = None,
        incidence_interval: IMInterval = "years",
        incidence_outcome_washout: Annotated[int, Field(ge=0)] = 0,
        incidence_repeated_events: bool = False,
        estimate_point_prevalence_output_path: str | None = None,
        point_prevalence_interval: IMInterval = "years",
        point_prevalence_time_point: IMTimePoint = "start",
        estimate_period_prevalence_output_path: str | None = None,
        period_prevalence_interval: IMInterval = "years"
    ) -> None:
        self.script_path = "inst/scripts/incidencePrevalence.R"
        if denominator_cohort_date_range is None:
            denominator_cohort_date_range = (date(1900, 1, 1), date(2100, 1, 1))
        self.denominator_cohort_name = denominator_cohort_name
        self.outcome_cohort_name = outcome_cohort_name
        self.arguments = [
            DatePair(argument_name="denominatorCohortDateRange", start_date=min(denominator_cohort_date_range), end_date=max(denominator_cohort_date_range)),
            JsonSerialisedArg[list[tuple[int,int]]](argument_name="denominatorAgeGroup", value=denominator_age_group),
            Flag(argument_name="denominatorBothOff", value=denominator_both_off),
            Flag(argument_name="denominatorMale", value=denominator_male),
            Flag(argument_name="denominatorFemale", value=denominator_female),
            SimpleArg[Annotated[int, Field(ge=0)]](argument_name="denominatorDaysPriorObservation", value=denominator_days_prior_observation),
            Flag(argument_name="requirementInteractions", value=requirement_interactions),
            SimpleArg[str](argument_name="outcomeCohortName", value=outcome_cohort_name),
            StringArg(argument_name="estimateIncidenceOutputPath", value=estimate_incident_output_path),
            SimpleArg[IMInterval](argument_name="incidence_interval", value=incidence_interval),
            SimpleArg[Annotated[int, Field(ge=0)]](argument_name="incidenceOutcomeWashout", value=incidence_outcome_washout),
            Flag(argument_name="incidenceRepeatedEvents", value = incidence_repeated_events),
            StringArg(argument_name="estimatePointPrevalenceOutputPath", value=estimate_point_prevalence_output_path),
            SimpleArg[IMInterval](argument_name="pointPrevalenceInterval", value=point_prevalence_interval),
            SimpleArg[IMTimePoint](argument_name="pointPrevalenceTimePoint", value=point_prevalence_time_point),
            StringArg(argument_name="estimatePeriodPrevalenceOutputPath", value=estimate_period_prevalence_output_path),
            SimpleArg[IMInterval](argument_name="periodPrevalenceInterval", value=period_prevalence_interval)
        ]
    
    def render_shell(self) -> str:
        rendered_args = [arg.render() for arg in self.arguments]
        rendered_args = " ".join([arg for arg in rendered_args if arg != ""])
        return f"Rscript {self.script_path} {self.denominator_cohort_name} {rendered_args}"

