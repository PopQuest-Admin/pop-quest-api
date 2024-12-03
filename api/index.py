from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/checksheet', methods=['GET'])
def validate():
    link = request.args.get('link')
    return f"link retuned : {link}"

@app.route('/test')
def test():
    response = requests.get("https://www.instructables.com/HyperDuino-based-CubeSat/")
    return response.text


# for local dev only
# if __name__ == '__main__':
#     app.run()