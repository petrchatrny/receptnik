from flask import Blueprint, request, Response

from src.controllers.auth_controller import easy_authentication_required
from src.controllers.format_controller import FormatController
from src.models.Ingredient import Ingredient

blueprint = Blueprint("ingredients", __name__, url_prefix="/ingredients")


@blueprint.get("/")
@easy_authentication_required
def get_ingredients():
    # get data
    data = dict(request.args)
    name = str(data.get("name", ""))
    limit = int(data.get("limit", 5))
    m_format = str(data.get("format", "json"))

    # get ingredients
    ingredients = Ingredient.query.filter(Ingredient.name.contains(name)).order_by(Ingredient.name).limit(limit).all()

    # convert to format
    try:
        fc = FormatController(m_format)
    except ValueError:
        return {"message": "wrong_format_type"}, 400

    return Response(fc.converter.convert_ingredient_list(ingredients), mimetype=f"application/{m_format}")
