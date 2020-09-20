from config import db, ma
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from marshmallow import fields


class PhysicalTopologyModel(db.Model):
    __tablename__ = "PhysicalTopology"
    __table_args__ = {'extend_existing': True}
    id = db.Column("id", db.Integer, 
                        primary_key= True)
    name = db.Column("name", db.String, 
                        nullable= False)
    data = db.Column("data", JSON, nullable= False)
    projects = db.relationship( "ProjectModel",
                                back_populates= "PT_id")

class TrafficMatrixModel(db.Model):
    __tablename__ = "TrafficMatrix"
    __table_args__ = {'extend_existing': True}
    id = db.Column( "id", 
                    db.Integer, primary_key= True)
    name = db.Column(   "name", 
                        db.String, nullable= False)
    data = db.Column(   "data", 
                        JSON, nullable= False)
    projects = db.relationship( "ProjectModel",
                                back_populates= "TM_id")

class UserModel(db.Model):
    __tablename__ = "User"
    __table_args__ = {'extend_existing': True}
    id = db.Column( "id", 
                    db.Integer, primary_key= True)
    name = db.Column(   "name", 
                        db.String, nullable= False)
    projects = db.relationship( "ProjectModel",
                                back_populates= "user")

class ProjectModel(db.Model):
    __tablename__ = "Project"
    __table_args__ = {'extend_existing': True}
    id = db.Column( "id", 
                    db.Integer, primary_key= True)
    name = db.Column(   "name", 
                        db.String, nullable= False)
    create_date = db.Column(db.DateTime, 
                            default=datetime.utcnow, 
                            onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey("User.id"))
    tm_id = db.Column(  db.Integer, 
                        db.ForeignKey("TrafficMatrix.id"))
    pt_id = db.Column(  db.Integer, 
                        db.ForeignKey("PhysicalTopology.id"))

    user = db.relationship(    "UserModel",
                                back_populates= "projects") 
    TM_id = db.relationship(    "TrafficMatrixModel",
                                back_populates= "projects") 
    PT_id = db.relationship(    "PhysicalTopologyModel",
                                back_populates= "projects") 


class PhysicalTopologySchema(ma.Schema):
    class Meta:
        model = PhysicalTopologyModel
        sqla_session = db.session

class TrafficMatrixSchema(ma.Schema):
    class Meta:
        model = TrafficMatrixModel
        sqla_session = db.session

class UserSchema(ma.Schema):
    class Meta:
        model = UserModel
        sqla_session = db.session
    
    projects = fields.Nested(   "User_ProjectSchema", 
                                default=[], many= True)

class User_ProjectSchema(ma.Schema):
    id = fields.Int()
    name = fields.Str()
    create_date = fields.DateTime()
    user_id = fields.Int()
    TM_id = fields.Int()
    PT_id = fields.Int()

class ProjectSchema(ma.Schema):
    class Meta:
        model = ProjectModel
        sqla_session = db.session