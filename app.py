from flask import Flask
app = Flask(__name__)

# This page will show all restaurants
@app.route('/')
@app.route('/restaurant')
def showRestaurants():

# This page will be for making a new restaurant
@app.route('/restaurant/new')
def newRestaurant():

# This page will be for editing restaurant
@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):

#Route for deleting restaurant
@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):

#Route for Restaurant menus
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id, menu_id):

#Route for new Menu Item:
@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id, menu_id):

#Route for editing menu items
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem():

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delet')
def deleteMenuItem():

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)