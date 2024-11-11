from flask import Flask, render_template, request, redirect, session, url_for, flash
from datetime import datetime
import mysql.connector
import uuid

app = Flask(__name__)
app.secret_key = 'your_unique_secret_key'



def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="namkeen"
    )

def unique_id():
    return str(uuid.uuid4())

# Home Page
@app.route('/')
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_info = cursor.fetchone()


    cursor.close()
    conn.close()

    return render_template('home.html', user_info=user_info)

# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['pass']
        confirm_password = request.form['cpass']
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user:
            flash('Email already exists!', 'error')
        else:
            user_id = unique_id()
            insert_query = "INSERT INTO users (id, name, email, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (user_id, name, email, password))
            conn.commit()

            session['user_id'] = user_id
            session['user_name'] = name
            session['user_email'] = email
            return redirect(url_for('home'))

        cursor.close()
        conn.close()

    return render_template('register.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            return redirect(url_for('home'))
        else:
            flash('Incorrect username or password', 'error')

        cursor.close()
        conn.close()

    return render_template('login.html')


# Product View Page
@app.route('/view_product', methods=['GET', 'POST'])
def view_product():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    user_id = session.get('user_id', '')

    if request.method == 'POST':
        product_id = request.form['product_id']

        # Adding product to wishlist
        if 'add_to_wishlist' in request.form:
            cursor.execute("SELECT * FROM wishlist WHERE user_id = %s AND product_id = %s", (user_id, product_id))
            if cursor.fetchone():
                flash('Product already exists in your wishlist', 'warning')
            else:
                cursor.execute("SELECT price FROM products WHERE id = %s LIMIT 1", (product_id,))
                product = cursor.fetchone()
                cursor.execute("INSERT INTO wishlist (id, user_id, product_id, price) VALUES (%s, %s, %s, %s)",
                               (unique_id(), user_id, product_id, product['price']))
                conn.commit()
                flash('Product added to wishlist successfully', 'success')

        # Adding product to cart
        if 'add_to_cart' in request.form:
            qty = int(request.form['qty'])
            cursor.execute("SELECT * FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
            if cursor.fetchone():
                flash('Product already exists in your cart', 'warning')
            else:
                cursor.execute("SELECT price FROM products WHERE id = %s LIMIT 1", (product_id,))
                product = cursor.fetchone()
                cursor.execute("INSERT INTO cart (id, user_id, product_id, price, qty) VALUES (%s, %s, %s, %s, %s)",
                               (unique_id(), user_id, product_id, product['price'], qty))
                conn.commit()
                flash('Product added to cart successfully', 'success')

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    return render_template('view_product.html', products=products)



# Contact Us Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    user_id = session.get('user_id', '')

    if request.method == 'POST':
        if 'submit-btn' in request.form:
            name = request.form['name']
            email = request.form['email']
            number = request.form['number']
            message = request.form['message']

            name = name.strip()
            email = email.strip()
            number = number.strip()
            message = message.strip()

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM message WHERE name = %s AND message = %s"
            cursor.execute(query, (name, message))
            
            if cursor.fetchone():
                flash('Message sent already!', 'warning')
            else:
                
                query = "INSERT INTO message ( user_id, name, email, number, message) VALUES ( %s, %s, %s, %s, %s)"
                cursor.execute(query, ( user_id, name, email, number, message))
                conn.commit()
                flash('Message sent successfully!', 'success')

            cursor.close()

    return render_template('contact.html')

# about us Page
@app.route('/about')
def about():
    return render_template('about.html')

# view_page

@app.route('/view_page', methods=['GET', 'POST'])
def view_page():
    user_id = session.get('user_id', '')

    if request.method == 'POST':
        product_id = request.form.get('product_id')

        if 'add_to_wishlist' in request.form:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM wishlist WHERE user_id = %s AND product_id = %s", (user_id, product_id))
            if cursor.fetchone():
                flash('Product already exists in your wishlist', 'warning')
            else:
                cursor.execute("SELECT price FROM products WHERE id = %s LIMIT 1", (product_id,))
                product = cursor.fetchone()
                cursor.execute("INSERT INTO wishlist (id, user_id, product_id, price) VALUES (%s, %s, %s, %s)", 
                               (unique_id(), user_id, product_id, product['price']))
                conn.commit()
                flash('Product added to wishlist successfully', 'success')

            conn.close()

        if 'add_to_cart' in request.form:
            qty = int(request.form.get('qty', 1))
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
            if cursor.fetchone():
                flash('Product already exists in your cart', 'warning')
            else:
                cursor.execute("SELECT price FROM products WHERE id = %s LIMIT 1", (product_id,))
                product = cursor.fetchone()
                cursor.execute("INSERT INTO cart (id, user_id, product_id, price, qty) VALUES (%s, %s, %s, %s, %s)", 
                               (unique_id(), user_id, product_id, product['price'], qty))
                conn.commit()
                flash('Product added to cart successfully', 'success')

            conn.close()

    if request.method == 'GET' and 'pid' in request.args:
        pid = request.args.get('pid')
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE id = %s", (pid,))
        product = cursor.fetchone()
        conn.close()

        if product:
            return render_template('view_page.html', product=product)
        else:
            flash('Product not found', 'error')
            return redirect(url_for('home'))

    return redirect(url_for('view_page'))





# Cart Page
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        user_id = None

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    
    if request.method == 'POST' and 'logout' in request.form:
        session.pop('user_id', None)
        return redirect(url_for('login'))

    # Update cart 
    if request.method == 'POST' and 'update_cart' in request.form:
        cart_id = request.form['cart_id']
        qty = request.form['qty']
        query = "UPDATE cart SET qty = %s WHERE id = %s"
        cursor.execute(query, (qty, cart_id))
        conn.commit()
        flash('Cart quantity updated successfully', 'success')

    # Delete item from cart
    if request.method == 'POST' and 'delete_item' in request.form:
        cart_id = request.form['cart_id']
        query = "DELETE FROM cart WHERE id = %s"
        cursor.execute(query, (cart_id,))
        conn.commit()
        flash('Cart item deleted successfully', 'success')

    # Empty cart
    if request.method == 'POST' and 'empty_cart' in request.form:
        query = "DELETE FROM cart WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        conn.commit()
        flash('Cart emptied successfully', 'success')

    # Get cart items
    query = "SELECT * FROM cart WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    cart_items = cursor.fetchall()

    grand_total = 0
    for item in cart_items:
        product_query = "SELECT * FROM products WHERE id = %s"
        cursor.execute(product_query, (item['product_id'],))
        product = cursor.fetchone()
        if product:
            item['product'] = product
            item['sub_total'] = item['qty'] * product['price']
            grand_total += item['sub_total']
        else:
            flash('Product not found!', 'error')

    conn.close()
    return render_template('cart.html', cart_items=cart_items, grand_total=grand_total)


# Wishlist Page
@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        user_id = None

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

   
    if request.method == 'POST' and 'logout' in request.form:
        session.pop('user_id', None)
        return redirect(url_for('login'))

    # Add to cart
    if request.method == 'POST' and 'add_to_cart' in request.form:
        product_id = request.form['product_id']
        qty = 1

        
        verify_cart = "SELECT * FROM cart WHERE user_id = %s AND product_id = %s"
        cursor.execute(verify_cart, (user_id, product_id))
        cart_item = cursor.fetchone()

        if cart_item:
            flash('Product already exists in your cart', 'warning')
        else:
            # Check if cart is full (more than 20 items)
            max_cart_items = "SELECT * FROM cart WHERE user_id = %s"
            cursor.execute(max_cart_items, (user_id,))
            cart_items = cursor.fetchall()
            if len(cart_items) > 20:
                flash('Cart is full', 'warning')
            else:
                # Add product to cart
                select_price = "SELECT price FROM products WHERE id = %s LIMIT 1"
                cursor.execute(select_price, (product_id,))
                product = cursor.fetchone()

                if product:
                    add_to_cart_query = """
                        INSERT INTO cart (user_id, product_id, price, qty) 
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(add_to_cart_query, (user_id, product_id, product['price'], qty))
                    conn.commit()
                    flash('Product added to cart successfully', 'success')

    # Delete item from wishlist
    if request.method == 'POST' and 'delete_item' in request.form:
        wishlist_id = request.form['wishlist_id']

        verify_delete = "SELECT * FROM wishlist WHERE id = %s"
        cursor.execute(verify_delete, (wishlist_id,))
        if cursor.fetchone():
            delete_wishlist_query = "DELETE FROM wishlist WHERE id = %s"
            cursor.execute(delete_wishlist_query, (wishlist_id,))
            conn.commit()
            flash('Wishlist item deleted successfully', 'success')
        else:
            flash('Wishlist item already deleted', 'warning')

    
    query = "SELECT * FROM wishlist WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    wishlist_items = cursor.fetchall()

    for item in wishlist_items:
        product_query = "SELECT * FROM products WHERE id = %s"
        cursor.execute(product_query, (item['product_id'],))
        item['product'] = cursor.fetchone()

    conn.close()
    return render_template('wishlist.html', wishlist_items=wishlist_items)


# Checkout Page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        user_id = None

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        
        if 'place_order' in request.form:
            name = request.form['name']
            number = request.form['number']
            email = request.form['email']
            address = f"{request.form['flat']}, {request.form['street']}, {request.form['city']}, {request.form['country']}, {request.form['pincode']}"
            address_type = request.form['address_type']
            method = request.form['method']
            date = datetime.today().strftime('%Y-%m-%d')
            status = 'pending'

            cursor.execute("SELECT * FROM cart WHERE user_id = %s", (user_id,))
            cart_items = cursor.fetchall()

            if request.args.get('get_id'):
                cursor.execute("SELECT * FROM products WHERE id = %s LIMIT 1", (request.args['get_id'],))
                product = cursor.fetchone()
                if product:
                    cursor.execute("""
                        INSERT INTO orders (id, user_id, name, number, email, address, address_type, method, product_id, price, qty, date, status) 
                        VALUES (UUID(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (user_id, name, number, email, address, address_type, method, product['id'], product['price'], 1,date, status))
                    conn.commit()
                    return redirect('/order')
            elif cart_items:
                for cart_item in cart_items:
                    cursor.execute("SELECT * FROM products WHERE id = %s", (cart_item['product_id'],))
                    product = cursor.fetchone()
                    if product:
                        cursor.execute("""
                            INSERT INTO orders (id, user_id, name, number, email, address, address_type, method, product_id, price, qty,date, status) 
                            VALUES (UUID(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (user_id, name, number, email, address, address_type, method, product['id'], product['price'], cart_item['qty'],date,  status))
                        conn.commit()

                cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
                conn.commit()
                return redirect('/order')

    # Calculate grand total for display
    grand_total = 0
    cart_items = []
    if request.args.get('get_id'):
        cursor.execute("SELECT * FROM products WHERE id = %s", (request.args['get_id'],))
        product = cursor.fetchone()
        if product:
            cart_items.append(product)
            grand_total += product['price']
    else:
        cursor.execute("SELECT * FROM cart WHERE user_id = %s", (user_id,))
        cart_items = cursor.fetchall()
        for cart_item in cart_items:
            cursor.execute("SELECT * FROM products WHERE id = %s", (cart_item['product_id'],))
            product = cursor.fetchone()
            if product:
                cart_item['product'] = product
                grand_total += product['price'] * cart_item['qty']

    return render_template('checkout.html', cart_items=cart_items, grand_total=grand_total)

# Order Page
@app.route('/order')
def order():
    # Check if the user is logged in
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM `orders` WHERE user_id = %s ORDER BY date DESC", (user_id,))
    orders = cursor.fetchall()

    order_list = []
    for order in orders:
        cursor.execute("SELECT * FROM `products` WHERE id = %s", (order['product_id'],))
        product = cursor.fetchone()
        if product:
            order_details = {
                'order_id': order['id'],
                'date': order['date'],
                'product_name': product['name'],
                'product_image': product['image'],
                'price': order['price'],
                'qty': order['qty'],
                'status': order['status']
            }
            order_list.append(order_details)

    cursor.close()
    conn.close()

    return render_template('order.html', orders=order_list)


# order_detail Page

@app.route('/view_order')
def view_order():
    user_id = session.get('user_id')
    get_id = request.args.get('get_id')

    if not user_id:
        return redirect(url_for('login'))

    if not get_id:
        return redirect(url_for('order'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM `orders` WHERE id = %s LIMIT 1", (get_id,))
    order = cursor.fetchone()

    if order:
        cursor.execute("SELECT * FROM `products` WHERE id = %s LIMIT 1", (order['product_id'],))
        product = cursor.fetchone()
        if product:
            grand_total = order['price'] 
       

    conn.close()
    return render_template('view_order.html', order=order, product=product, grand_total=grand_total)

@app.route('/cancel_order', methods=['POST'])
def cancel_order():
    get_id = request.form.get('order_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Update the order status to 'canceled'
    cursor.execute("UPDATE `orders` SET status = %s WHERE id = %s", ('canceled', get_id))
    conn.commit()
    conn.close()
    
    flash('Order canceled successfully')
    return redirect(url_for('order'))





# Logout Page
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    




    
    
    
    
    
    
    
    
    
    
    
    
    










    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    



