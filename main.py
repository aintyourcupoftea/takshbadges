from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
from datetime import datetime
import io
from base64 import b64encode
from flask_cors import CORS

app = Flask(_name_)
CORS(app, resources={r"/*": {"origins": "https://www.khojcommunity.com"}}) 

def add_text_to_badge(username):
    badge_temp = ['./badges/1.png', './badges/2.png', './badges/3.png', './badges/4.png', './badges/5.png']
    image_path = random.choice(badge_temp)

    with Image.open(image_path) as img:
        txt = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)

        username_font_size = 55
        tagline_font_size = 30
        date_font_size = 30
        username_font = ImageFont.truetype("./fonts/Merriweather-Bold.ttf", username_font_size)
        tagline_font = ImageFont.truetype("./fonts/Poppins-MediumItalic.ttf", tagline_font_size)
        date_font = ImageFont.truetype("./fonts/Poppins-Medium.ttf", date_font_size)

        x = 60
        username_y = 560 if image_path == './badges/1.png' else 580
        tagline_y = username_y + username_font_size + 25
        date_y = img.height - (100 if image_path == './badges/1.png' else 94)

        draw.text((x, username_y), username, font=username_font, fill=(255, 255, 255) if image_path == './badges/1.png' else (0, 0, 0))
        shadow = txt.filter(ImageFilter.GaussianBlur(radius=2))
        img = Image.alpha_composite(img.convert('RGBA'), shadow)
        img = Image.alpha_composite(img, txt)

        final_draw = ImageDraw.Draw(img)

        tag_list = ['Future Innovator', 'Champion', 'Tech Trailblazer', 'Ultra Pro Max Learner',
                    'Project Prodigy', 'Young Visionary', 'Curious', 'legend']
        tagline = random.choice(tag_list)
        final_draw.text((x, tagline_y), tagline, font=tagline_font, fill=(255, 255, 255) if image_path == './badges/1.png' else (0, 0, 0))

        current_date = datetime.now().strftime("%d %b %Y")
        final_draw.text((x + (15 if image_path == './badges/1.png' else 7), date_y), current_date, font=date_font, fill=(0, 0, 0) if image_path == './badges/1.png' else (255, 255, 255))

        # Convert image to Base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = b64encode(buffered.getvalue()).decode()

        return f"data:image/png;base64,{img_str}" 

@app.route('/gen_badge', methods=['POST'])
def generate_badge():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400

    badge_image_data = add_text_to_badge(username)
    return jsonify({"image_data": badge_image_data})

if _name_ == '_main_':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
