from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def check_google_sheet(link):
    prefixes = ["https://","http://"]
    for pre in prefixes:
        link = link.strip(pre)
        if link.startswith("docs.google.com"):
            parts = str(link).split("/")
            if parts[1] == "spreadsheets" and parts[2] == "d":
                data = {
                    "vailidity" : True
                }
                return jsonify(data)
            else:
                data = {
                    "vailidity" : False
                }
                return jsonify(data)
        else:
            data = {
                "vailidity" : False
            }
            return jsonify(data)


@app.route('/')
def home():
    return 'Welcome to the popquest API'

@app.route('/checksheet', methods=['GET'])
def validate():
    link = request.args.get('link')
    return check_google_sheet(link)

@app.route('/test')
def test():
    response = requests.get("https://www.instructables.com/HyperDuino-based-CubeSat/")
    return response.text


# for local dev only
if __name__ == '__main__':
    app.run()