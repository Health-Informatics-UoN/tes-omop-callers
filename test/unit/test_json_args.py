from tes_omop_callers.script_args import JsonSerialisedArg


def test_int_tuples_print():
    assert (
        JsonSerialisedArg[list[tuple[int, int]]](
            argument_name="ageGroup", value=[(0, 150)]
        ).render()
        == "--ageGroup='[[0, 150]]'"
    )

    assert (
        JsonSerialisedArg[list[tuple[int, int]]](
            argument_name="ageGroup", value=[(0, 17), (18, 30)]
        ).render()
        == "--ageGroup='[[0, 17], [18, 30]]'"
    )


def test_dict_print():
    assert (
        JsonSerialisedArg[dict](
            argument_name="conceptSet", value={"diabetes": [201254, 201826]}
        ).render()
        == "--conceptSet='{\"diabetes\": [201254, 201826]}'"
    )
