# services/users/manage.py
import os
import unittest
from flask.cli import FlaskGroup
import coverage
from V1 import app


cli = FlaskGroup(app)


@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    cli()
