from internal.exceptions import FieldInUseError, CustomError
from internal.helper import json_from_request, check_keys, get_record_by_id

from app import db, services
from app.subject.models import Subject
from .models import Lesson, LessonTeacher, LessonStudent

from flask import g, jsonify


def add_teachers(teacher_ids, lesson):
    response = services.user.post(
        "permissions/validate",
        json={'user_ids': teacher_ids, 'permissions': ["Teacher"]},
        headers={'Content-Type': 'application/json', **g.user.headers_dict()}
    )
    if response.status_code != 200:
        raise CustomError(
            **response.json()
        )
    for teacher_id in teacher_ids:
        lesson.teachers.append(LessonTeacher(lesson.id, teacher_id))


def add_students(student_ids, lesson):
    response = services.user.post(
        "permissions/validate",
        json={'user_ids': student_ids, 'permissions': ["Student"]},
        headers={'Content-Type': 'application/json', **g.user.headers_dict()}
    )
    if response.status_code != 200:
        raise CustomError(
            **response.json()
        )
    for student_id in student_ids:
        lesson.students.append(LessonStudent(lesson.id, student_id))


def lesson_create(request):
    # Parse JSON from request
    data = json_from_request(request)

    # Check JSON has keys needed
    expected_keys = ['name', 'subject_id']
    check_keys(expected_keys=expected_keys, data=data)

    # Validate subject_id
    subject = get_record_by_id(
        data['subject_id'],
        Subject,
        custom_not_found_error=CustomError(409, message="Invalid subject_id.")
    )

    # Validate name
    validate_lesson_name(data['name'], g.user.school_id)

    # Create lesson
    lesson = Lesson(
        name=data['name'],
        school_id=g.user.school_id,
        subject_id=subject.id
    )

    # db.session.add(lesson)
    # db.session.commit()

    # Add teachers (if supplied)
    if 'teacher_ids' in data.keys():
        add_teachers(data['teacher_ids'], lesson)

    # Add students (if supplied)
    if 'student_ids' in data.keys():
        add_students(data['student_ids'], lesson)

    db.session.add(lesson)
    db.session.commit()

    return jsonify({'success': True, 'lesson': lesson.to_dict(nest_teachers=True)}), 201


def validate_lesson_name(name, school_id):
    query = Lesson.query.filter_by(name=name, school_id=school_id)
    lesson = query.first()

    if lesson is not None:
        raise FieldInUseError('name')


def lesson_listing(request):
    query = Lesson.query.filter_by(school_id=g.user.school_id)

    # Filter by subject
    subjects = request.args.get("subject")

    if subjects is not None:
        subjects = subjects.split(",")
        query = query.filter(Lesson.subject_id.in_(subjects))

    lessons = query.all()
    return jsonify({'success': True, 'lessons': [lesson.to_dict(nest_teachers=True) for lesson in lessons]})