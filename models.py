from config import db, ma
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from marshmallow import fields
import uuid


class PhysicalTopologyModel(db.Model):
    __tablename__ = "PhysicalTopology"
    __table_args__ = {'extend_existing': True}

    primary_id = db.Column("primary_id", db.String, primary_key= True, default=lambda: uuid.uuid4().hex)
    id = db.Column("id", db.String, nullable=False)
    name = db.Column("name", db.String, nullable= False)
    data = db.Column("data", JSON, nullable= False)
    projects = db.relationship( "ProjectModel", back_populates= "physical_topology")
    user_id = db.Column(db.String, db.ForeignKey("User.id"))
    user = db.relationship( "UserModel", back_populates= "physical_topologies")
    create_date = db.Column(db.DateTime, default=datetime.utcnow, 
                            onupdate=datetime.utcnow)
    comment = db.Column("comment", db.String, nullable=False)
    version = db.Column("version", db.Integer, nullable=False)
    
    def __repr__(self):
        return f"PT(id= {self.id}, version= {self.version}, name= {self.name})"

class TrafficMatrixModel(db.Model):
    __tablename__ = "TrafficMatrix"
    __table_args__ = {'extend_existing': True}

    primary_id = db.Column( "primary_id", db.String, primary_key= True, default=lambda: uuid.uuid4().hex)
    id = db.Column("id", db.String, nullable=False)
    name = db.Column("name", db.String, nullable= False)
    data = db.Column("data", JSON, nullable= False)
    user_id = db.Column(db.String, db.ForeignKey("User.id"))
    user = db.relationship( "UserModel", back_populates= "traffic_matrices")
    projects = db.relationship( "ProjectModel", back_populates= "traffic_matrix")
    create_date = db.Column(db.DateTime, default=datetime.utcnow, 
                            onupdate=datetime.utcnow)
    comment = db.Column("comment", db.String, nullable=False)
    version = db.Column("version", db.Integer, nullable=False)
    
    def __repr__(self):
        return f"TM(id= {self.id}, version= {self.version} name= {self.name})"

class UserModel(db.Model):
    __tablename__ = "User"
    __table_args__ = {'extend_existing': True}

    id = db.Column( "id", db.String, primary_key= True, default=lambda: uuid.uuid4().hex)
    username = db.Column("username", db.String, nullable= False, unique= True)
    password = db.Column("password", db.String, nullable= False)
    projects = db.relationship("ProjectModel", back_populates= "user")
    traffic_matrices = db.relationship( "TrafficMatrixModel", back_populates= "user")
    physical_topologies = db.relationship( "PhysicalTopologyModel", back_populates= "user")
    create_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    role = db.Column("role", db.String, nullable= False)
    
    def __repr__(self):
        return f"USER(name= {self.username})"

class ProjectModel(db.Model):
    __tablename__ = "Project"
    __table_args__ = {'extend_existing': True}

    id = db.Column( "id", db.String, primary_key= True, default=lambda: uuid.uuid4().hex)
    name = db.Column("name", db.String, nullable= False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.String, db.ForeignKey("User.id"))
    tm_id = db.Column(db.String, db.ForeignKey("TrafficMatrix.primary_id"))
    pt_id = db.Column(db.String, db.ForeignKey("PhysicalTopology.primary_id"))
    user = db.relationship("UserModel", back_populates= "projects") 
    traffic_matrix = db.relationship("TrafficMatrixModel", back_populates= "projects") 
    physical_topology = db.relationship("PhysicalTopologyModel", back_populates= "projects")
    current_pt_version = db.Column("current_pt_version", db.Integer, nullable=False)
    current_tm_version = db.Column("current_tm_version", db.Integer, nullable=False)
    clusters = db.relationship("ClusterModel", back_populates= "project") 

    def __repr__(self):
        return f"PROJECT(name= {self.name}, username= {self.user.name}, PT name={self.physical_topologies.name}, TM name={self.traffic_matrix.name})"

class ClusterModel(db.Model):
    __tablename__ = "Cluster"
    __table_args__ = {'extend_existing': True}

    id = db.Column( "id", db.String, primary_key= True, default=lambda: uuid.uuid4().hex)
    name = db.Column("name", db.String, nullable= False)
    data = db.Column("data", JSON, nullable= False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    project_id = db.Column(db.String, db.ForeignKey("Project.id"))
    project = db.relationship("ProjectModel", back_populates= "clusters")

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