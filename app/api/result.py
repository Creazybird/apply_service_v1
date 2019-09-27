#coding:utf-8
import json
from . import api
from ...app import db
from ...app.models import Project, Applicant, Result
from flask import jsonify, request

@api.route('/project/<int:pid>/result/get/', methods = ['GET'])
@Applicant.check
def get_results(aid, pid):
    if request.method == 'GET':
        project = Project.query.filter_by(id=pid).first()
        if project != None:
            project_results_list = Result.query.filter_by(project_id=pid).all()
            project_results_index_list = []
            for result in project_results_list:
                project_results_index_list.append(result.id)
            result_index_list = eval(project.result_index_list)
            result_list = []
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
                if result_index != -1:
                    result = project_results_list[result_index]
                    one_result["id"] = result.id
                    one_result["name"] = result.result_name
                    one_result["type"] = result.result_type
                    one_result["start"] = result.start_date
                    one_result["end"] = result.end_date
                    one_result["undertakers"] = result.undertakes
                    result_list.append(one_result)
                    return jsonify({"result_list":result_list}), 200
                else:
                    return jsonify({"msg":"result is inexistent"}), 404
        else:
            return jsonify({"msg":"project is inexistent"}), 404