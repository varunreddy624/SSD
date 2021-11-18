# Database :
1. Users-
    * userid - String - PK 
    * name - String
    * password - String
    * ischef - Boolean
2. Menu-
    * id - PK
    * halfprice
    * fullprice
3. Order-
    * orderid - PK
    * transactionid -FK
    * itemid - FK
    * plate - HALF/FULL
    * quantity
    * price
5. Transaction-
    * userid - FK
    * transactionid (auto generated) -PK
    * date
    * tip
    * discount
    * split
    * total

# Rest Endpoint :
If you're using flask-login just use `@login_required` annotation for route protection
* `/menu/add` : `POST` -> add an item to menu
* `/menu/fetch` : `GET` -> get all the menu items in json  structure
* `/user/signup`: `POST` -> create new user in db
* `/user/login`: `GET` -> login user and add to session and send cookie (store cookie on client)
* `/user/logout`: `GET` -> logout user from session and make cookie invalid
* `/transaction/entry` : `POST` -> Store the transaction in database
* `/transaction/fetch` : `GET`-> Fetch details of single transaction(transaction id)
* `/transaction/all` : `GET`-> Fetch all transactions(minimal info)

# Client script operations :
1. Options -
    * Signup - create a new user with ischef flag false
    * Login - take username and password and authenticate -> find if chef/user
2. Login user/Chef
    * User Login - Options: (do not allow logout while orders are in queue)
        * View Menu
        * Order an item
        * Generate the Bill (Do not generate bill if items not ordered)
        * View Transactions - > Select transaction -> View in Detail
        * Logout
    * Chef Login - Options:
        * View Menu
        * Order an item
        * Generate the Bill
        * View Transactions - > Select transaction -> View in Detail
        * Add new item in menu
        * Logout

# Transaction structure:

```json
{
   "total": 1246.90,
   "tip": 10.00,
   "discount": 20.00,
   "split": 5,
   "orders": [
      {
         "itemid": 1,
         "plate": "FULL",
         "quantity": 3,
         "price": 120
      },
      {
         "itemid": 1,
         "plate": "HALF",
         "quantity": 3,
         "price": 234
      },
      {
         "itemid": 2,
         "plate": "FULL",
         "quantity": 3,
         "price": 245
      }
   ]
}
```