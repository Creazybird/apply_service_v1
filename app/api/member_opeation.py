#coding:utf-8
import json
from . import api
from ...app import db
from ...app.models import Project, Applicant
from flask import jsonify, request

@api.route('/project/<int:pid>/member/get', methods = ['GET'])
@Applicant.check
def get_members(aid, pid):
    if request.method == 'GET':
        project = Project.query.filter_by(id=pid).first()
        if project != None:
            member_list = eval(project.member_list)
            return member_list, 200
        else:
            return jsonify({"msg":"project is inexistent"}), 404


@api.route('/project/<int:pid>/member/edit', methods = ['POST'])
@Applicant.check
def edit_members(aid, pid):
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


