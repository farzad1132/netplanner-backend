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
                        nullable= False,
                        unique= True)
    data = db.Column("data", JSON, nullable= False)
    projects = db.relationship( "ProjectModel",
                                back_populates= "PT")
    user_id = db.Column(db.Integer, 
                        db.ForeignKey("User.id"))
    user = db.relationship( "UserModel",
                            back_populates= "PTs")
    
    create_date = db.Column(db.DateTime, 
                            default=datetime.utcnow, 
                            onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"PT(id= {self.id}, name= {self.name})"

class TrafficMatrixModel(db.Model):
    __tablename__ = "TrafficMatrix"
    __table_args__ = {'extend_existing': True}
    id = db.Column( "id", 
                    db.Integer, primary_key= True)
    name = db.Column(   "name", 
                        db.String,
                        nullable= False,
                        unique= True)
    data = db.Column(   "data", 
                        JSON, nullable= False)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey("User.id"))
    user = db.relationship( "UserModel",
                            back_populates= "TMs")
    projects = db.relationship( "ProjectModel",
                                back_populates= "TM")
    
    create_date = db.Column(db.DateTime, 
                            default=datetime.utcnow, 
                            onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"TM(id= {self.id}, name= {self.name})"

class UserModel(db.Model):
    __tablename__ = "User"
    __table_args__ = {'extend_existing': True}
    id = db.Column( "id", 
                    db.Integer, 
                    primary_key= True)
    name = db.Column(   "name", 
                        db.String, 
                        nullable= False,
                        unique= True)
    projects = db.relationship( "ProjectModel",
                                back_populates= "user")

    TMs = db.relationship( "TrafficMatrixModel",
                            back_populates= "user")
    
    PTs = db.relationship( "PhysicalTopologyModel",
                            back_populates= "user")
    
    create_date = db.Column(db.DateTime, 
                            default=datetime.utcnow, 
                            onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"USER(name= {self.name})"

class ProjectModel(db.Model):
    __tablename__ = "Project"
    __table_args__ = {'extend_existing': True}
    id = db.Column( "id", 
                    db.Integer, 
                    primary_key= True)
    name = db.Column(   "name", 
                        db.String, 
                        nullable= False,
                        unique= True)
    create_date = db.Column(db.DateTime, 
                            default=datetime.utcnow, 
                            onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey("User.id"))
    tm_id = db.Column(  db.Integer, 
                        db.ForeignKey("TrafficMatrix.id"))
    pt_id = db.Column(  db.Integer, 
                        db.ForeignKey("PhysicalTopology.id"))

    user = db.relationship( "UserModel",
                            back_populates= "projects") 
    TM = db.relationship(   "TrafficMatrixModel",
                            back_populates= "projects") 
    PT = db.relationship(   "PhysicalTopologyModel",
                            back_populates= "projects")

    def __repr__(self):
        return f"PROJECT(name= {self.name}, username= {self.user.name}, PT name={self.PT.name}, TM name={self.TM.name})" 


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
    tm_id = fields.Int()
    pt_id = fields.Int()

class ProjectSchema(ma.Schema):
    class Meta:
        model = ProjectModel
        sqla_session = db.session