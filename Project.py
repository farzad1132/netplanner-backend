from flask import abort, request
import json
from config import db
from models import ProjectModel, ProjectSchema

def read_Project(Id, UserId):
    print("get method")


def create_Project(TM_Id, PT_Id, Clusters_Id, UserId):
    print("post method")

def update_Project(Id, UserId):
    print("put method")

def delete_Project(Id, UserId):
    print("delete method")