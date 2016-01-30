import types
from contextlib import contextmanager
from functools import wraps
import click
from framework.grader import stack, current_test, scores


@contextmanager
def test_group(name):
    stack.append(name)
    scores.setdefault(current_test(), 0)
    try:
        yield
    finally:
        stack.pop(len(stack) - 1)


def test(requires=None):
    if requires is None:
        requires = []
    if not isinstance(requires, types.ListType):
        requires = [requires]
    requires = {req: 1 for req in requires}

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with test_group(func.__name__):
                for test_name, min_score in requires.iteritems():
                    if isinstance(test_name, types.FunctionType):
                        test_name = test_name.__name__
                    your_score = scores[test_name]
                    if your_score < min_score:
                        msg = "Skipping `%s` since your score in `%s` (%d) does not meet the minimum requirement (%d)." % (
                            current_test(), test_name, your_score, min_score)
                        click.secho(msg, fg='blue', bold=True)
                        return
                return func(*args, **kwargs)

        return wrapper

    return decorator
