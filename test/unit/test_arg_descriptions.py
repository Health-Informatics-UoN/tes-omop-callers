from typing import Annotated

from pydantic import Field, ValidationError
import pytest

from tes_omop_callers.builders.build_script_task import (
    ArgDescription,
)
from tes_omop_callers.script_args import SimpleArg


@pytest.fixture
def arg_descriptions() -> list[ArgDescription]:
    return [
        ArgDescription(
            python_arg_name="test_month",
            argument_name="testMonth",
            arg_class=SimpleArg[Annotated[int, Field(gt=0, le=12)]],
        ),
        ArgDescription(
            python_arg_name="test_day",
            argument_name="testDay",
            arg_class=SimpleArg[Annotated[int, Field(gt=0, le=7)]],
        ),
    ]


def test_arg_descriptions_validate(arg_descriptions):
    args = [desc.build_arg() for desc in arg_descriptions]
    with pytest.raises(ValidationError):
        _ = args[0](argument_name="testMonth", value=13)
    with pytest.raises(ValidationError):
        _ = args[1](argument_name="testDay", value="Monday")


def test_arg_descriptions_docstrings_single_type_no_default():
    desc = ArgDescription(
        python_arg_name="test_arg",
        argument_name="testArg",
        arg_class=SimpleArg[str],
        description="A test argument with no default",
    )
    assert desc.build_docstring() == "test_arg: str\n\tA test argument with no default"


def test_arg_descriptions_docstrings_single_type_with_default():
    desc = ArgDescription(
        python_arg_name="test_arg",
        argument_name="testArg",
        arg_class=SimpleArg[str],
        default="foo",
        description="A test argument with a default",
    )
    assert (
        desc.build_docstring()
        == "test_arg: str = foo\n\tA test argument with a default"
    )


def test_arg_descriptions_docstrings_optional_no_default():
    desc = ArgDescription(
        python_arg_name="test_arg",
        argument_name="testArg",
        arg_class=SimpleArg[str | None],
        description="A test argument with no default",
    )
    assert (
        desc.build_docstring()
        == "test_arg: str | None = None\n\tA test argument with no default"
    )


def test_arg_descriptions_docstrings_optional_with_default():
    desc = ArgDescription(
        python_arg_name="test_arg",
        argument_name="testArg",
        arg_class=SimpleArg[str | None],
        default="foo",
        description="A test argument with a default",
    )
    assert (
        desc.build_docstring()
        == "test_arg: str | None = foo\n\tA test argument with a default"
    )
