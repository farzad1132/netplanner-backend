from config import db, ma
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from marshmallow import fields
import uuid
from flask_sqlalchemy import BaseQuery

class QueryWithSoftDelete(BaseQuery):
    _with_deleted = False

    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        obj._with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(is_deleted=False) if not obj._with_deleted else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(db.class_mapper(self._mapper_zero().class_),
                              session=db.session(), _with_deleted=True)

class PhysicalTopologyModel(db.Model):
    __tablename__ = "PhysicalTopology"
    __table_args__ = {'extend_existing': True}
    query_class = QueryWithSoftDelete

    primary_id = db.Column("primary_id", db.String, primary_key= True, default=lambda: uuid.uuid4().hex)
    id = db.Column("id", db.String, nullable=False)
    name = db.Column("name", db.String, nullable= False)
    data = db.Column("data", JSON, nullable= False)
    projects = db.relationship( "ProjectModel", back_populates= "physical_topology")
    owner_id = db.Column(db.String, db.ForeignKey("User.id"))
    owner = db.relationship( "UserModel", back_populates= "physical_topologies")
    create_date = db.Column(db.DateTime, default=datetime.utcnow, 
                            onupdate=datetime.utcnow)
    comment = db.Column("comment", db.String, nullable=False)
    version = db.Column("version", db.Integer, nullable=False)
    is_deleted = db.Column("is_deleted", db.Boolean, nullable=False, default=False)
    #clusters = db.relationship("ClusterModel", back_populates= "physical_topology") 
    
    def __repr__(self):
        return f"PT(id= {self.id}, version= {self.version}, name= {self.name})"

class TrafficMatrixModel(db.Model):
    __tablename__ = "TrafficMatrix"
    __table_args__ = {'extend_existing': True}
    query_class = QueryWithSoftDelete

    primary_id = db.Column( "primary_id", db.String, primary_key= True, default=lambda: uuid.uuid4().hex)
    id = db.Column("id", db.String, nullable=False)
    name = db.Column("name", db.String, nullable= False)
    data = db.Column("data", JSON, nullable= False)
    owner_id = db.Column(db.String, db.ForeignKey("User.id"))
    owner = db.relationship( "UserModel", back_populates= "traffic_matrices")
    projects = db.relationship( "ProjectModel", back_populates= "traffic_matrix")
    create_date = db.Column(db.DateTime, default=datetime.utcnow, 
                            onupdate=datetime.utcnow)
    comment = db.Column("comment", db.String, nullable=False)
    version = db.Column("version", db.Integer, nullable=False)
    is_deleted = db.Column("is_deleted", db.Boolean, nullable=False, default=False)
    
    def __repr__(self):
        return f"TM(id= {self.id}, version= {self.version} name= {self.name})"

class UserModel(db.Model):
    __tablename__ = "User"
    __table_args__ = {'extend_existing': True}
    query_class = QueryWithSoftDelete

    id = db.Column( "id", db.String, primary_key= True, default=lambda: uuid.uuid4().hex)
    username = db.Column("username", db.String, nullable=False, unique=True)
    password = db.Column("password", db.String, nullable=False)
    email = db.Column("email", db.String, nullable=False, unique=True)
    projects = db.relationship("ProjectModel", back_populates= "owner")
    traffic_matrices = db.relationship( "TrafficMatrixModel", back_populates= "owner")
    physical_topologies = db.relationship( "PhysicalTopologyModel", back_populates= "owner")
    create_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    shared_pts = db.relationship( "PhysicalTopologyUsersModel", back_populates= "user")
    shared_tms = db.relationship( "TrafficMatrixUsersModel", back_populates= "user")
    shared_projects = db.relationship( "ProjectUsersModel", back_populates= "user")
    role = db.Column("role", db.String, nullable= False)
    is_deleted = db.Column("is_deleted", db.Boolean, nullable=False, default=False)
    
    def __repr__(self):
        return f"USER(name= {self.username})"

class ProjectModel(db.Model):
    __tablename__ = "Project"
    __table_args__ = {'extend_existing': True}
    query_class = QueryWithSoftDelete

    id = db.Column( "id", db.String, primary_key= True, default=lambda: uuid.uuid4().hex)
    name = db.Column("name", db.String, nullable= False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = db.Column(db.String, db.ForeignKey("User.id"))
    tm_id = db.Column(db.String, db.ForeignKey("TrafficMatrix.primary_id"))
    pt_id = db.Column(db.String, db.ForeignKey("PhysicalTopology.primary_id"))
    owner = db.relationship("UserModel", back_populates= "projects") 
    traffic_matrix = db.relationship("TrafficMatrixModel", back_populates= "projects") 
    physical_topology = db.relationship("PhysicalTopologyModel", back_populates= "projects")
    current_pt_version = db.Column("current_pt_version", db.Integer, nullable=False)
    current_tm_version = db.Column("current_tm_version", db.Integer, nullable=False)
    clusters = db.relationship("ClusterModel", back_populates= "project")
    shared_users = db.relationship("ProjectUsersModel", back_populates= "project")
    is_deleted = db.Column("is_deleted", db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"PROJECT(name= {self.name}, username= {self.user.name}, PT name={self.physical_topologies.name}, TM name={self.traffic_matrix.name})"

class ProjectUsersModel(db.Model):
    # this model is used to give other users access to project
    __tablename__ = "ProjectUsers"
    __table_args__ = {'extend_existing': True}
    query_class = QueryWithSoftDelete

    id = db.Column( "id", db.String, primary_key= True, default=lambda: uuid.uuid4().hex)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.String, db.ForeignKey("User.id"))
    user = db.relationship("UserModel", back_populates= "shared_projects")
    project_id = db.Column(db.String, db.ForeignKey("Project.id"))
    project = db.relationship("ProjectModel", back_populates= "shared_users")
    is_deleted = db.Column("is_deleted", db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"user_id= {self.user_id}, project_id= {self.project_id}"

class PhysicalTopologyUsersModel(db.Model):
    # this model is used to give other users access to physical topology
    # NOTE: for pt_id we didn't use foreignkey because 'id' in physical topology is not unique (multiple
    #       versions have same id)
    __tablename__ = "PhysicalTopologyUsers"
    __table_args__ = {'extend_existing': True}
    query_class = QueryWithSoftDelete

    id = id = db.Column("id", db.String, primary_key= True, default=lambda: uuid.uuid4().hex)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.String, db.ForeignKey("User.id"))
    pt_id = db.Column("pt_id", db.String, nullable= False)
    user = db.relationship("UserModel", back_populates= "shared_pts")
    is_deleted = db.Column("is_deleted", db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"user_id= {self.user_id}, pt_id= {self.pt_id}"

class TrafficMatrixUsersModel(db.Model):
    # this model is used to give other users access to traffic matrix
    # NOTE: for tm_id we didn't use foreignkey because 'id' in traffic matrix is not unique (multiple
    #       versions have same id)
    __tablename__ = "TrafficMatrixUsers"
    __table_args__ = {'extend_existing': True}
    query_class = QueryWithSoftDelete

    id = id = db.Column("id", db.String, primary_key= True, default=lambda: uuid.uuid4().hex)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.String, db.ForeignKey("User.id"))
    tm_id = db.Column("tm_id", db.String, nullable= False)
    user = db.relationship("UserModel", back_populates= "shared_tms")
    is_deleted = db.Column("is_deleted", db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"user_id= {self.user_id}, tm_id= {self.tm_id}"

class ClusterModel(db.Model):
    __tablename__ = "Cluster"
    __table_args__ = {'extend_existing': True}
    query_class = QueryWithSoftDelete

    id = db.Column( "id", db.String, primary_key= True, default=lambda: uuid.uuid4().hex)
    name = db.Column("name", db.String, nullable= False)
    data = db.Column("data", JSON, nullable= False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    pt_id = db.Column("pt_id", db.String, nullable= False)
    pt_version = db.Column("pt_version", db.Integer, nullable=False)
    #physical_topology = db.relationship("PhysicalTopologyModel", back_populates= "clusters")
    project_id = db.Column(db.String, db.ForeignKey("Project.id"))
    project = db.relationship("ProjectModel", back_populates= "clusters")
    is_deleted = db.Column("is_deleted", db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"id= {self.id}, project_id= {self.project_id}, name= {self.name}"


class ClusterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ClusterModel
        sqla_session = db.session
        include_fk = True

class PhysicalTopologySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PhysicalTopologyModel
        sqla_session = db.session
        include_fk = True

class TrafficMatrixSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrafficMatrixModel
        sqla_session = db.session
        include_fk = True

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        sqla_session = db.session
        include_fk = True
    
    projects = fields.Nested("UserProjectSchema", default=[], many= True)

class UserProjectSchema(ma.Schema):
    id = fields.Int()
    name = fields.Str()
    create_date = fields.DateTime()
    user_id = fields.Int()
    tm_id = fields.Int()
    pt_id = fields.Int()

class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProjectModel
        sqla_session = db.session
        include_fk = True