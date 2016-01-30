import click

stack = []
scores = {}
config = {
    'student_bin': '/bin/false'
}


def current_test():
    return '.'.join(stack)


def grade(score, cond):
    color = 'green' if cond else 'red'
    got = score if cond else 0
    scores[current_test()] += got
    click.secho('%s: %s' % (current_test(), got), fg=color, bold=True)
