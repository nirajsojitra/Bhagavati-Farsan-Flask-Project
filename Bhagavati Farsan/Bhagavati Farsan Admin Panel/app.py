from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import hashlib
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Directory for profile and product image uploads
UPLOAD_FOLDER = 'static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# MySQL connection configuration
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'namkeen',
}

# Database connection setup
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Check if the uploaded file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Generate unique ID
def unique_id():
    return str(uuid.uuid4())

   

# Register Admin Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        password = hashlib.sha1(request.form['password'].encode()).hexdigest()
        cpassword = hashlib.sha1(request.form['cpassword'].encode()).hexdigest()

        if 'image' not in request.files or request.files['image'].filename == '':
            flash('Profile image is required', 'warning')
            return redirect(request.url)

        image_file = request.files['image']
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Check if email already exists
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM `admin` WHERE email = %s", (email,))
            existing_admin = cursor.fetchone()

            if existing_admin:
                flash(' email already exists', 'warning')
            elif password != cpassword:
                flash('Passwords do not match', 'warning')
            else:
                # Insert new admin
                admin_id = unique_id()
                cursor.execute("INSERT INTO `admin` (id, name, email, password, profile) VALUES (%s, %s, %s, %s, %s)",
                               (admin_id, name, email, password, filename))
                conn.commit()
                image_file.save(image_path)
                flash('New admin registered successfully!', 'success')
                return redirect(url_for('login'))

            cursor.close()
            conn.close()

    return render_template('register.html')

# Login Route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = hashlib.sha1(request.form['password'].encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `admin` WHERE email = %s AND password = %s", (email, password))
        admin = cursor.fetchone()

        if admin:
            session['admin_id'] = admin['id']
            return redirect('/dashboard')
        else:
            flash('Incorrect username or password', 'error')

        cursor.close()
        conn.close()

    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch admin profile for welcome message
    admin_id = session['admin_id']
    cursor.execute("SELECT name FROM admin WHERE id = %s", (admin_id,))
    fetch_profile = cursor.fetchone()

    # Fetch dashboard data
    cursor.execute("SELECT COUNT(*) AS num_of_products FROM products")
    num_of_products = cursor.fetchone()['num_of_products']

    cursor.execute("SELECT COUNT(*) AS num_of_active_products FROM products WHERE status = %s", ('active',))
    num_of_active_products = cursor.fetchone()['num_of_active_products']

    cursor.execute("SELECT COUNT(*) AS num_of_deactive_products FROM products WHERE status = %s", ('deactive',))
    num_of_deactive_products = cursor.fetchone()['num_of_deactive_products']

    cursor.execute("SELECT COUNT(*) AS num_of_users FROM users")
    num_of_users = cursor.fetchone()['num_of_users']

    cursor.execute("SELECT COUNT(*) AS num_of_admin FROM admin")
    num_of_admin = cursor.fetchone()['num_of_admin']

    cursor.execute("SELECT COUNT(*) AS num_of_message FROM message")
    num_of_message = cursor.fetchone()['num_of_message']

    cursor.execute("SELECT COUNT(*) AS num_of_orders FROM orders")
    num_of_orders = cursor.fetchone()['num_of_orders']

    cursor.execute("SELECT COUNT(*) AS num_of_confirm_orders FROM orders WHERE status = %s", ('complete',))
    num_of_confirm_orders = cursor.fetchone()['num_of_confirm_orders']

    cursor.execute("SELECT COUNT(*) AS num_of_canceled_orders FROM orders WHERE status = %s", ('canceled',))
    num_of_canceled_orders = cursor.fetchone()['num_of_canceled_orders']

    cursor.close()
    conn.close()

    return render_template(
        'dashboard.html',
        fetch_profile=fetch_profile,
        num_of_products=num_of_products,
        num_of_active_products=num_of_active_products,
        num_of_deactive_products=num_of_deactive_products,
        num_of_users=num_of_users,
        num_of_admin=num_of_admin,
        num_of_message=num_of_message,
        num_of_orders=num_of_orders,
        num_of_confirm_orders=num_of_confirm_orders,
        num_of_canceled_orders=num_of_canceled_orders
    )

# Add Product Route
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'admin_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        wheight = request.form['wheight']
        price = request.form['price']
        content = request.form['content']
        status = 'active' if 'publish' in request.form else 'deactive'

        image = request.files['image']
        image_name = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM products WHERE image = %s", (image_name,))
        if cursor.fetchone():
            flash('Image name already exists', 'warning')
        elif image and image.content_length > 2000000:
            flash('Image size is too large', 'warning')
        else:
            image.save(image_path)
            cursor.execute("""
                INSERT INTO products (id, name,wheight, price, image, product_details, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (unique_id(), name, wheight, price, image_name, content, status))
            conn.commit()
            flash(f'Product {"published" if status == "active" else "saved as draft"} successfully!', 'success')

        cursor.close()
        conn.close()

    return render_template('add_product.html')

# View Product Route
@app.route('/view_product', methods=['GET', 'POST'])
def view_product():
    if 'admin_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        product_id = request.form['product_id']

        # Delete product
        cursor.execute("DELETE FROM `products` WHERE id = %s", (product_id,))
        conn.commit()

        flash('Product deleted successfully!', 'success')

    # Fetch all products
    cursor.execute("SELECT * FROM `products`")
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('view_product.html', products=products)

# View deactive Product Route
@app.route('/deactive', methods=['GET', 'POST'])
def deactive():
    if 'admin_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        product_id = request.form['product_id']

        # Delete product
        cursor.execute("DELETE FROM `products` WHERE id = %s", (product_id,))
        conn.commit()

        flash('Product deleted successfully!', 'success')

    # Fetch all products
    cursor.execute("SELECT * FROM `products`")
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('deactive.html', products=products)    

# View active Product Route
@app.route('/active', methods=['GET', 'POST'])
def active():
    if 'admin_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        product_id = request.form['product_id']

        # Delete product
        cursor.execute("DELETE FROM `products` WHERE id = %s", (product_id,))
        conn.commit()

        flash('Product deleted successfully!', 'success')

    # Fetch all products
    cursor.execute("SELECT * FROM `products`")
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('active.html', products=products)    

# View Users (User Account Page)
@app.route('/user_account')
def user_account():
    if 'admin_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('user_account.html', users=users)

# Admin Account Page (View All Admins)
@app.route('/admin_account')
def admin_account():
    if 'admin_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM `admin`")
    admins = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('admin_account.html', admins=admins)

# Admin Messages Page
@app.route('/admin_message', methods=['GET', 'POST'])
def admin_message():
    if 'admin_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST' and 'delete' in request.form:
        delete_id = request.form.get('delete_id')
        cursor.execute("DELETE FROM `message` WHERE id = %s", (delete_id,))
        conn.commit()
        flash('Message deleted successfully!', 'success')

    cursor.execute("SELECT * FROM `message`")
    messages = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_message.html', messages=messages)

# Orders Page
@app.route('/order', methods=['GET', 'POST'])
def order():
    if 'admin_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # dictionary=True returns rows as dictionaries

    if request.method == 'POST':
        order_id = request.form.get('order_id')

        # Delete order logic
        if 'delete_order' in request.form:
            if order_id:
                # Verify if the order exists
                cursor.execute('SELECT * FROM orders WHERE id = %s', (order_id,))
                verify_delete = cursor.fetchone()
                if verify_delete:
                    cursor.execute('DELETE FROM orders WHERE id = %s', (order_id,))
                    conn.commit()
                    flash('Order deleted successfully', 'success')
                else:
                    flash('Order already deleted or does not exist', 'warning')

        # Update order logic
        if 'update_order' in request.form:
            update_payment = request.form.get('update_payment')
            if order_id and update_payment:
                # Update payment status
                cursor.execute('UPDATE orders SET payment_status = %s WHERE id = %s', (update_payment, order_id))
                conn.commit()
                flash('Order payment status updated successfully', 'success')

                cursor.execute('UPDATE orders SET status = %s WHERE id = %s', (update_payment, order_id))
                conn.commit()
                flash('Order payment status updated successfully', 'success')



                
    # Fetch confirmed orders
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    
    conn.close()

    return render_template('order.html', orders=orders)


# complete_order

@app.route('/complete_order', methods=['GET', 'POST'])
def complete_order():
    if 'admin_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # dictionary=True returns rows as dictionaries

    if request.method == 'POST':
        order_id = request.form.get('order_id')

        # Delete order logic
        if 'delete_order' in request.form:
            if order_id:
                # Verify if the order exists
                cursor.execute('SELECT * FROM orders WHERE id = %s', (order_id,))
                verify_delete = cursor.fetchone()
                if verify_delete:
                    cursor.execute('DELETE FROM orders WHERE id = %s', (order_id,))
                    conn.commit()
                    flash('Order deleted successfully', 'success')
                else:
                    flash('Order already deleted or does not exist', 'warning')

        # Update order logic
        if 'update_order' in request.form:
            update_payment = request.form.get('update_payment')
            if order_id and update_payment:
                # Update payment status
                cursor.execute('UPDATE orders SET payment_status = %s WHERE id = %s', (update_payment, order_id))
                conn.commit()
                flash('Order payment status updated successfully', 'success')

                
    # Fetch confirmed orders
    cursor.execute("SELECT * FROM orders WHERE status = 'complete'")
    orders = cursor.fetchall()
    
    conn.close()

    return render_template('complete_order.html', orders=orders) 

# cancel_order

@app.route('/cancel_order', methods=['GET', 'POST'])
def cancel_order():
    if 'admin_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if admin is not logged in

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Use dictionary=True to get results as dictionaries

    if request.method == 'POST':
        order_id = request.form.get('order_id')

        # Delete Order Logic
        if 'delete_order' in request.form:
            if order_id:
                cursor.execute('SELECT * FROM orders WHERE id = %s', (order_id,))
                order = cursor.fetchone()
                if order:
                    cursor.execute('DELETE FROM orders WHERE id = %s', (order_id,))
                    conn.commit()
                    flash('Order deleted successfully', 'success')
                else:
                    flash('Order already deleted or does not exist', 'warning')

        # Update Order Logic
        elif 'update_order' in request.form:
            update_payment = request.form.get('update_payment')
            if order_id and update_payment:
                # Update payment status
                cursor.execute('UPDATE orders SET payment_status = %s WHERE id = %s', (update_payment, order_id))
                conn.commit()

                
                flash('Order updated successfully', 'success')

    # Fetch all confirmed orders to display
    cursor.execute("SELECT * FROM orders WHERE status = 'canceled'")
    orders = cursor.fetchall()
    
    conn.close()

    return render_template('cancel_order.html', orders=orders)


# Route for reading a product
@app.route('/read_product/<post_id>', methods=['GET', 'POST'])
def read_product(post_id):
    # Check if the user is logged in as an admin
    admin_id = session.get('admin_id')
    if not admin_id:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch product data
    cursor.execute("SELECT * FROM products WHERE id = %s", (post_id,))
    product = cursor.fetchone()

    if request.method == 'POST' and 'delete' in request.form:
        product_id = request.form.get('product_id')

        # Fetch product image to delete
        cursor.execute("SELECT image FROM products WHERE id = %s", (product_id,))
        fetch_delete_image = cursor.fetchone()

        # Delete image from filesystem if exists
        if fetch_delete_image and fetch_delete_image['image']:
            image_path = os.path.join('static', 'img', fetch_delete_image['image'])
            if os.path.exists(image_path):
                os.remove(image_path)

        # Delete product from the database
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        flash("Product deleted successfully", "success")
        return redirect(url_for('view_product'))

    conn.close()
    return render_template('read_product.html', product=product)


@app.route('/edit_product/<id>', methods=['GET', 'POST'])
def edit_product(id):
    # Check if the user is logged in as an admin
    admin_id = session.get('admin_id')
    if not admin_id:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch product details
    cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    product = cursor.fetchone()

    if not product:
        flash("Product not found", "error")
        return redirect(url_for('view_product'))

    if request.method == 'POST':
        if 'update' in request.form:
            # Update product details
            name = request.form['name']
            price = request.form['price']
            content = request.form['content']
            status = request.form.get('status', '')

            cursor.execute("""
                UPDATE products SET name = %s, price = %s, product_details = %s, status = %s WHERE id = %s
            """, (name, price, content, status, id))
            conn.commit()

            # Handle image update
            old_image = request.form.get('old_image')
            image = request.files.get('image')
            if image:
                image_path = os.path.join('static/img', image.filename)
                image.save(image_path)

                # Update database with new image name
                cursor.execute("UPDATE products SET image = %s WHERE id = %s", (image.filename, id))
                conn.commit()

                # Delete the old image if a new one was uploaded
                if old_image and old_image != image.filename:
                    old_image_path = os.path.join('static/img', old_image)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

            flash("Product updated successfully", "success")
            return redirect(url_for('view_product'))

        elif 'delete' in request.form:
            # Delete product
            cursor.execute("SELECT image FROM products WHERE id = %s", (id,))
            product = cursor.fetchone()
            if product and product['image']:
                image_path = os.path.join('static/img', product['image'])
                if os.path.exists(image_path):
                    os.remove(image_path)

            cursor.execute("DELETE FROM products WHERE id = %s", (id,))
            conn.commit()

            flash("Product deleted successfully", "success")
            return redirect(url_for('view_product'))

    conn.close()
    return render_template('edit_product.html', product=product)





    
         

if __name__ == '__main__':
    app.run(debug=True)
















