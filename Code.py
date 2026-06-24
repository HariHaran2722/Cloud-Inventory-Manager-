from flask import Flask,request,jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    return conn

def init_db():
    conn =get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT,
                   productname TEXT NOT NULL,
                   category TEXT NOT NULL, 
                   price REAL NOT NULL, 
                   quantity INTEGER NOT NULL)''')
    conn.commit()   
    conn.close()

@app.route('/')
def home():
    return "Cloud Database Manager using Flask"

@app.route('/products',methods=['POST'])
def add_product():
    data = request.json
    productname = data["productname"]
    category = data["category"]
    price = data["price"]
    quantity =data["quantity"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO products 
                   (productname,category,price,quantity)
                   VALUES(?,?,?,?)''',(productname,category,price,quantity))
    conn.commit()
    conn.close()
    return jsonify({"message":"Product added successfully"})

@app.route('/products/<int:id>',methods=['PUT'])
def up_product(id):
    data=request.json
    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute('''UPDATE products 
                SET quantity = ? 
                WHERE id = ?''',(data['quantity'],id))
    conn.commit()
    conn.close()
    return jsonify({'message' : 'Stock updated Successfully'})

@app.route('/products/<int:id>',methods=['DELETE'])
def delete_product(id):
    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute('''DELETE FROM products
                 WHERE id = ?''',
                 (id,))
    conn.commit()
    conn.close()
    return jsonify({'message' : 'Product deleted Successfully'})

@app.route('/product-count',methods=['GET'])
def productcount():
    conn = get_db_connection()
    cur = conn.cursor()
    count=cur.execute('''SELECT COUNT(*) FROM products''').fetchone()
    conn.close()
    return jsonify ({'total-products':count[0]})


@app.route('/low-stock',methods=['GET'])
def low_stock():
    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute('''SELECT * FROM products WHERE quantity < 10''')
    products=cur.fetchall()
    result=[]
    for product in products:
        result.append({
            'id': product[0],
            'productname': product[1],
            'category': product[2],
            'price': product[3],
            'quantity': product[4]
        })  
    conn.close()
    return jsonify(result)

@app.route('/products/search/<string:name>',methods=['GET'])
def search_product(name):
    conn=get_db_connection()
    cur=conn.cursor()
    product=cur.execute('''SELECT * FROM products WHERE productname LIKE ?''',(name,)).fetchone()
    conn.close()
    if product:
        return jsonify({
            'id': product[0],
            'productname': product[1],
            'category': product[2],
            'price': product[3],
            'quantity': product[4]
        })  
    else:
        return jsonify({'message':'Product not found'})                            

@app.route('/inventory-value',methods=['GET'])
def inventory_value():
    conn=get_db_connection()
    cur=conn.cursor()
    total_value=cur.execute('''SELECT SUM(price * quantity) FROM products''').fetchone()
    conn.close()
    return jsonify({'total-inventory-value':total_value[0]})

@app.route('/products/category/<string:category>',methods=['GET'])
def get_products_by_category(category):
    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute('''SELECT * FROM products WHERE category = ?''',(category,))
    products=cur.fetchall()
    result=[]
    for product in products:
        result.append({
            'id': product[0],
            'productname': product[1],
            'category': product[2],
            'price': product[3],
            'quantity': product[4]
        })
    conn.close()
    return jsonify(result)

init_db()
if __name__=='__main__':
    app.run(debug=True , port=5006)