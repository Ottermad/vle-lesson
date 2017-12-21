from flask import Blueprint, request, g
from .models import Subject
from app.lesson.models import Lesson
from .subject_functions import (
    create_subject_view, 
    list_subject_view,
    subject_detail_view,
    subject_delete_view,
    subject_update_view
)
from internal.exceptions import UnauthorizedError

subject_blueprint = Blueprint("subject", __name__, url_prefix="/subject")


@subject_blueprint.route('/subject', methods=['POST', 'GET'])
def subject_list_or_create_view():
    if request.method == "POST":
        return create_subject_view(request)
    else:
        return list_subject_view(request)


@subject_blueprint.route('/subject/<subject_id>', methods=['GET', 'PUT', 'DELETE'])
def subject_individual_view(subject_id):
    if request.method == 'GET':
        return subject_detail_view(request, subject_id=subject_id)
    if request.method == 'DELETE':
        if g.user.has_permissions({'Administrator'}):
            return subject_delete_view(request, subject_id)
        raise UnauthorizedError()
    if request.method == 'PUT':
        if g.user.has_permissions({'Administrator'}):
            return subject_update_view(request, subject_id)
        raise UnauthorizedError()
