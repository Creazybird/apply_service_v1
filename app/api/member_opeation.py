#coding:utf-8
import json
from . import api
from ...app import db
from ...app.models import Project
from flask import jsonify, request

@api.route('/project/member/get', methods = ['GET'])

def get_members(pid):
    if request.method == 'GET':
        project = Project.query.filter_by(id=pid).first()
        if project != None:
            member_list = json.load(project.member_list)
            return member_list, 200
        else:
            return jsonify({"msg":"project is inexistent"}), 404


@api.route('/project/member/edit', methods = ['POST'])
def get_members(pid):
    if request.method == "POST":
        member_json = request.get_json()
        project = Project.query.filter_by(id=pid).first()
        if project != None:
            project.member_list = str(member_json)
            db.session.add(project)
            db.session.commit()
            return jsonify({"msg":"edit member successful"}),200
        else:
            return jsonify({"msg":"project is inexistent "}), 404


