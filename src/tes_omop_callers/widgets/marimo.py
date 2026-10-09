from math import inf

try:
    import marimo as mo
except ImportError:
    mo = None


def build_int_widget(
    label: str,
    maximum: int | None = None,
    minimum: int | None = None,
    exclusiveMaximum: int | None = None,
    exclusiveMinimum: int | None = None,
):
    if mo is not None:
        start = max(
            minimum if minimum is not None else -inf,
            exclusiveMinimum + 1 if exclusiveMinimum is not None else -inf,
        )
        end = min(
            maximum if maximum is not None else inf,
            exclusiveMaximum - 1 if exclusiveMaximum is not None else inf,
        )
        return mo.ui.number(
            start=start if start != -inf else None,
            stop=end if end != inf else None,
            step=1,
            label=label,
        )
    else:
        raise ImportError("The marimo group needs to be installed to use their widgets")


def build_string_widget(label: str, maxLength: int | None):
    if mo is not None:
        return mo.ui.text(max_length=maxLength, label=label)
    else:
        raise ImportError("The marimo group needs to be installed to use their widgets")


default_marimo_widgets = {int: build_int_widget, str: build_string_widget}
