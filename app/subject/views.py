from flask import Blueprint
from .models import Subject
from app.lesson.models import Lesson

subject_blueprint = Blueprint("subject", __name__, url_prefix="/subject")