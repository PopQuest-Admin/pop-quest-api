from flask import Flask, request, jsonify, send_file, send_from_directory
import requests
from PIL import Image, ImageDraw, ImageFont, ImageColor
import io

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

@app.route('/generate_button', methods=['GET'])
def generate():
    text = request.args.get('button')
    bg_image_width = 697
    bg_image_height = 135
    font_size = 85
    font_path = "./font.ttf"
    # output_file = "output1.png"
    # color = (236,75,104)\
    color = ImageColor.getrgb("rgb(236, 75, 104)")
    # color = (236, 75, 104, 255)
    hex_color = "#EC4B68"
    color_int = int(hex_color.lstrip('#'), 16)
    bg_img = "./bg.png"

    if len(text) > 10:
        raise ValueError("Text exceeds the maximum limit of 10 characters.")

    image = Image.open(bg_img)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("ERROR FONT FILE FOUND")

    # text_width, text_height = draw.textlength(text, font=font)
    text_width = draw.textlength(text, font=font)
    text_height = font_size * 1
    x_position = (bg_image_width - text_width) // 2
    y_position = (bg_image_height - text_height) // 2

    draw.text((x_position, y_position), text, "blue", font=font)

    # image.save(output_file)
    # image.save(f"./static/{output_file}")


    # image_bytes = io.BytesIO()
    # image_data = image_bytes.getvalue()
    # return send_file(image_data,mimetype='image/png')
    # return send_file(io.BytesIO(image),mimetype='image/jpeg')
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)  # Reset file pointer to the beginning
    return send_file(image_bytes, mimetype='image/png')

@app.route('/test')
def test():
    return "Welcome to the /test endpoint !!!"

@app.route('/image')
def ima():
    return send_file("output.png", mimetype='image/png')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run()