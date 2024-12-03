from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def check_google_sheet(link):
    try:
        prefixes = ["https://","http://"]
        for pre in prefixes:
            link = link.strip(pre)
            if link.startswith("docs.google.com"):
                parts = str(link).split("/")
                if parts[1] == "spreadsheets" and parts[2] == "d":
                    return True
                else:
                    return False
            else:
                return False
    except:
        return "ERROR IN : check google sheet func"
        

def read_google_sheet(url, api_key):
    try:
        parts = str(url).split('/')
        sheet_id = parts[5]
        sheet_name = "Sheet1"
        template_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{sheet_name}!A1:Z?alt=json&key={api_key}"
        response  = requests.get(template_url)

        data = response.json()
        return data
    
    except:
        return "Error occured"

@app.route('/')
def home():
    return 'Welcome to the popquest API'

@app.route('/checksheet', methods=['GET'])
def validate():
    link = request.args.get('link')
    data = {
        "validity" : check_google_sheet(link)
    }
    return jsonify(data)

@app.route('/readsheet', methods=['GET'])
def readdata():
    sheet_url = request.args.get('url')
    api_key = request.args.get('api_key')
    
    return jsonify(read_google_sheet(sheet_url,api_key))

@app.route('/test')
def test():
    return "Welcome to the test route"


if __name__ == '__main__':
    app.run()