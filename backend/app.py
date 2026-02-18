# ------------------- Imports -------------------

from flask import Flask, request, jsonify
from db import create_db_connection
import jwt
from functools import wraps
from flask import request, jsonify

# ------------------- Flask App -------------------

app = Flask(__name__)
SECRET_KEY = "your_secret_here"

# ------------------- INPUT SANITIZATION -------------------
def sanitize_input(text):
    if not text:
        return ""
    # Remove HTML tags to prevent XSS
    return re.sub(r'<[^>]*?>', '', str(text))

# ------------------- JWT Decorator --------------------

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['username']
        except:
            return jsonify({"message": "Token is invalid!"}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# ------------------- Home route -------------------
@app.route("/")
def home():
    return "Park Ranger API Running ~ Phase 2"

# ------------------- USERS -------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = sanitize_input(data.get("username"))
    password = sanitize_input(data.get("password"))

    conn = create_db_connection()
    if not conn:
        return jsonify({"status": "db connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM USER WHERE username=%s AND password_hash=%s", 
        (username, password)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        token = jwt.encode({"username": username}, SECRET_KEY, algorithm="HS256")
        return jsonify({"status": "success", "token": token})
    
    return jsonify({"status": "failed"}), 401


# ------------------- PRODUCTS -------------------
@app.route("/products", methods=["POST"])
@token_required
def add_product(current_user):
    data = request.json
    name = sanitize_input(data.get("product_name"))
    tier = sanitize_input(data.get("performance_tier", ""))
    rate = float(data.get("sentiment_rate", 0))

    conn = create_db_connection()
    if not conn:
        return jsonify({"status": "db connection failed"}), 500

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO PRODUCT (product_name, performance_tier, sentiment_rate) VALUES (%s,%s,%s)",
        (name, tier, rate)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "product added"})

@app.route("/products", methods=["GET"])
def get_products():
    conn = create_db_connection()
    if not conn:
        return jsonify({"status": "db connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM PRODUCT")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(products)

@app.route("/products/<int:product_id>", methods=["PUT"])
@token_required
def edit_product(current_user, product_id):
    data = request.json
    name = sanitize_input(data.get("product_name"))
    tier = sanitize_input(data.get("performance_tier"))
    rate = float(data.get("sentiment_rate", 0))

    conn = create_db_connection()
    if not conn:
        return jsonify({"status": "db connection failed"}), 500

    cursor = conn.cursor()
    cursor.execute(
        "UPDATE PRODUCT SET product_name=%s, performance_tier=%s, sentiment_rate=%s WHERE product_id=%s",
        (name, tier, rate, product_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "product updated"})

@app.route("/products/<int:product_id>", methods=["DELETE"])
@token_required
def delete_product(current_user, product_id):
    conn = create_db_connection()
    if not conn:
        return jsonify({"status": "db connection failed"}), 500

    cursor = conn.cursor()
    cursor.execute("DELETE FROM PRODUCT WHERE product_id=%s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "product deleted"})

# ------------------- FEEDBACK (Basic Orders) -------------------
@app.route("/feedback", methods=["POST"])
@token_required
def add_feedback(current_user):
    data = request.json
    loc_id = data.get("location_id")
    prod_id = data.get("product_id")
    src_id = data.get("source_id")
    text = sanitize_input(data.get("feedback_text"))
    label = sanitize_input(data.get("sentiment_label", ""))
    score = float(data.get("sentiment_score", 0))

    conn = create_db_connection()
    if not conn:
        return jsonify({"status": "db connection failed"}), 500

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO FEEDBACK (location_id, product_id, source_id, feedback_text, sentiment_label, sentiment_score) VALUES (%s,%s,%s,%s,%s,%s)",
        (loc_id, prod_id, src_id, text, label, score)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "feedback added"})

@app.route("/feedback", methods=["GET"])
def get_feedback():
    conn = create_db_connection()
    if not conn:
        return jsonify({"status": "db connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM FEEDBACK")
    feedbacks = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(feedbacks)

# ------------------- LOCATIONS -------------------
@app.route('/locations', methods=['GET'])
def get_locations():
    conn = create_db_connection()
    if not conn:
        return jsonify({"status": "db connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM LOCATION")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)


# ------------------- RUN SERVER -------------------
if __name__ == "__main__":
    app.run(debug=True)