from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
import uuid
from sqlalchemy.orm import relationship
from database import base
from sqlalchemy import Boolean, Integer, String, ForeignKey, Column, DateTime, Float

class GroomingRegisterModel(base):
    __tablename__ = "GroomingRegister"
    __table_args__ = {'extend_existing': True}

    # generall information
    id = Column("id", String, primary_key=True)
    project_id = Column("project_id", String, nullable=False)
    pt_id = Column("pt_id", String, nullable=False)
    tm_id = Column("tm_id", String, nullable=False)
    pt_version = Column("pt_version", Integer, nullable=False)
    tm_version = Column("tm_version", Integer, nullable=False)
    form = Column("form", JSON, nullable=False)
    manager_id = Column(String, ForeignKey("User.id"))
    manager = relationship("UserModel", back_populates="grooming_registers")
    start_date = Column(DateTime, default=datetime.utcnow)
    with_clustering = Column("with_clustering", Boolean, nullable=False)
    clusters = Column("clusters", JSON)
    is_failed = Column("is_failed", Boolean, nullable=False, default=False)
    exception = Column("exception", String)
    is_finished = Column("is_finished", Boolean, nullable=False, default=False)
    is_deleted = Column("is_deleted", Boolean, nullable=False, default=False)

class GroomingModel(base):
    __tablename__ = "Grooming"
    __table_args__ = {'extend_existing': True}

    # generall information
    id = Column("id", String, primary_key=True)
    project_id = Column("project_id", String, nullable=False)
    pt_id = Column("pt_id", String, nullable=False)
    tm_id = Column("tm_id", String, nullable=False)
    pt_version = Column("pt_version", Integer, nullable=False)
    tm_version = Column("tm_version", Integer, nullable=False)
    form = Column("form", JSON, nullable=False)
    manager_id = Column(String, ForeignKey("User.id"))
    manager = relationship("UserModel", back_populates="grooming_algorithms")
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    with_clustering = Column("with_clustering", Boolean, nullable=False)
    clusters = Column("clusters", JSON)
    is_finished = Column("is_finished", Boolean, nullable=False, default=False)
    is_deleted = Column("is_deleted", Boolean, nullable=False, default=False)

    # actual result
    traffic = Column("traffic", JSON, nullable=False)
    service_devices = Column("service_devices", JSON, nullable=False)
    clustered_tms = Column("clustered_tms", JSON)
    service_mapping = Column("service_mapping", JSON)

    def __repr__(self):
        return  f"Grooming(id={self.id}, pt_id={self.pt_id}, tm_id={self.tm_id},"\
                f" pt_version={self.pt_version}, tm_version={self.tm_version}, manager_id={self.manager_id})"

class AdvGroomingModel(base):
    __tablename__ = "AdvGrooming"
    __table_args__ = {'extend_existing': True}

    # generall information
    id = Column("id", String, primary_key=True)
    project_id = Column("project_id", String, nullable=False)
    pt_id = Column("pt_id", String, nullable=False)
    tm_id = Column("tm_id", String, nullable=False)
    pt_version = Column("pt_version", Integer, nullable=False)
    tm_version = Column("tm_version", Integer, nullable=False)
    form = Column("form", JSON, nullable=False)
    manager_id = Column(String, ForeignKey("User.id"))
    manager = relationship("UserModel", back_populates="grooming_algorithms")
    with_clustering = Column("with_clustering", Boolean, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_finished = Column("is_finished", Boolean, nullable=False, default=False)
    is_deleted = Column("is_deleted", Boolean, nullable=False, default=False)

    # actual result
    connections = Column("connections", JSON, nullable=False)
    lambda_link = Column("lambda_link", Integer, nullable=False)
    average_lambda_capacity_usage = Column("average_lambda_capacity_usage", Float, nullable=False)
    lightpaths = Column("lightpaths", JSON, nullable=False)