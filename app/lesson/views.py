from flask import Blueprint, request, g
from internal.exceptions import UnauthorizedError

from .lesson_functions import lesson_create, lesson_listing

lessons_blueprint = Blueprint('lessons',  __name__, url_prefix="/lessons")


@lessons_blueprint.route('/lesson', methods=['POST', 'GET'])
def lesson_list_or_create_view():
    if request.method == "POST":
        if g.user.has_permissions({'Administrator'}):
            return lesson_create(request)
        raise UnauthorizedError()
    if request.method == "GET":
        return lesson_listing(request)
