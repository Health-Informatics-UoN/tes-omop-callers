import pytest
from pydantic import ValidationError

from tes_omop_callers.script_args import EndArg, MonthArg, StringArg


def test_string_arg_prints():
    arg = StringArg(argument_name="wizard", value="Gandalf")
    assert arg.render() == "--wizard=Gandalf"


def test_string_arg_rejects_numbers():
    with pytest.raises(ValidationError):
        _ = StringArg(argument_name="wizard", value=1)


def test_month_arg_prints():
    arg = MonthArg(argument_name="valentinesMonth", value=2)
    assert arg.render() == "--valentinesMonth=2"


def test_month_arg_rejects_oob():
    with pytest.raises(ValidationError):
        _ = MonthArg(argument_name="nextYear", value=13)
    with pytest.raises(ValidationError):
        _ = MonthArg(argument_name="lastYear", value=-3)


def test_end_arg_prints_event():
    arg = EndArg(value="event_end_date")
    assert arg.render() == "--end=event_end_date"


def test_end_arg_prints_observation():
    arg = EndArg(value="observation_period_end_date")
    assert arg.render() == "--end=observation_period_end_date"


def test_end_arg_prints_int():
    arg = EndArg(value=1)
    assert arg.render() == "--end=1"


def test_end_arg_rejects():
    with pytest.raises(ValidationError):
        _ = EndArg(value="after_the_end")
