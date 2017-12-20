from app import db


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    school_id = db.Column(db.Integer)

    def __init__(self, name, school_id):
        self.name = name
        self.school_id = school_id

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'school_id': self.school_id
        }
