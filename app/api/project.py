import datetime
from flask import jsonify, request, current_app, abort
from . import api
from .. import db
from ..models import Project, Applicant

@api.route("/project/new/", methods=["GET"], endpoint="CreateProject")
@Applicant.check
def create_project(aid):
    applicant = Applicant.query.filter_by(id=aid).first()
    if applicant.posting is True:
        return jsonify({
            "project_id": applicant.posting_project_id,
        }), 201
    else:
        category_id = request.args.get("category_id")
        project = Project(applicant_id=aid, project_category_id=category_id)
        applicant.posting = True
        db.session.add(project)
        db.session.commit()
        applicant.posting_project_id = project.id
        db.session.add(applicant)
        db.session.commit()
        return jsonify({
            "project_id": project.id,
        }), 200