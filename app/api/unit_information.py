#coding:utf-8

from . import api
from .. import db
from ..models import Project, Applicant
from flask import jsonify, request


@api.route('/project/posting/cache/unit/', methods = ['GET'])
@Applicant.check
def get_information(aid):
    if request.method == 'GET':
        applicant = Applicant.query.filter_by(id=aid).first()
        if applicant.posting:
            project = Project.query.filter_by(id=applicant.posting_project_id).first()
            if project == None:
                return jsonify({"msg": "project is inexistent"}), 404
            one_unit = {
                'work_unit':project.work_unit,
                'unit_linkman':project.unit_linkman,
                'unit_linkman_email':project.unit_linkman_email,
                'unit_linkman_tel':project.unit_linkman_tel,
                'academy_linkman':project.academy_linkman,
                'academy_linkman_email':project.academy_linkman_email,
                'academy_linkman_tel':project.academy_linkman_tel,
                'pid':project.id
            }
            return jsonify({'information':one_unit}),200



@api.route('/project/<int:pid>/unit/add/', methods = ['POST'])
@Applicant.check
def add_information(aid, pid):
    if request.method == 'POST':
        project = Project.query.filter_by(id=pid).first()
        if project == None:
            return jsonify({"msg": "project is inexistent"}), 404
        project.work_unit = request.get_json().get('work_unit')
        project.unit_linkman = request.get_json().get('unit_linkman')
        project.unit_linkman_email = request.get_json().get('unit_linkman_email')
        project.unit_linkman_tel =request.get_json().get('unit_linkman_tel')
        project.academy_linkman = request.get_json().get('academy_linkman')
        project.academy_linkman_email = request.get_json().get('academy_linkman_email')
        project.academy_linkman_tel = request.get_json().get('academy_linkman_tel')
        db.session.add(project)
        db.session.commit()
        return jsonify({'msg':'unit imformation add successful'})



