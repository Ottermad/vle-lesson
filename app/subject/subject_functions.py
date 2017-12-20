from flask import jsonify, g

from internal.exceptions import FieldInUseError
from internal.helper import json_from_request, check_keys, get_record_by_id

from app import db
from .models import Subject
from app.lesson.models import Lesson


def create_subject(name, school_id):
    if subject_name_in_use(name, school_id):
        raise FieldInUseError('Name')

    subject = Subject(name=name, school_id=school_id)
    db.session.add(subject)
    db.session.commit()
    return subject


def subject_name_in_use(name, school_id):
    # Check name does not already exist for school
    query = Subject.query.filter_by(
        name=name, school_id=school_id
    )
    return query.first() is not None


def subjects_for_school(school_id):
    return Subject.query.filter_by(school_id=school_id).all()


def create_subject_view(request):
    data = json_from_request(request)
    expected_keys = ["name"]
    check_keys(expected_keys, data)

    subject = create_subject(data['name'], g.user.school_id)

    return jsonify({'success': True, 'subject': subject.to_dict()}), 201


def list_subject_view(request):
    # Get subjects and convert to dicts
    subjects = [s.to_dict() for s in subjects_for_school(g.user.school_id)]
    return jsonify({'success': True, 'subjects': subjects})


def subject_detail_view(request, subject_id):
    subject = get_record_by_id(subject_id, Subject)
    return jsonify({'success': True, 'subject': subject.to_dict()})


def subject_delete_view(request, subject_id):
    subject = get_record_by_id(subject_id, Subject)

    # Check if subject still has lessons
    lesson = Lesson.query.filter_by(subject_id=subject.id).first()
    if lesson is not None:
        return jsonify({
            'error': True,
            'message': 'Please delete all lessons which are part of this subject'
        }), 409
    db.session.delete(subject)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Deleted.'})


def subject_update_view(request, subject_id):
    # Get subject
    subject = get_record_by_id(subject_id, Subject)

    # Get JSON data
    data = json_from_request(request)

    # If name in data, then update the name
    if 'name' in data.keys():
        if subject_name_in_use(data['name'], school_id=subject.school_id):
            raise FieldInUseError("name")
        subject.name = data['name']

    db.session.add(subject)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Updated.'})
