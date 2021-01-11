from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
import uuid
from sqlalchemy.orm import relationship
from database import base
from sqlalchemy import Boolean, Integer, String, ForeignKey, Column, DateTime

class PhysicalTopologyModel(base):
    __tablename__ = "PhysicalTopology"
    __table_args__ = {'extend_existing': True}
    

    primary_id = Column("primary_id", String, primary_key= True, default=lambda: uuid.uuid4().hex)
    id = Column("id", String, nullable=False)
    name = Column("name", String, nullable= False)
    data = Column("data", JSON, nullable= False)
    projects = relationship( "ProjectModel", back_populates= "physical_topology")
    owner_id = Column(String, ForeignKey("User.id"))
    owner = relationship( "UserModel", back_populates= "physical_topologies")
    create_date = Column(DateTime, default=datetime.utcnow, 
                            onupdate=datetime.utcnow)
    comment = Column("comment", String, nullable=False)
    version = Column("version", Integer, nullable=False)
    is_deleted = Column("is_deleted", Boolean, nullable=False, default=False)
    #clusters = relationship("ClusterModel", back_populates= "physical_topology") 
    
    def __repr__(self):
        return f"PT(id= {self.id}, version= {self.version}, name= {self.name})"

class TrafficMatrixModel(base):
    __tablename__ = "TrafficMatrix"
    __table_args__ = {'extend_existing': True}
    

    primary_id = Column( "primary_id", String, primary_key= True, default=lambda: uuid.uuid4().hex)
    id = Column("id", String, nullable=False)
    name = Column("name", String, nullable= False)
    data = Column("data", JSON, nullable= False)
    owner_id = Column(String, ForeignKey("User.id"))
    owner = relationship( "UserModel", back_populates= "traffic_matrices")
    projects = relationship( "ProjectModel", back_populates= "traffic_matrix")
    create_date = Column(DateTime, default=datetime.utcnow, 
                            onupdate=datetime.utcnow)
    comment = Column("comment", String, nullable=False)
    version = Column("version", Integer, nullable=False)
    is_deleted = Column("is_deleted", Boolean, nullable=False, default=False)
    
    def __repr__(self):
        return f"TM(id= {self.id}, version= {self.version} name= {self.name})"

class UserModel(base):
    __tablename__ = "User"
    __table_args__ = {'extend_existing': True}
    

    id = Column( "id", String, primary_key= True, default=lambda: uuid.uuid4().hex)
    username = Column("username", String, nullable=False, unique=True)
    password = Column("password", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True)
    projects = relationship("ProjectModel", back_populates= "owner")
    traffic_matrices = relationship( "TrafficMatrixModel", back_populates= "owner")
    physical_topologies = relationship( "PhysicalTopologyModel", back_populates= "owner")
    create_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    shared_pts = relationship( "PhysicalTopologyUsersModel", back_populates= "user")
    shared_tms = relationship( "TrafficMatrixUsersModel", back_populates= "user")
    shared_projects = relationship( "ProjectUsersModel", back_populates= "user")
    role = Column("role", String, nullable= False)
    is_deleted = Column("is_deleted", Boolean, nullable=False, default=False)
    
    def __repr__(self):
        return f"USER(name= {self.username})"

class ProjectModel(base):
    __tablename__ = "Project"
    __table_args__ = {'extend_existing': True}
    

    id = Column( "id", String, primary_key= True, default=lambda: uuid.uuid4().hex)
    name = Column("name", String, nullable= False)
    create_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = Column(String, ForeignKey("User.id"))
    tm_id = Column(String, ForeignKey("TrafficMatrix.primary_id"))
    pt_id = Column(String, ForeignKey("PhysicalTopology.primary_id"))
    owner = relationship("UserModel", back_populates= "projects") 
    traffic_matrix = relationship("TrafficMatrixModel", back_populates= "projects") 
    physical_topology = relationship("PhysicalTopologyModel", back_populates= "projects")
    current_pt_version = Column("current_pt_version", Integer, nullable=False)
    current_tm_version = Column("current_tm_version", Integer, nullable=False)
    clusters = relationship("ClusterModel", back_populates= "project")
    shared_users = relationship("ProjectUsersModel", back_populates= "project")
    is_deleted = Column("is_deleted", Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"PROJECT(name= {self.name}, username= {self.owner.name}, PT name={self.physical_topology.name}, TM name={self.traffic_matrix.name})"

class ProjectUsersModel(base):
    # this model is used to give other users access to project
    __tablename__ = "ProjectUsers"
    __table_args__ = {'extend_existing': True}
    

    id = Column( "id", String, primary_key= True, default=lambda: uuid.uuid4().hex)
    create_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(String, ForeignKey("User.id"))
    user = relationship("UserModel", back_populates= "shared_projects")
    project_id = Column(String, ForeignKey("Project.id"))
    project = relationship("ProjectModel", back_populates= "shared_users")
    is_deleted = Column("is_deleted", Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"user_id= {self.user_id}, project_id= {self.project_id}"

class PhysicalTopologyUsersModel(base):
    # this model is used to give other users access to physical topology
    # NOTE: for pt_id we didn't use foreignkey because 'id' in physical topology is not unique (multiple
    #       versions have same id)
    __tablename__ = "PhysicalTopologyUsers"
    __table_args__ = {'extend_existing': True}
    

    id = id = Column("id", String, primary_key= True, default=lambda: uuid.uuid4().hex)
    create_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(String, ForeignKey("User.id"))
    pt_id = Column("pt_id", String, nullable= False)
    user = relationship("UserModel", back_populates= "shared_pts")
    is_deleted = Column("is_deleted", Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"user_id= {self.user_id}, pt_id= {self.pt_id}"

class TrafficMatrixUsersModel(base):
    # this model is used to give other users access to traffic matrix
    # NOTE: for tm_id we didn't use foreignkey because 'id' in traffic matrix is not unique (multiple
    #       versions have same id)
    __tablename__ = "TrafficMatrixUsers"
    __table_args__ = {'extend_existing': True}
    

    id = id = Column("id", String, primary_key= True, default=lambda: uuid.uuid4().hex)
    create_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(String, ForeignKey("User.id"))
    tm_id = Column("tm_id", String, nullable= False)
    user = relationship("UserModel", back_populates= "shared_tms")
    is_deleted = Column("is_deleted", Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"user_id= {self.user_id}, tm_id= {self.tm_id}"

class ClusterModel(base):
    __tablename__ = "Cluster"
    __table_args__ = {'extend_existing': True}
    

    id = Column( "id", String, primary_key= True, default=lambda: uuid.uuid4().hex)
    name = Column("name", String, nullable= False)
    data = Column("data", JSON, nullable= False)
    create_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    pt_id = Column("pt_id", String, nullable= False)
    pt_version = Column("pt_version", Integer, nullable=False)
    #physical_topology = relationship("PhysicalTopologyModel", back_populates= "clusters")
    project_id = Column(String, ForeignKey("Project.id"))
    project = relationship("ProjectModel", back_populates= "clusters")
    is_deleted = Column("is_deleted", Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"id= {self.id}, project_id= {self.project_id}, name= {self.name}"