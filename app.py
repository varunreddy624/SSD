from flask import Flask, request, jsonify, session
from flask_session import Session
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin


app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:mYSQLSERVER@localhost:3306/testdb"

db = SQLAlchemy(app)


class Menu(UserMixin, db.Model):
    __tablename__ = 'menu'

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    half_plate_price = db.Column(db.Integer, nullable=False)
    full_plate_price = db.Column(db.Integer, nullable=False)


class Transactions(UserMixin, db.Model):
    __tablename__ = 'transactions'

    transaction_id = db.Column(db.Integer, primary_key=True)
    item_total_cost = db.Column(db.Integer, nullable=False)
    tip_percent = db.Column(db.Float, nullable=False)
    number_of_persons_to_split = db.Column(db.Integer, nullable=False)
    random_discount_val= db.Column(db.Float, nullable=False)
    total_bill_cost = db.Column(db.Float, nullable=False)


class ItemList(UserMixin, db.Model):
    __tablename__ = 'item_list'

    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.transaction_id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('menu.item_id'),primary_key=True)
    type = db.Column(db.String(30),primary_key=True)
    quantity = db.Column(db.Integer,nullable=False)



class MenuAdd(Resource):
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


class MenuRead(Resource):
    def get(self):
        data = Menu.query.all()
        returnValue = {}
        if len(data) == 0:
            return "No Entries have been added yet"
        for menu in data:
            returnValue[menu.item_id] = {"half_plate_price": menu.half_plate_price, "full_plate_price": menu.full_plate_price}
        return jsonify(returnValue)


class TransactionAdd(Resource):
    def post(self):
        data_posted_by_user = request.get_json()
        item_total_cost = data_posted_by_user['item_total_cost']
        tip_percent = data_posted_by_user['tip_percent']
        number_of_persons_to_split = data_posted_by_user['number_of_persons_to_split']
        random_discount_val = data_posted_by_user['random_discount_val']
        total_bill_cost = data_posted_by_user['total_bill_cost']

        transObj = Transactions(
                                item_total_cost=item_total_cost,
                                tip_percent=tip_percent,
                                number_of_persons_to_split=number_of_persons_to_split,
                                random_discount_val=random_discount_val,
                                total_bill_cost=total_bill_cost
                                )

        db.session.add(transObj)
        db.session.commit()
        return jsonify({'transaction_id':transObj.transaction_id})


class ItemAdd(Resource):
    def post(self):
        data_posted_by_user = request.get_json()
        transaction_id = data_posted_by_user['transaction_id']
        item_id = data_posted_by_user['item_id']
        type = data_posted_by_user['type']
        quantity = data_posted_by_user['quantity']

        itemListObj = ItemList(
                            transaction_id=transaction_id,
                            item_id=item_id,
                            type=type,
                            quantity=quantity
                        )
        db.session.add(itemListObj)
        db.session.commit()
        return "item added successfully"


api.add_resource(MenuAdd, '/menu/add')
api.add_resource(MenuRead, '/menu/fetch')
api.add_resource(ItemAdd,'/item_list/add')
api.add_resource(TransactionAdd,'/transaction/add')

if __name__ == '__main__':
    app.run(port=8000, debug=True)