import datetime
from flask import jsonify, request, current_app, abort
from . import api
from .. import db
from ..models import Project, Applicant, ProjectCategory, FundingPlan, Result


@api.route("/project/posting/cache/base_information/",methods=["GET"], endpoint="GetProjectCache")
@Applicant.check
def get_project_cache(aid):
    applicant = Applicant.query.filter_by(id=aid).first()
    if applicant.posting:
        project = Project.query.filter_by(id=applicant.posting_project_id).first()
        return jsonify({
            "name_cn": project.name_cn,
            "apply_date": project.apply_date,
            "start_date": project.start_date,
            "end_date": project.end_date,
            "abstract_cn": project.abstract_cn,
            "project_code_1": project.project_code_1,
            "project_code_2": project.project_code_2
        }), 200
    else:
        return jsonify("Posting nothing"), 201


@api.route("/project/base_information/", methods=["POST"], endpoint="PostProjectBaseInformation")
@Applicant.check
def post_project_base_information(aid):
    payload = request.json
    applicant = Applicant.query.filter_by(id=aid).first()
    project = Project(project_category_id=request.json.get("project_category_id"), applicant_id=aid)
    if applicant.posting:
        project = Project.query.filter_by(id=applicant.posting_project_id).first()
    else:
        applicant.posting = True
        project.status = 0
        db.session.add(project)
        db.session.commit()
        applicant.posting_project_id = project.id
        db.session.add(applicant)
        db.session.commit()

    project.name_cn = payload.get("name_cn")
    project.apply_date = payload.get("apply_date")
    project.start_date = payload.get("start_date")
    project.end_date = payload.get("end_date")
    project.abstract_cn = payload.get("abstract_cn")
    project.project_code_1 = payload.get("project_code_1")
    project.project_code_2 = payload.get("project_code_2")

    db.session.add(project)
    db.session.commit()
    return jsonify({
        "project_id": project.id
    }), 200
