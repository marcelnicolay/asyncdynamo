from asyncdynamo.orm.session import Session
from tornado import gen

import json


class Table(object):
    def __init__(self, name, key):
        self.name = name
        self.key = key

    def _get_keyschema(self):
        return {"HashKeyElement": {"AttributeName": self.key, "AttributeType": "S"}}

    @staticmethod
    @gen.engine
    def get_or_create(self, name, key, callback):

        table = Table(name, key)

        table_exist = yield gen.Task(table.exist)
        if not table_exist:
            yield gen.Task(table.create)

        callback(table)

    @gen.engine
    def exist(self, callback):
        session = Session()

        response, error = yield gen.Task(session.make_request, action='DescribeTable', body=json.dumps({"TableName": self.name}))

        if error:
            callback(False)
        else:
            callback(True)

    @gen.engine
    def create(self, callback):
        session = Session()
        table_data = {
            "TableName": self.name,
            "KeySchema": self._get_keyschema(),
            "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 10}
        }

        response, error = yield gen.Task(session.make_request, action='CreateTable', body=json.dumps(table_data))

        callback(response, error)

    @gen.engine
    def drop(self, callback):
        session = Session()
        table_data = {
            "TableName": self.name,
        }

        response, error = yield gen.Task(session.make_request, action='DeleteTable', body=json.dumps(table_data))
        callback(response[0])

    @gen.engine
    def put_item(self, item, callback):
        session = Session()

        response, error = yield gen.Task(session.put_item, self.name, item)

        if error and error['error'] and 'resource not found' in error['error'].reason:
            yield gen.Task(self.create)
            response, error = yield gen.Task(session.put_item, self.name, item)

        callback(response[0])

    @gen.engine
    def get_item(self, item, callback):
        session = Session()

        response, error = yield gen.Task(session.get_item, self.name, item)

        if error and error['error'] and 'resource not found' in error['error'].reason:
            yield gen.Task(self.create)
            response, error = yield gen.Task(session.get_item, self.name, item)

        callback(response[0])

    @gen.engine
    def query(self, callback=None, *args, **kwargs):
        session = Session()

        response, error = yield gen.Task(session.query, self.name, *args, **kwargs)

        if error and error['error'] and 'resource not found' in error['error'].reason:
            yield gen.Task(self.create)
            response, error = yield gen.Task(session.query, self.name, *args, **kwargs)

        callback(response[0])
