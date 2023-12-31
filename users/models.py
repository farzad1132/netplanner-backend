"""
    This module contains some of user related models
"""

import datetime

from database import base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime


class UserRegisterModel(base):
    """
        This model used at user registration process
    """

    __tablename__ = "UserRegister"
    __table_args__ = {'extend_existing': True}

    id = Column("id", Integer, primary_key=True)
    username = Column("username", String, nullable=False, unique=True)
    password = Column("password", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True)
    create_date = Column("create_date", DateTime,
                         default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"UserRegister(username= {self.username})"
