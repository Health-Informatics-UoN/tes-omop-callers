from typing import Annotated, Literal

from pydantic import Field, ValidationError
import pytest

from tes_omop_callers.builders.build_script_task import (
    ArgDescription,
    build_omop_script_task,
)
from tes_omop_callers.script_args import SimpleArg

@pytest.fixture
def arg_descriptions() -> list[ArgDescription]:
    return [
        ArgDescription(
            python_arg_name="test_month",
            argument_name="testMonth",
            arg_class=SimpleArg[Annotated[int, Field(gt=0, le=12)]]
            ),
        ArgDescription(
            python_arg_name="test_day",
            argument_name="testDay",
            arg_class=SimpleArg[Annotated[int, Field(gt=0, le=7)]]
            )
    ]

@pytest.fixture
def arg_with_default() -> ArgDescription:
    return ArgDescription(
            python_arg_name="best_hobbit",
            argument_name="bestHobbit",
            arg_class=SimpleArg[Literal["Samwise", "Pippin", "Merry", "Frodo"]],
            default="Samwise"
            )

def test_arg_descriptions(arg_descriptions):
    args = [desc.build_arg() for desc in arg_descriptions]
    with pytest.raises(ValidationError):
        _ = args[0](argument_name="testMonth", value=13)
    with pytest.raises(ValidationError):
        _ = args[1](argument_name="testDay", value="Monday")

@pytest.fixture
def built_task(arg_descriptions):
    return build_omop_script_task(
            name="TestTask",
            script_path="test_path",
            argument_descriptions=arg_descriptions,
            must_run=False
            )

def test_build_omop_script_task(built_task):
    test_task = built_task(test_month=5, test_day=5)

    assert not test_task.must_run

    assert test_task.render() == "Rscript test_path --testMonth=5 --testDay=5"

def test_built_task_rejects_extras(built_task):
    with pytest.raises(TypeError):
        _ = built_task(test_month=5, test_day=5, something_else="something else")

@pytest.fixture
def built_task_with_default(arg_descriptions, arg_with_default):
    return build_omop_script_task(
            name="AnotherTestTask",
            script_path="scripts/hobbits.R",
            argument_descriptions=[*arg_descriptions, arg_with_default],
            must_run=True
            )

def test_build_with_default(built_task_with_default):
    no_override = built_task_with_default(test_month=5, test_day=5)

    assert "--bestHobbit=Samwise" in no_override.render()

    override = built_task_with_default(test_month=5, test_day=5, best_hobbit="Frodo")

    assert "--bestHobbit=Frodo" in override.render()

