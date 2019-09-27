from flask import jsonify, request, current_app, abort
from . import api
from .. import db
from ..models import ProjectCategory

@api.route("/projectCategories/", methods=["GET"], endpoint="GetProjectCategoryList")
def get_project_category_list():
    categories = ProjectCategory.query.all()
    dict = {
        "list": [{
            "id": x.id,
            "name": x.category_name
        } for x in categories]
    }
    return jsonify(dict), 200