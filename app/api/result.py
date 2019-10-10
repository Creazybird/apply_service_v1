#coding:utf-8
import json
import datetime
from . import api
from .. import db
from ..models import Project, Applicant, Result
from flask import jsonify, request

@api.route('/project/posting/cache/result/get/', methods = ['GET'])
@Applicant.check
def get_results(aid):
    if request.method == 'GET':
        applicant = Applicant.query.filter_by(id=aid).first()
        if applicant.posting:
            project = Project.query.filter_by(id=applicant.posting_project_id).first()
            if project == None:
                return jsonify({"msg": "project is inexistent"}), 404
            project_results_list = Result.query.filter_by(project_id=pid).all()
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
                "undertakers":"",
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
                one_result["undertakers"] = result.undertakes
                result_list.append(one_result)
                return jsonify({"result_list":result_list}), 200


@api.route('/project/<int:pid>/result/add/', methods = ['POST'])
@Applicant.check
def add_results(aid, pid):
    if request.method == "POST":
        project = Project.query.filter_by(id=pid).first()
        if project == None:
            return jsonify({"msg": "project is inexistent"}), 404
        name = request.get_json().get('name')
        type = request.get_json().get('type')
        start = request.get_json().get('start')
        start = datetime.datetime.strptime(start,"%Y%m%d")
        end = request.get_json().get('end')
        end = datetime.datetime.strptime(end, "%Y%m%d")
        result = Result(result_name=name,
                        result_type=type,
                        start_date=start,
                        end_date=end)
        db.session.add(result)
        db.session.commit()
        result_list = eval(project.result_index_list)
        result_list.append(result.id)
        project.result_index_list = str(result_list)
        db.session.add(project)
        db.session.commit()
        return jsonify({"msg":"result add successful"}), 200



@api.route('/project/<int:pid>/result/<int:rid>/delete/', methods = ['POST'])
@Applicant.check
def delete_result(aid, pid, rid):
    if request.method == 'POST':
        project = Project.query.filter_by(id=pid).first()
        if project == None:
            return jsonify({"msg": "project is inexistent"}), 404
        if Result.query.filter_by(id=rid).delete():
            return jsonify({'msg':'result have been deleted'}),200
        else:
            return jsonify({'msg':'result is inexitent'}),200


@api.route('/project/<int:pid>/result/save/', method = ['POST'])
@Applicant.check
def save_results(aid, pid):
    if request.method == 'POST':
        project = Project.query.filter_by(id=pid).first()
        if project == None:
            return jsonify({"msg": "project is inexistent"}), 404
        results_index = request.get_json().get('index')
        if results_index == None:
            return jsonify({'msg':'index is empty'}), 404
        index = results_index.split(' ')
        project.result_index_list = str(index)
        db.session.add(project)
        db.session.commit()
        return jsonify({'msg':'result saved'}),200

