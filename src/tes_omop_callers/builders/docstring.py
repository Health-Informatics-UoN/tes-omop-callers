from .build_script_task import ArgDescription


def build_docstring(
    description: str, args: list[ArgDescription], returns_description: str
) -> str:
    parameters_description = "\n".join([arg.build_docstring() for arg in args])
    return f"""{description}

Parameters
----------
{parameters_description}

Returns
-------
{returns_description}
"""
