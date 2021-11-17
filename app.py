from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin


app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:mYSQLSERVER@localhost:3306/testdb"

db = SQLAlchemy(app)

class Menu(UserMixin, db.Model):
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    half_plate_price = db.Column(db.Integer, nullable=False)
    full_plate_price = db.Column(db.Integer, nullable=False)



class Create(Resource):
    def post(self):
        data_posted_by_user = request.get_json()
        item_id = data_posted_by_user['item_id']
        half_plate_price = data_posted_by_user['half_plate_price']
        full_plate_price = data_posted_by_user['full_plate_price']

        presentOrNot = Menu.query.filter_by(item_id=item_id).first()
        
        if presentOrNot is not None:
            return "item_id already exists"

        else:
            menuObj = Menu(item_id=item_id, half_plate_price=half_plate_price, full_plate_price=full_plate_price)
            db.session.add(menuObj)
            db.session.commit()
            return "item added successfully"


class Read(Resource):
    def get(self):
        data = Menu.query.all()
        returnValue = {}
        if len(data) == 0:
            return "No Entries have been added yet"
        for menu in data:
            returnValue[str(menu.item_id)] = {"half_plate_price": menu.half_plate_price, "full_plate_price": menu.full_plate_price}
        return jsonify(returnValue)


api.add_resource(Create, '/create')
api.add_resource(Read, '/read')

if __name__ == '__main__':
    app.run(port=8000, debug=True)