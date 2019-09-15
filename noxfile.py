import nox


@nox.session
def lint(session):
    session.install('flake8')
    session.run('flake8')


@nox.session
def tests(session):
    session.install("-r", "requirements-dev.txt")
    session.run('python', 'manage.py', 'test')
