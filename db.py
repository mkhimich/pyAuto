from datetime import datetime

from peewee import *

db = SqliteDatabase('test_result.db')


class TestResult(Model):
    id = IntegerField(primary_key=True, unique=True)
    name = CharField()
    browser = CharField()
    start_time = DateTimeField(default=datetime.now)
    result = CharField()
    error = CharField()

    class Meta:
        database = db  # This model uses the "test_result.db" database.


def insert_result(test_name, test_browser, test_start_time, test_result, error_massage):
    TestResult.create(name=test_name, browser=test_browser, strat_time=test_start_time, result=test_result,
                      error=error_massage)
