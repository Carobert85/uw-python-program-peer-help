"""This module creates our database for our program"""

import os
import peewee as pw
from loguru import logger

file = 'social_network.db'
if os.path.exists(file):
    os.remove(file)

db = pw.SqliteDatabase(file, pragmas={'foreign_keys': 1})


class BaseModel(pw.Model):
    """Base class that lets us define the database and Meta class in
    a single place
    """
    logger.info("Allows database to be changed in one place")

    class Meta:
        database = db


class Users(BaseModel):
    """Defines the Users table for our social media network
    """
    user_id = pw.CharField(primary_key=True, max_length=30)
    user_name = pw.CharField(max_length=30)
    user_last_name = pw.CharField(max_length=100)
    user_email = pw.CharField(unique=True)


class Status(BaseModel):
    """Defines the Status table for our social media network
    """
    status_id = pw.CharField(primary_key=True, max_length=30)
    user_id = pw.ForeignKeyField(Users, null=False)
    status_text = pw.TextField()


def create_model_tables():
    """Creates tables"""
    with db:
        db.create_tables([Users, Status])


def main():
    """Creates our database"""
    db.connect()
    # db.execute_sql('PRAGMA foreign keys = ON;')
    create_model_tables()


