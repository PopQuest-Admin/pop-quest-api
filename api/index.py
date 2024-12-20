from flask import Flask, request, jsonify, send_file, send_from_directory
import requests
from PIL import Image, ImageDraw, ImageFont, ImageColor
import io
import json

app = Flask(__name__, static_folder='static')

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

def read_google_sheet(url, api_key):
    try:
        parts = str(url).split("/")
        sheet_id = parts[5]
        sheet_name = "Sheet1"
        template_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{sheet_name}!A1:Z?alt=json&key={api_key}"
        response = requests.get(template_url)
        data = response.json()

        source = data["values"]
        source.pop(0)

        return_data = {}
        return_data["count"] = len(source)

        counter = 1
        for item in source:
            key = f"{str(counter)}"
            value = {
                "question": item[0],
                "choice1": item[1],
                "choice2": item[2],
                "choice3": item[3],
                "choice4": item[4],
                "answer": item[1],
            }
            return_data[key] = value
            counter += 1
        #json_data = json.dumps(return_data)
        return return_data
    
    except:
        return "Error occurred"

@app.route('/readsheet', methods=['GET'])
def readdata():
    sheet_url = request.args.get('url')
    api_key = request.args.get('api_key')
    
    return jsonify(read_google_sheet(sheet_url,api_key))

@app.route('/generate_button', methods=['GET'])
def generate():
    text = request.args.get('button')
    bg_image_width = 697
    bg_image_height = 135
    font_size = 85
    font_path = "./font.ttf"
    color = ImageColor.getrgb("rgb(236, 75, 104)")
    bg_img = "./bg.png"

    if len(text) > 10:
        raise ValueError("Text exceeds the maximum limit of 10 characters.")

    image = Image.open(bg_img)
    image = image.convert("RGB")
    draw = ImageDraw.Draw(image)


    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("ERROR FONT FILE FOUND")

    text_width = draw.textlength(text, font=font)
    text_height = font_size * 1
    x_position = (bg_image_width - text_width) // 2
    y_position = (bg_image_height - text_height) // 2
    draw.text((x_position, y_position), text,  (236,75,104), font=font)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    
    return send_file(image_bytes, mimetype='image/png')

@app.route('/test')
def test():
    return "Welcome to the /test endpoint !!!"


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run()