import pytest

from tes_omop_callers.define_cohorts import DefineConceptCohort
from tes_omop_callers.shell_bundlers import CohortShellBundler

@pytest.fixture
def define_cohort_task():
    return DefineConceptCohort("test_cohort", concept_set={"diabetes": [201254, 201826]})

@pytest.fixture
def single_definition_cohort_shell_bundler(define_cohort_task):
    return  CohortShellBundler(
            image="ghcr.io/health-informatics-uon/omop-r-tools:sha-9aa526d",
            tasks = [define_cohort_task]
            )

def test_cohort_shell_bundler_handles_cohort(single_definition_cohort_shell_bundler):
    assert single_definition_cohort_shell_bundler.cohorts == ["test_cohort"]
    assert len(single_definition_cohort_shell_bundler.tasks) == 2

def test_cohort_shell_bundler_renders_shell(single_definition_cohort_shell_bundler):
    assert single_definition_cohort_shell_bundler.render_shell() == (
            "Rscript "
            "inst/scripts/defineConceptCohortSet.R test_cohort "
            "--conceptSet='{\"diabetes\": [201254, 201826]}' "
            "--end=observation_period_end_date "
            "--requiredObservation='[0,0]'; "
            "Rscript "
            "inst/scripts/cleanUpCohortTables.R test_cohort"
            )

def test_cohort_shell_bundler_renders_executor(single_definition_cohort_shell_bundler):
    executor = single_definition_cohort_shell_bundler.render_executor()
    assert executor["image"] == "ghcr.io/health-informatics-uon/omop-r-tools:sha-9aa526d"
    assert executor["command"][:2] == ["bin/sh", "-c"]

# Two cohorts defined
@pytest.fixture
def second_define_cohort_task():
    return DefineConceptCohort("test_cohort_2", concept_set={"neoplasm": [123456]})

@pytest.fixture
def two_definition_cohort_shell_bundler(define_cohort_task, second_define_cohort_task):
    return  CohortShellBundler(
            image="ghcr.io/health-informatics-uon/omop-r-tools:sha-9aa526d",
            tasks = [define_cohort_task, second_define_cohort_task]
            )

def test_cohort_shell_bundler_handles_two_cohorts(two_definition_cohort_shell_bundler):
    # Using a set is non-deterministic in the ordering
    assert len(two_definition_cohort_shell_bundler.cohorts) == 2
    assert "test_cohort" in two_definition_cohort_shell_bundler.cohorts
    assert "test_cohort_2" in two_definition_cohort_shell_bundler.cohorts
    assert len(two_definition_cohort_shell_bundler.tasks) == 3

def test_cohort_shell_bundler_renders_two_cohorts(two_definition_cohort_shell_bundler):
    shell_command = two_definition_cohort_shell_bundler.render_shell()
    assert "--conceptSet='{\"diabetes\": [201254, 201826]}' " in shell_command
    assert "--conceptSet='{\"neoplasm\": [123456]}' " in shell_command
    dropped_tables = shell_command.split("inst/scripts/cleanUpCohortTables.R")[1]
    assert "test_cohort" in dropped_tables
    assert "test_cohort_2" in dropped_tables
