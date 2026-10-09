import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from tes_omop_callers.define_cohorts import DefineConceptCohort

    return (DefineConceptCohort,)


@app.cell
def _(DefineConceptCohort):
    concept_set = DefineConceptCohort(
        cohort_name="test_diabetes",
        concept_set={"diabetes": [1289812]}
    )
    return (concept_set,)


@app.cell
def _(concept_set):
    concept_set.marimo_form()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
