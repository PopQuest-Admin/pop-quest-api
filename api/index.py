from flask import Flask, request, jsonify
import requests
import utils

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the popquest API'

@app.route('/websrc', methods=['GET'])
def about():
    website = request.args.get('web')
    src = utils.websrc(website)
    return src

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