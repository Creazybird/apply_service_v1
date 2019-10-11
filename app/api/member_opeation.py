#coding:utf-8
import json
from . import api
from .. import db
from ..models import Project, Applicant
from flask import jsonify, request

@api.route('/project/posting/cache/member/', methods = ['GET'])
@Applicant.check
def get_members(aid):
    if request.method == 'GET':
        applicant = Applicant.query.filter_by(id=aid).first()
        if applicant.posting:
            project = Project.query.filter_by(id=applicant.posting_project_id).first()
            if project == None:
                return jsonify({"msg": "project is inexistent"}), 404
            if project.member_list == None:
                return jsonify({'msg':'member_list is empty'}), 404
            member_list = eval(project.member_list)
            return member_list, 200


@api.route('/project/member/edit/', methods = ['POST'])
@Applicant.check
def edit_members(aid):
    if request.method == "POST":
        applicant = Applicant.query.filter_by(id=aid).first()
        if applicant.posting:
            pid = applicant.posting_project_id
            member_json = request.get_json()
            project = Project.query.filter_by(id=pid).first()
            if project != None:
                project.member_list = str(member_json)
                db.session.add(project)
                db.session.commit()
                return jsonify({"msg":"edit member successful"}),200
            else:
                return jsonify({"msg":"project is inexistent "}), 404


