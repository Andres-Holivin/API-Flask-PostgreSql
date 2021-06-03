from run import app
from flask import jsonify

@app.route('/home',methods=['GET'])
def Home():
    return jsonify({"nama":"hello"})