from flask import request, Response

from flask import Blueprint

from src.controllers.auth_controller import easy_authentication_required
from src.controllers.format_controller import FormatController
from src.models.FoodType import FoodType

blueprint = Blueprint("food_types", __name__, url_prefix="/food-types")


@blueprint.get("/")
@easy_authentication_required
def get_food_types():
    # get data
    data = dict(request.args)
    name = str(data.get("name", ""))
    limit = int(data.get("limit", 3))
    m_format = str(data.get("format", "json"))

    # get food types
    food_types = FoodType.query.filter(FoodType.name.contains(name)).limit(limit).all()

    # convert to format
    try:
        fc = FormatController(m_format)
    except ValueError:
        return {"message": "wrong_format_type"}, 400

    return Response(fc.converter.convert_food_type_list(food_types, False), mimetype=f"application/{m_format}")
