from typing import Annotated
import pytest
from pydantic import Field, ValidationError

from tes_omop_callers.script_args import EndArg, MonthArg, SimpleArg, StringArg


def test_simple_arg_str_prints():
    arg = SimpleArg[str](argument_name="wizard", value="Gandalf")
    assert arg.render() == "--wizard=Gandalf"

def test_simple_arg_str_rejects_numbers():
    with pytest.raises(ValidationError):
        _ = SimpleArg[str](argument_name="wizard", value=1)

def test_simple_arg_int_limit_rejects():
    with pytest.raises(ValidationError):
        _ = SimpleArg[Annotated[int, Field(lt=10)]](argument_name="finger", value=30)

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
