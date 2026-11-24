"""Shared pytest helpers for the course checks."""

import importlib.util

import pytest


@pytest.fixture
def load(request):
    """Import an exercise file by name from the part's `exercises/` folder.

    A check in course/part-XX/checks/ calls load("ex1_ticket_label") and gets
    the module from course/part-XX/exercises/ex1_ticket_label.py.
    """
    exercises = request.path.parent.parent / "exercises"

    def _load(name):
        path = exercises / f"{name}.py"
        if not path.exists():
            pytest.fail(f"Cannot find exercises/{path.name}. Was it renamed or moved?", pytrace=False)
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as error:
            pytest.fail(
                f"exercises/{path.name} crashed while loading: {type(error).__name__}: {error}",
                pytrace=False,
            )
        return module

    return _load
