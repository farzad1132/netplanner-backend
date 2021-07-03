"""
    This schema contains RWA related models
"""

from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from sqlalchemy.orm import relationship
from database import base
from sqlalchemy import Boolean, Integer, String, ForeignKey, Column, DateTime

class RWARegisterModel(base):
    """
        RWA Registration model

        After a user attempts to start rwa algorithm this models is used to store initial information of
        algorithm into database (used before running algorithm)
    """
    __tablename__ = "RWARegister"
    __table_args__ = {'extend_existing': True}

    # generall information
    id = Column("id", String, primary_key=True)
    project_id = Column("project_id", String, nullable=False)
    grooming_id = Column("grooming_id", String, nullable=False)
    pt_id = Column("pt_id", String, nullable=False)
    tm_id = Column("tm_id", String, nullable=False)
    pt_version = Column("pt_version", Integer, nullable=False)
    tm_version = Column("tm_version", Integer, nullable=False)
    manager_id = Column(String, ForeignKey("User.id"))
    manager = relationship("UserModel", back_populates="rwa_registers")
    start_date = Column(DateTime, default=datetime.utcnow)
    form = Column("form", JSON, nullable=False)
    is_failed = Column("is_failed", Boolean, nullable=False, default=False)
    exception = Column("exception", String)
    is_finished = Column("is_finished", Boolean, nullable=False, default=False)
    is_deleted = Column("is_deleted", Boolean, nullable=False, default=False)

class RWAModel(base):
    """
        RWA result model

        This models is used after rwa result has been calculated and stores result into database
    """
    __tablename__ = "RWA"
    __table_args__ = {'extend_existing': True}

    # generall information
    id = Column("id", String, primary_key=True)
    project_id = Column("project_id", String, nullable=False)
    grooming_id = Column("grooming_id", String, nullable=False)
    pt_id = Column("pt_id", String, nullable=False)
    tm_id = Column("tm_id", String, nullable=False)
    pt_version = Column("pt_version", Integer, nullable=False)
    tm_version = Column("tm_version", Integer, nullable=False)
    manager_id = Column(String, ForeignKey("User.id"))
    manager = relationship("UserModel", back_populates="rwa_algorithms")
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, default=datetime.utcnow)
    form = Column("form", JSON, nullable=False)
    is_failed = Column("is_failed", Boolean, nullable=False, default=False)
    exception = Column("exception", String)
    is_finished = Column("is_finished", Boolean, nullable=False, default=False)
    is_deleted = Column("is_deleted", Boolean, nullable=False, default=False)

    # actual result
    lightpaths = Column("lightpaths", JSON, nullable=False)

    def __repr__(self):
        return  f"RWA(id={self.id}, grooming_id={self.grooming_id}, pt_id={self.pt_id}, tm_id={self.tm_id},"\
                f" pt_version={self.pt_version}, tm_version={self.tm_version}, manager_id={self.manager_id})"