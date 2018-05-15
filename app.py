from flask import Flask, render_template, url_for, redirect, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

"""
Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'},
                {'name':'Blue Burgers', 'id':'2'},
                {'name':'Taco Hut', 'id':'3'}]

Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese',
'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake',
'description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert',
'id':'2'},{'name':'Caesar Salad',
'description':'with fresh organic vegetables', 'price':'$5.99',
'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon',
'price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip',
'description':'creamy dip with fresh spinach','price':'$1.99',
'course':'Appetizer','id':'5'} ]
item = {'name':'Cheese Pizza','description':'made with fresh cheese',
'price':'$5.99','course' :'Entree'}
"""


# This page will show all restaurants

@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
    restaurant = session.query(Restaurant).all()
    return render_template(
        'restaurants.html', restaurant=restaurant)


# This page will be for making a new restaurant

@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template(
            'newRestaurant.html')


# This page will be for editing restaurant

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
    else:
        return render_template(
            'editRestaurant.html', restaurant=editedRestaurant)


# Route for deleting restaurant

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurantToDelete = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        session.commit()
        return redirect(
            url_for('showRestaurants', restaurant_id=restaurant_id))
    else:
        return render_template(
            'deleteRestaurant.html', restaurant=restaurantToDelete)


# Route for Restaurant menus
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return render_template(
        'menu.html', restaurant=restaurant, items=items)


# Route for new Menu Item:

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
            'description'], price=request.form['price'],
            course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showMenu'), restaurant_id=restaurant_id)
    else:
        return render_template(
            'newMenuItem.html', restaurant_id=restaurant_id)


# Route for editing menu items

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editMenuItem.html', restaurant_id=restaurant_id,
            menu_id=menu_id, item=editedItem)


# Route for deleting menu items

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        return redirect(url_for(
            'showMenu', restaurant_id=restaurant_id))
    return render_template(
        'deleteMenuItem.html', restaurant_id=restaurant_id,
        menu_id=menu_id, item=deletedItem)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
