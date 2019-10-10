import json
from flask import jsonify, request, current_app, abort
from . import api
from .. import db
from ..models import FundingPlan, Project, Applicant


@api.route("/project/funding_plan/", methods=["POST"], endpoint="PostProjectFundingPlan")
@Applicant.check
def post_project_funding_plan(aid):
    applicant = Applicant.query.filter_by(id=aid).first()
    if applicant.posting is False:
        return jsonify({
            "msg": "You're not posting any project.",
        }), 201

    project = Project.query.filter_by(id=applicant.posting_project_id).first()

    payload = request.json
    funding = FundingPlan.query.filter_by(id=project.funding_plan_id).first()
    if funding is None:
        funding = FundingPlan(condition_id=1, applicant_id=aid, years=json.dumps({}))
        db.session.add(funding)
        db.session.commit()
        project.funding_plan_id = funding.id
        db.session.add(project)
        db.session.commit()
    
    funding.count = payload.get("count")
    funding.device = payload.get("device")
    funding.data = payload.get("data")
    funding.meeting = payload.get("meeting")
    funding.travel = payload.get("travel")
    funding.working = payload.get("working")
    funding.manage = payload.get("manage")
    funding.other = payload.get("other")
    funding.years = json.dumps(payload.get("years"))

    if not funding.check():
        return jsonify("Wrong format."), 403

    db.session.add(funding)
    db.session.commit()
    return jsonify("ok"), 200


@api.route("/project/posting/cache/funding_plan/", methods=["GET"], endpoint="GetFundingPlanCache")
@Applicant.check
def get_funding_plan_cache(aid):
    applicant = Applicant.query.filter_by(id=aid).first()
    if applicant.posting is False:
        return jsonify({
            "msg": "You're not posting any project.",
        }), 201
    project = Project.query.filter_by(id=applicant.posting_project_id).first()
    funding = FundingPlan.query.filter_by(id=project.funding_plan_id).first()
    if funding is None:
        funding = FundingPlan(condition_id=1, applicant_id=aid, years=json.dumps({}))
        db.session.add(funding)
        db.session.commit()
    return jsonify({
        "count": funding.count,
        "device": funding.device,
        "data": funding.data,
        "meeting": funding.meeting,
        "travel": funding.travel,
        "working": funding.working,
        "manage": funding.manage,
        "other": funding.other,
        "years": json.loads(funding.years)
    }), 200
