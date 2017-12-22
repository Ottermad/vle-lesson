from flask import Blueprint, request, g
from internal.decorators import permissions_required
from internal.exceptions import UnauthorizedError

from .lesson_functions import (
    lesson_create,
    lesson_listing,
    lesson_detail,
    lesson_update,
    lesson_delete,
    lessons_taught
)

lessons_blueprint = Blueprint('lessons',  __name__, url_prefix="/lessons")


@lessons_blueprint.route('/lesson', methods=['POST', 'GET'])
def lesson_list_or_create_view():
    if request.method == "POST":
        if g.user.has_permissions({'Administrator'}):
            return lesson_create(request)
        raise UnauthorizedError()
    if request.method == "GET":
        return lesson_listing(request)


@lessons_blueprint.route('/lesson/<int:lesson_id>', methods=['GET', 'PUT', 'DELETE'])
def lesson_detail_view(lesson_id):
    if request.method == 'GET':
        return lesson_detail(request, lesson_id=lesson_id)

    if request.method == 'PUT':
        if g.user.has_permissions({'Administrator'}):
            return lesson_update(request, lesson_id=lesson_id)
        raise UnauthorizedError()

    if request.method == 'DELETE':
        if g.user.has_permissions({'Administrator'}):
            return lesson_delete(request, lesson_id=lesson_id)
        raise UnauthorizedError()


@lessons_blueprint.route('/lesson/taught')
@permissions_required({'Teacher'})
def lessons_taught_view():
    return lessons_taught(request)
