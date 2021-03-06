#!/usr/bin/python
# -*- coding: utf-8 -*-
"""The ORM module defining the SQL model for dispatcher k8s."""
import json
import uuid
from datetime import datetime
from peewee import Model, CharField, TextField, DateTimeField, UUIDField
from .dispatcher import DB, ReceiveTaskModel


class ScriptLogEncoder(json.JSONEncoder):
    """Json Encoder for the ScriptLog object."""

    def default(self, o):
        """Default method to encode a ScriptLog object."""
        if isinstance(o, uuid.UUID):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


def database_setup():
    """Setup the database."""
    ScriptLog.database_setup()
    DB.create_tables((ReceiveTaskModel,))


class ScriptLog(Model):
    """Example saving some name data."""

    uuid = UUIDField(primary_key=True, default=uuid.uuid4, index=True)
    event = TextField(index=False)
    stdout = TextField(index=False, null=True)
    stderr = TextField(index=False, null=True)
    return_code = TextField(index=True, null=True)
    script_id = CharField(index=True)
    created = DateTimeField(default=datetime.now, index=True)
    updated = DateTimeField(default=datetime.now, index=True)
    deleted = DateTimeField(null=True, index=True)

    # pylint: disable=too-few-public-methods
    class Meta:
        """The meta class that contains db connection."""

        database = DB
    # pylint: enable=too-few-public-methods

    @classmethod
    def database_setup(cls):
        """Setup the database by creating all tables."""
        if not cls.table_exists():
            cls.create_table()

    @classmethod
    def connect(cls):
        """Connect to the database."""
        # pylint: disable=no-member
        cls._meta.database.connect(True)
        # pylint: enable=no-member

    @classmethod
    def close(cls):
        """Close the connection to the database."""
        # pylint: disable=no-member
        cls._meta.database.close()
        # pylint: enable=no-member

    @classmethod
    def atomic(cls):
        """Do the database atomic action."""
        # pylint: disable=no-member
        return cls._meta.database.atomic()
        # pylint: enable=no-member
