from app import db


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
    teachers = db.relationship("LessonTeacher")
    students = db.relationship("LessonStudent")
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
            lesson_as_dict['teachers'] = [t.to_dict() for t in self.teachers]

        if nest_students:
            lesson_as_dict['students'] = [s.to_dict() for s in self.students]

        # if nest_homework:
        #     lesson_as_dict['homework'] = [h.to_dict(date_as_string=True) for h in self.homework]

        return lesson_as_dict
