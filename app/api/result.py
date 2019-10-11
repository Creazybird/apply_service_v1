#coding:utf-8
import json
import datetime
from . import api
from .. import db
from ..models import Project, Applicant, Result
from flask import jsonify, request

@api.route('/project/posting/cache/result/', methods = ['GET'])
@Applicant.check
def get_results(aid):
    if request.method == 'GET':
        applicant = Applicant.query.filter_by(id=aid).first()
        if applicant.posting:
            project = Project.query.filter_by(id=applicant.posting_project_id).first()
            if project == None:
                return jsonify({"msg": "project is inexistent"}), 404
            if project.result_index_list == None:
                return jsonify({'msg':'result_list is empty'}), 404
            project_results_list = Result.query.filter_by(project_id=applicant.posting_project_id).all()
            result_list = []
            if project_results_list == None:
                return jsonify({"result_list":result_list}), 200
            project_results_index_list = []
            for result in project_results_list:
                project_results_index_list.append(result.id)
            result_index_list = eval(project.result_index_list)
            one_result = {
                "id":"",
                "name":"",
                "type":"",
                "start":"",
                "end":"",
                "is_key": False,
                "undertakers":"",
                "participants": "",
            }
            for index in result_index_list:
                result_index = project_results_index_list.index(index)
                if result_index == -1:
                    return jsonify({"msg": "result is inexistent"}), 404
                result = project_results_list[result_index]
                one_result["id"] = result.id
                one_result["name"] = result.result_name
                one_result["type"] = result.result_type
                one_result["start"] = result.start_date
                one_result["end"] = result.end_date
                one_result["is_key"] = result.is_key
                one_result["undertakers"] = result.undertakers
                one_result["participants"] = result.participants
                result_list.append(one_result)
            return jsonify({"result_list":result_list}), 200


@api.route('/project/result/', methods = ['POST'])
@Applicant.check
def add_results(aid):
    if request.method == "POST":
        applicant = Applicant.query.filter_by(id=aid).first()
        pid = applicant.posting_project_id
        project = Project.query.filter_by(id=pid).first()
        if project == None:
            return jsonify({"msg": "project is inexistent"}), 404
        result_name = request.get_json().get('result_name')
        result_type = request.get_json().get('result_type')
        result_start = request.get_json().get('result_start')
        #result_start = datetime.datetime.strptime(result_start,"%Y-%m-%d")
        result_end = request.get_json().get('result_end')
        #result_end = datetime.datetime.strptime(result_end, "%Y-%m-%d")
        result_is_key = request.get_json().get('is_key')
        result_undertakers = request.get_json().get('result_undertakers')
        result_participants = request.get_json().get('result_participants')
        result = Result(result_name=result_name,
                        result_type=result_type,
                        start_date=result_start,
                        end_date=result_end,
                        is_key=result_is_key,
                        undertakers=result_undertakers,
                        participants=result_participants)
        db.session.add(result)
        db.session.commit()
        result_list = []
        if project.result_index_list != None:
            result_list = eval(project.result_index_list)
        result_list.append(result.id)
        project.result_index_list = str(result_list)
        db.session.add(project)
        db.session.commit()
        return jsonify({"msg":"result add successful"}), 200



@api.route('/project/result/<int:rid>/delete/', methods = ['POST'])
@Applicant.check
def delete_result(aid, rid):
    applicant = Applicant.query.filter_by(id=aid).first()
    pid = applicant.posting_project_id
    if request.method == 'POST':
        project = Project.query.filter_by(id=pid).first()
        if project == None:
            return jsonify({"msg": "project is inexistent"}), 404
        if Result.query.filter_by(id=rid).delete():
            return jsonify({'msg':'result have been deleted'}),200
        else:
            return jsonify({'msg':'result is inexitent'}),404


@api.route('/project/result/save/', methods = ['POST'])
@Applicant.check
def save_results(aid):
    applicant = Applicant.query.filter_by(id=aid).first()
    pid = applicant.posting_project_id
    if request.method == 'POST':
        project = Project.query.filter_by(id=pid).first()
        if project == None:
            return jsonify({"msg": "project is inexistent"}), 404
        results_index = request.get_json().get('index')
        if results_index == None:
            return jsonify({'msg':'index is empty'}), 404
        index = [int(x) for x in results_index.split(' ')]
        project.result_index_list = str(index)
        db.session.add(project)
        db.session.commit()
        return jsonify({'msg':'result saved'}),200
