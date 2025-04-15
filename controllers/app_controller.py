from flask import jsonify, abort

def get_home(req):
    return "Welcome to the Food Recomendation Home Page"