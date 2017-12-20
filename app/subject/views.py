from flask import Blueprint, request
from .models import Subject
from app.lesson.models import Lesson
from .subject_functions import create_subject_view, list_subject_view

subject_blueprint = Blueprint("subject", __name__, url_prefix="/subject")


@subject_blueprint.route('/subject', methods=['POST', 'GET'])
def subject_list_or_create_view():
    if request.method == "POST":
        return create_subject_view(request)
    else:
        return list_subject_view(request)
