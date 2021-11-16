from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(80), nullable=False)
    stream = db.Column(db.String(80), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))


class Create(Resource):
    def post(self):
        data_posted_by_user = request.get_json()
        id = data_posted_by_user['id']
        name = data_posted_by_user['name']
        stream = data_posted_by_user['stream']

        presentOrNot = Student.query.filter_by(id=id).first()
        if presentOrNot is not None:
            return "id already exists"

        else:
            studentObj = Student(id=id, name=name, stream=stream)
            db.session.add(studentObj)
            db.session.commit()
            return "added successfully"


class Read(Resource):
    def get(self):
        data = Student.query.all()
        returnValue = {}
        if len(data) == 0:
            return "No Entries have been added yet"
        for student in data:
            returnValue[str(student.id)] = {"name": student.name, "stream": student.stream}
        return jsonify(returnValue)


class Update(Resource):
    def put(self):
        data_posted_by_user = request.get_json()
        id = data_posted_by_user['id']
        name = data_posted_by_user['name']
        stream = data_posted_by_user['stream']

        presentOrNot = Student.query.filter_by(id=id).first()
        if presentOrNot is not None:
            presentOrNot.name = name
            presentOrNot.stream = stream
            db.session.flush()
            db.session.commit()
            return 'Update Success'
        else:
            return 'id not found'


class Delete(Resource):
    def delete(self):
        data_posted_by_user=request.get_json()
        id=data_posted_by_user['id']

        presentOrNot=Student.query.filter_by(id=id).first()
        if presentOrNot is not None:
            db.session.delete(presentOrNot)
            db.session.flush()
            db.session.commit()
            return 'Delete success'
        else:
            return 'id not found'


api.add_resource(Create, '/create')
api.add_resource(Read, '/read')
api.add_resource(Update, '/update')
api.add_resource(Delete, '/delete')

if __name__ == '__main__':
    app.run(port=8000, debug=True)