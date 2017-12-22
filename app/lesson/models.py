from app import db, services
from flask import g
from internal.exceptions import CustomError


class LessonTeacher(db.Model):
    # __table_args__ = (
    #     PrimaryKeyConstraint('lesson_id', 'user_id'),
    #     {},
    # )
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, lesson_id, user_id):
        self.lesson_id = lesson_id
        self.user_id = user_id

    def to_dict(self):
        return {
            'user_id': self.user_id
        }


class LessonStudent(db.Model):
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), primary_key=True)
    user_id = db.Column('user_id', db.Integer, primary_key=True)

    def __init__(self, lesson_id, user_id):
        self.lesson_id = lesson_id
        self.user_id = user_id

    def to_dict(self):
        return {
            'user_id': self.user_id
        }


class Lesson(db.Model):
    __mapper_args__ = {'confirm_deleted_rows': False}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    subject_id =db.Column(db.Integer, db.ForeignKey('subject.id'))
    school_id = db.Column(db.Integer)

    subject = db.relationship('Subject')
    teachers = db.relationship(
        "LessonTeacher",
        cascade="all, delete-orphan"
    )
    students = db.relationship("LessonStudent", cascade="all, delete-orphan")
    # teachers = db.relationship(
    #     'User', secondary=lesson_teacher,
    #     backref=db.backref('lesson_teacher', lazy='dynamic')
    # )

    # students = db.relationship(
    #     'User', secondary=lesson_student,
    #     backref=db.backref('lesson_student', lazy='dynamic')
    # )

    def __init__(self, name, subject_id, school_id):
        self.name = name
        self.subject_id = subject_id
        self.school_id = school_id

    def to_dict(self, nest_teachers=False, nest_students=False, nest_subject=False, nest_homework=False):
        lesson_as_dict = {
            'id': self.id,
            'name': self.name,
            'school_id': self.school_id,
            'subject_id': self.subject_id
        }

        if nest_subject:
            lesson_as_dict['subject'] = self.subject.to_dict()

        if nest_teachers:
            response = services.user.get("user/user", params={'ids': t.user_id for t in self.teachers}, headers=g.user.headers_dict())
            if response.status_code != 200:
                    raise CustomError(
                        **response.json()
                    )
            lesson_as_dict['teachers'] = response.json()['users']

        if nest_students:
            response = services.user.get("user/user", params={'ids': s.user_id for s in self.students}, headers=g.user.headers_dict())
            if response.status_code != 200:
                   raise CustomError(
                       **response.json()
                   )
            lesson_as_dict['students'] = response.json()['users']


        if nest_homework:
            lesson_as_dict['homework'] = []
            # lesson_as_dict['homework'] = [h.to_dict(date_as_string=True) for h in self.homework]

        return lesson_as_dict
