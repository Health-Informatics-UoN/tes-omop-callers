# TES OMOP callers
A library for creating executors for a TES message.
Designed for calling OMOP scripts, but could actually be used more widely.
Naming things is hard.

## Usage

Some tasks are predefined for you.
For example, to create a concept set cohort using the [omop-r-tools](https://github.com/Health-Informatics-UoN/omop-r-toolkit):

```python
from tes_omop_callers.define_cohorts import DefineConceptCohort

cohort_task = DefineConceptCohort(
    "diabetes_cohort", concept_set={"diabetes": [201254, 201826]}
)
```

This will specify a task that creates a cohort table of people with diabetes (matching the concept_ids specified).
By itself, this does nothing.

We can add another task for incidence and prevalence:

```python
from tes_omop_callers.incidence_prevalence import IncidencePrevalence

i_p_task = IncidencePrevalence(
    "denom", "diabetes_cohort", estimate_incidence_output_path="outputs/incidence.csv"
)
```

This task estimates the incidence of diabetes in your population based on their entry into the diabetes cohort defined earlier.

These tasks are still just python objects, but they can create commands to execute the task using their `render` method.
For example, calling `cohort_task.render()` will return:

```sh
Rscript inst/scripts/defineConceptCohortSet.R test_cohort --conceptSet='{\"diabetes\": [201254, 201826]}' --end=observation_period_end_date --requiredObservation='[0,0]'"
```

These tasks can be used and chained together with a bundler

```python
from tes_omop_callers.shell_bundlers import CohortShellBundler

cohort_bundler = CohortShellBundler(
    image="ghcr.io/health-informatics-uon/omop-r-tools:sha-9aa526d",
    tasks=[cohort_task, i_p_task],
)
```

Calling `cohort_bundler.render` will create a string to execute the scripts as a shell command:

```sh
Rscript inst/scripts/defineConceptCohortSet.R diabetes_cohort --conceptSet=\'{"diabetes": [201254, 201826]}\' --end=observation_period_end_date --requiredObservation=\'[0,0]\'&& Rscript inst/scripts/incidencePrevalence.R diabetes_cohort --denominatorCohortDateRange=1900-01-01,2100-01-01 --denominatorAgeGroup=\'[[0, 150]]\' --denominatorDaysPriorObservation=0 --requirementInteractions --outcomeCohortName=denom --estimateIncidenceOutputPath=outputs/incidence.csv --incidence_interval=years --incidenceOutcomeWashout=0 --pointPrevalenceInterval=years --pointPrevalenceTimePoint=start --periodPrevalenceInterval=years; Rscript inst/scripts/cleanUpCohortTables.R diabetes_cohort
```

This chains together the tasks defined above, and adds one at the end that drops the cohort table you created earlier at the end.

If instead, you call `cohort_bundler.render_executor()`, you will get:

```python
{
    "image": "ghcr.io/health-informatics-uon/omop-r-tools:sha-9aa526d",
    "command": [
        "bin/sh",
        "-c",
        "Rscript inst/scripts/defineConceptCohortSet.R diabetes_cohort --conceptSet='{\"diabetes\": [201254, 201826]}' --end=observation_period_end_date --requiredObservation='[0,0]'&& Rscript inst/scripts/incidencePrevalence.R diabetes_cohort --denominatorCohortDateRange=1900-01-01,2100-01-01 --denominatorAgeGroup='[[0, 150]]' --denominatorDaysPriorObservation=0 --requirementInteractions --outcomeCohortName=denom --estimateIncidenceOutputPath=outputs/incidence.csv --incidence_interval=years --incidenceOutcomeWashout=0 --pointPrevalenceInterval=years --pointPrevalenceTimePoint=start --periodPrevalenceInterval=years; Rscript inst/scripts/cleanUpCohortTables.R diabetes_cohort",
    ],
}
```

This can be used as an executor in a TES message, and can be used in conjunction with the [Five Safes TES workbench](https://github.com/federated-research/Five-Safes-TES-Workbench/)

```python
wb = Workbench()

wb.build_tes.custom(
    # Other arguments to the custom template
    ...,
    executors=[cohort_bundler.render_executor()],
)

wb.submit()
```

## Setting up tasks
Some tasks are defined here, but the library is meant to make things easier if you want to define a task to execute in this way.
Each task has some arguments, which might have some constraints we can impose when creating the arguments.

### Arguments
To help with creating arguments, the `ScriptArg` protocol is defined:

```python
class ScriptArg(Protocol):
    argument_name: str

    def render(self) -> str: ...
```

This means it has to have a name, and a method that returns a string.
The protocol by itself doesn't do much.
Two examples of classes that implement this will cover a lot of use cases.

#### `SimpleArg`
Some arguments will have a value that can be passed to the script as the value's string representation and we can use a `SimpleArg`:

```python
class SimpleArg[T](BaseArg[T]):
    argument_name: str
    value: T

    def render(self) -> str:
        if self.value is not None:
            return f"--{self.argument_name}={self.value}"
        else:
            return ""
```

When creating an instance of a `SimpleArg`, you can parameterize it with a type, e.g.:

```python
SimpleArg[Annotated[int, Field(ge=0)]]
```

will create a class that will reject any value that isn't an integer greater than or equal to 0.
This means you can render the argument safe in the knowledge that some target script which only accepts positive integers won't fail because that argument is wrong.

#### `JsonSerialisedArg`
In a similar way, if you have a value which needs to be serialised to JSON, you can impose similar constraints on the values.
For example:

```python
JsonSerialisedArg[list[tuple[int, int]]]
```

will create an argument that will only accept lists of integer 2-tuples, and will generate a command-line argument where the value is the JSON for those.

#### `Flag`
Some command-line options don't have a value, and are flags.
If specified, the flag is on, otherwise it's off.
Creating a `Flag` `ScriptArg` will handle this.

#### Others
These examples cover a lot of uses.
More particular cases are in `tes_omop_callers.script_args`.

### Building a task
The task specifications used above have been implemented for you.
To make it easier to describe a task yourself, there is a function, `tes_omop_callers.builders.build_omop_script_task`, which takes a list of descriptions of command-line arguments and builds one of these classes for you.

#### `ArgDescription`
To describe an argument for this way of building a task, you need to specify what python will call the argument, what the command-line argument name is, the type of argument it is, and possibly a default.

```python
ArgDescription(
    python_arg_name="test_month",
    argument_name="testMonth",
    arg_class=SimpleArg[Annotated[int, Field(gt=0, le=12)]],
)
```

This uses the `SimpleArg` class defined above to define an argument that can take values 1 -> 12.

#### `build_omop_script_task`
If you have multiple arguments for your script, you can use this to build a task.

```python
arg_descriptions = [
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
```

If you pass this to `build_omop_script_task`:

```python
Task = build_omop_script_task(
    name="TestTask",
    script_path="test_path",
    argument_descriptions=arg_descriptions,
)
```

then `Task` will be a class that takes your `arg_descriptions` `python_arg_name` attributes as initialisation parameters.

```python
Task(test_month=5, test_day=5)  # will return a Task instance
Task(test_month=5)  # will fail because test_day is not defined
Task(test_month=5, test_day=5, year=2026)  # will fail because it has no year parameter
```

These tasks can then be used to render executors, etc.
A docstring for the task can also be passed in.
