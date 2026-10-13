from datetime import date
from typing import Annotated, Literal

from pydantic import Field

from tes_omop_callers.base import OMOPScriptTask
from tes_omop_callers.script_args import (
    DatePair,
    Flag,
    JsonSerialisedArg,
    SimpleArg,
    StringArg,
)

IMInterval = Literal["years", "months", "quarters", "weeks", "overall"]
IMTimePoint = Literal[
    "start", "middle", "end"
]  # This is a bit of a guess, I can see "start", and "middle" in the docs


class IncidencePrevalence(OMOPScriptTask):
    """
    Specification of an IncidencePrevalence task
    """
    def __init__(
        self,
        outcome_cohort_name: str,
        denominator_cohort_name: str | None = None,
        denominator_cohort_date_range: tuple[date, date] | None = (date(1900, 1, 1), date(2100, 1, 1)),
        denominator_age_group: list[tuple[int, int]] = [(0, 150)],
        denominator_both_off: bool = False,
        denominator_male: bool = False,
        denominator_female: bool = False,
        denominator_days_prior_observation: Annotated[int, Field(ge=0)] = 0,
        requirement_interactions: bool = True,
        estimate_incidence_output_path: str | None = None,
        incidence_interval: IMInterval = "years",
        incidence_outcome_washout: Annotated[int, Field(ge=0)] = 0,
        incidence_repeated_events: bool = False,
        estimate_point_prevalence_output_path: str | None = None,
        point_prevalence_interval: IMInterval = "years",
        point_prevalence_time_point: IMTimePoint = "start",
        estimate_period_prevalence_output_path: str | None = None,
        period_prevalence_interval: IMInterval = "years"
    ) -> None:
        """
        Parameters
        ----------
        outcome_cohort_name: str
            Pre-defined outcome cohort name
        denominator_cohort_name: str | None = None
            Name to use for the denominator cohort
        denominator_cohort_date_range: tuple[date, date] | None = (date(1900, 1, 1), date(2100, 1, 1))
            Optional pair of dates, the first indicating the earliest cohort start date and the second indicating the latest possible cohort end date.
        denominator_age_group: list[tuple[int, int]] = [(0, 150)]
            A list of age groups for which cohorts will be created.
        denominator_both_off: bool = False
            If True, do not have a cohort of people assigned either Male or Female.
        denominator_male: bool = False
            Have a cohort of people assigned Male.
        denominator_female: bool = False
            Have a cohort of people assigned Female.
        denominator_days_prior_observation: Annotated[int, Field(ge=0)] = 0
            The number of days of prior observation required for an individual to start contributing time in a cohort.
        requirement_interactions: bool = True
            If True, cohorts will be created for all combinations of ageGroup, sex, and daysPriorObservation. If False, only the first value specified for the other factors will be used.
        estimate_incidence_output_path: str | None = None
            A path to which the output of estimateIncidence is saved.
        incidence_interval: IMInterval = "years"
            The interval for incidence, if estimating incidence.
        incidence_outcome_washout: Annotated[int, Field(ge=0)] = 0
            The washout for incidence, if estimating incidence.
        incidence_repeated_events: bool = False
            Whether to measure repeated events if estimating incidence.
        estimate_point_prevalence_output_path: str | None = None
            A path to which the output of estimatePointPrevalence is saved.
        point_prevalence_interval: IMInterval = "Years"
            The interval for point prevalence, if estimating point prevalence.
        point_prevalence_time_point: IMTimePoint = "start"
            The time point for point prevalence, if estimating point prevalence.
        estimate_period_prevalence_output_path: str | None = None
            A path to which the output of estimatePeriodPrevalence is saved.
        period_prevalence_interval: IMInterval = "Years"
            The interval for period prevalence, if estimating period prevalence.
        """
        self.script_path = "inst/scripts/incidencePrevalence.R"
        if denominator_cohort_date_range is None:
            denominator_cohort_date_range = (date(1900, 1, 1), date(2100, 1, 1))
        self.denominator_cohort_name = denominator_cohort_name
        self.outcome_cohort_name = outcome_cohort_name
        self.arguments = [
            DatePair(
                argument_name="denominatorCohortDateRange",
                start_date=min(denominator_cohort_date_range),
                end_date=max(denominator_cohort_date_range),
            ),
            JsonSerialisedArg[list[tuple[int, int]]](
                argument_name="denominatorAgeGroup", value=denominator_age_group
            ),
            Flag(argument_name="denominatorBothOff", value=denominator_both_off),
            Flag(argument_name="denominatorMale", value=denominator_male),
            Flag(argument_name="denominatorFemale", value=denominator_female),
            SimpleArg[Annotated[int, Field(ge=0)]](
                argument_name="denominatorDaysPriorObservation",
                value=denominator_days_prior_observation,
            ),
            Flag(
                argument_name="requirementInteractions", value=requirement_interactions
            ),
            SimpleArg[str](
                argument_name="outcomeCohortName", value=outcome_cohort_name
            ),
            StringArg(
                argument_name="estimateIncidenceOutputPath",
                value=estimate_incidence_output_path,
            ),
            SimpleArg[IMInterval](
                argument_name="incidence_interval", value=incidence_interval
            ),
            SimpleArg[Annotated[int, Field(ge=0)]](
                argument_name="incidenceOutcomeWashout", value=incidence_outcome_washout
            ),
            Flag(
                argument_name="incidenceRepeatedEvents", value=incidence_repeated_events
            ),
            StringArg(
                argument_name="estimatePointPrevalenceOutputPath",
                value=estimate_point_prevalence_output_path,
            ),
            SimpleArg[IMInterval](
                argument_name="pointPrevalenceInterval", value=point_prevalence_interval
            ),
            SimpleArg[IMTimePoint](
                argument_name="pointPrevalenceTimePoint",
                value=point_prevalence_time_point,
            ),
            StringArg(
                argument_name="estimatePeriodPrevalenceOutputPath",
                value=estimate_period_prevalence_output_path,
            ),
            SimpleArg[IMInterval](
                argument_name="periodPrevalenceInterval",
                value=period_prevalence_interval,
            ),
        ]

    def render(self) -> str:
        rendered_args = [arg.render() for arg in self.arguments]
        rendered_args = " ".join([arg for arg in rendered_args if arg != ""])
        return (
            f"Rscript {self.script_path} {self.denominator_cohort_name} {rendered_args}"
        )
