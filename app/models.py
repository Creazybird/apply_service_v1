import time
import json
import datetime
from . import db
from .exceptions import ActivityError
import werkzeug.http
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, jsonify, request
from functools import wraps


class Project(db.Model):
    __tablename__ = 'project'
    id      = db.Column(db.Integer, primary_key=True)
    name_cn = db.Column(db.String(120))
    name_en = db.Column(db.String(120))
    apply_date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    end_date   = db.Column(db.Date)
    status                = db.Column(db.Integer, default=0)
    abstract_cn           = db.Column(db.Text)
    abstract_en           = db.Column(db.Text)
    project_code_1        = db.Column(db.String(8))
    project_code_2        = db.Column(db.String(8))
    result_type           = db.Column(db.Integer)
    apply_funding_count   = db.Column(db.Integer, default=0)
    work_unit             = db.Column(db.String(120))
    unit_linkman          = db.Column(db.String(36))
    unit_linkman_email    = db.Column(db.String(24))
    unit_linkman_tel      = db.Column(db.String(16))
    academy_linkman       = db.Column(db.String(36))
    academy_linkman_email = db.Column(db.String(24))
    academy_linkman_tel   = db.Column(db.String(16))
    result_index_list     = db.Column(db.Text)
    member_list           = db.Column(db.Text)

    applicant_id = db.Column(db.Integer, nullable=False)
    project_category_id = db.Column(db.Integer, nullable=False)
    funding_plan_id = db.Column(db.Integer)


class ProjectCategory(db.Model):
    __tablename__ = 'project_category'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(16))

    apply_condition_id = db.Column(db.Integer, nullable=False)


class Applicant(db.Model):
    __tablename__ = 'applicant'
    id = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(36))
    sex        = db.Column(db.Boolean)
    nation     = db.Column(db.String(16))
    birth_date = db.Column(db.Date)
    administrative_duty = db.Column(db.String(32))
    professional_duty   = db.Column(db.String(32))
    last_degree         = db.Column(db.String(16))
    specialization      = db.Column(db.String(64))
    metor    = db.Column(db.String(16))
    province = db.Column(db.String(20))
    tel      = db.Column(db.String(16))
    location = db.Column(db.String(120))
    zip_code = db.Column(db.String(6))
    posting  = db.Column(db.Boolean)

    posting_project_id = db.Column(db.Integer)
    accound_id = db.Column(db.Integer, nullable=False)

    def check(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(1, *args, **kwargs)
        return decorated_function


class FundingPlan(db.Model):
    __tablename__ = 'funding_plan'
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)
    device = db.Column(db.Float, default=0.0)
    data = db.Column(db.Float, default=0.0)
    meeting = db.Column(db.Float, default=0.0)
    travel = db.Column(db.Float, default=0.0)
    working = db.Column(db.Float, default=0.0)
    manage = db.Column(db.Float, default=0.0)
    other = db.Column(db.Float, default=0.0)
    years = db.Column(db.Text)

    condition_id = db.Column(db.Integer, nullable=False)
    applicant_id = db.Column(db.Integer, nullable=False)

    def check(self):
        return int(self.device+self.data+self.meeting+self.travel+self.manage+self.working+self.other) == self.count


class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key=True)
    result_name = db.Column(db.String(64))
    result_type = db.Column(db.Integer, default=0)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    undertakes = db.Column(db.String(128))

    project_id = db.Column(db.Integer, nullable=False)