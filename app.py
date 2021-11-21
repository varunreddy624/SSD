from collections import defaultdict
from flask import Flask, json, request, jsonify
from flask_login.utils import login_required
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user


app = Flask(__name__)
app.secret_key = 'something'

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:mYSQLSERVER@localhost:3306/testdb"

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(50))
    is_chef = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.user_id

    def is_active(self):
        return True
    
    def is_authenticated(self):
        return True


@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    try:
        t= User.query.get(int(user_id))
        return t
    except:
        return None


class Menu(UserMixin, db.Model):
    __tablename__ = 'menu'

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    half_plate_price = db.Column(db.Integer, nullable=False)
    full_plate_price = db.Column(db.Integer, nullable=False)


class Transactions(UserMixin, db.Model):
    __tablename__ = 'transactions'

    transaction_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),db.ForeignKey('user.username'))
    item_total_cost = db.Column(db.Integer, nullable=False)
    tip_percent = db.Column(db.Float, nullable=False)
    updated_share_of_each_person = db.Column(db.Float, nullable=False)
    random_discount_val= db.Column(db.Float, nullable=False)
    total_bill_cost = db.Column(db.Float, nullable=False)


class ItemList(UserMixin, db.Model):
    __tablename__ = 'item_list'

    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.transaction_id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('menu.item_id'),primary_key=True)
    type = db.Column(db.String(30),primary_key=True)
    quantity = db.Column(db.Integer,nullable=False)


class SignUp(Resource):
    def post(self):
        data_posted_by_user = request.get_json()
        username = data_posted_by_user['username']
        password = data_posted_by_user['password']
        is_chef = data_posted_by_user['is_chef']
        isPresent = User.query.filter_by(username=username).first()

        returnValue = {}

        if isPresent is not None:
            returnValue['data']='username already exists'
        
        else:
            userObj = User(username=username,password=password,is_chef=is_chef)
            db.session.add(userObj)
            db.session.commit()
            returnValue['data']="sign up successfully"
        
        return jsonify(returnValue)



class Login(Resource):
    def post(self):
        data_posted_by_user = request.get_json()
        username = data_posted_by_user['username']
        password = data_posted_by_user['password']
        user = User.query.filter_by(username=username,password=password).first()


        returnValue = {}
        if user:
            login_user(user,remember=True)
            returnValue['data']='success'
        
        else:
            returnValue['data']='failure'

        return jsonify(returnValue)


class MenuAdd(Resource):
    def post(self):
        data_posted_by_user = request.get_json()
        username = data_posted_by_user['username']
        print(username)
        if User.query.filter_by(username=username).first().is_chef == True:
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
        else:
            return "only chefs can manipulate menu"


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
        username = data_posted_by_user['username']
        item_total_cost = data_posted_by_user['item_total_cost']
        tip_percent = data_posted_by_user['tip_percent']
        updated_share_of_each_person = data_posted_by_user['updated_share_of_each_person']
        random_discount_val = data_posted_by_user['random_discount_val']
        total_bill_cost = data_posted_by_user['total_bill_cost']

        transObj = Transactions(
                                username = username,
                                item_total_cost=item_total_cost,
                                tip_percent=tip_percent,
                                updated_share_of_each_person=updated_share_of_each_person,
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
        items_list = data_posted_by_user['items_list']

        for i in items_list:
            itemListObj = ItemList(
                                transaction_id=transaction_id,
                                item_id=i['item_id'],
                                type=i['type'],
                                quantity=i['quantity']
                            )
            db.session.add(itemListObj)

        db.session.commit()
        return "item added successfully"

class TransactionView(Resource):
    def post(self):
        data_posted_by_user = request.get_json()

        username = data_posted_by_user['username']

        data = Transactions.query.filter_by(username=username)
        returnValue = {}
        for tx in data:
            returnValue[tx.transaction_id] = {"total_bill_cost": tx.total_bill_cost}
        return jsonify(returnValue)


class TransactionSpecificView(Resource):
    def post(self):
        data_posted_by_user = request.get_json()

        transaction_id = data_posted_by_user['transaction_id']

        transaction_summary = Transactions.query.filter_by(transaction_id=transaction_id).first()
        itemList = ItemList.query.filter_by(transaction_id=transaction_id)

        order=defaultdict(lambda: [0, 0])
        for i in itemList:
            if i.type=="Half":
                order[i.item_id][0]=i.quantity
            else:
                order[i.item_id][1]=i.quantity

        returnValue = {}
        returnValue['order']=order
        returnValue['item_total_cost']=transaction_summary.item_total_cost
        returnValue['random_discount_val']=transaction_summary.random_discount_val
        returnValue['total_bill_cost']=transaction_summary.total_bill_cost
        returnValue['updated_share_of_each_person']=transaction_summary.updated_share_of_each_person
        returnValue['tip_percent']=transaction_summary.tip_percent
    

        return jsonify({'data':returnValue})

class Logout(Resource):
    def get(self):
        logout_user()


api.add_resource(SignUp,'/signup')
api.add_resource(Login,'/login')
api.add_resource(Logout,'/logout')

api.add_resource(MenuAdd, '/menu/add')
api.add_resource(MenuRead, '/menu/fetch')

api.add_resource(ItemAdd,'/item_list/add')

api.add_resource(TransactionAdd,'/transaction/add')
api.add_resource(TransactionView,'/transaction/fetch/all')
api.add_resource(TransactionSpecificView,'/transaction/fetch/specific')

if __name__ == '__main__':
    app.run(port=8000, debug=True)