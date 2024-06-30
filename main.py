from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
from datetime import datetime
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://www.khojcommunity.com"}})

def add_text_to_badge(username):
    badge_temp = ['./badges/1.png','./badges/2.png', './badges/3.png', './badges/4.png', './badges/5.png']
    image_path = random.choice(badge_temp)  
    
    if image_path != './badges/1.png':
        with Image.open(image_path) as img:
            txt = Image.new('RGBA', img.size, (255,255,255,0))
            draw = ImageDraw.Draw(txt)

            username_font_size = 55
            tagline_font_size = 30
            date_font_size = 30
            username_font = ImageFont.truetype("./fonts/Merriweather-Bold.ttf", username_font_size)
            tagline_font = ImageFont.truetype("./fonts/Poppins-MediumItalic.ttf", tagline_font_size)
            date_font = ImageFont.truetype("./fonts/Poppins-Medium.ttf", date_font_size)

            x = 60
            username_y = 580
            tagline_y = username_y + username_font_size + 25
            date_y = img.height - 94

            draw.text((x, username_y), username, font=username_font, fill=(0,0,0))
            shadow = txt.filter(ImageFilter.GaussianBlur(radius=2))
            img = Image.alpha_composite(img.convert('RGBA'), shadow)
            img = Image.alpha_composite(img, txt)

            final_draw = ImageDraw.Draw(img)

            tag_list = ['Future Innovator', 'Champion', 'Tech Trailblazer', 'Ultra Pro Max Learner',
                        'Project Prodigy', 'Young Visionary', 'Curious', 'legend']
            tagline = random.choice(tag_list)
            final_draw.text((x, tagline_y), tagline, font=tagline_font, fill=(0,0,0))

            current_date = datetime.now().strftime("%d %b %Y")
            final_draw.text((x+7, date_y), current_date, font=date_font, fill=(255,255,255))

            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            return img_byte_arr
    else: # The Amount of Laziness here is just beautiful 🙄...
            with Image.open(image_path) as img:
                txt = Image.new('RGBA', img.size, (255,255,255,0))
                draw = ImageDraw.Draw(txt)

                username_font_size = 55
                tagline_font_size = 30
                date_font_size = 30
                username_font = ImageFont.truetype("./fonts/Merriweather-Bold.ttf", username_font_size)
                tagline_font = ImageFont.truetype("./fonts/Poppins-MediumItalic.ttf", tagline_font_size)
                date_font = ImageFont.truetype("./fonts/Poppins-Medium.ttf", date_font_size)

                x = 60
                username_y = 560
                tagline_y = username_y + username_font_size + 25
                date_y = img.height - 100

                draw.text((x, username_y), username, font=username_font, fill=(255,255,255))
                shadow = txt.filter(ImageFilter.GaussianBlur(radius=2))
                img = Image.alpha_composite(img.convert('RGBA'), shadow)
                img = Image.alpha_composite(img, txt)

                final_draw = ImageDraw.Draw(img)

                tag_list = ['Future Innovator', 'Champion', 'Tech Trailblazer', 'Ultra Pro Max Learner',
                            'Project Prodigy', 'Young Visionary', 'Curious', 'legend']
                tagline = random.choice(tag_list)
                final_draw.text((x, tagline_y), tagline, font=tagline_font, fill=(255,255,255))

                current_date = datetime.now().strftime("%d %b %Y")
                final_draw.text((x+15, date_y), current_date, font=date_font, fill=(0,0,0))

                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                return img_byte_arr

@app.route('/gen_badge', methods=['POST'])
def generate_badge():
    data = request.json
    username = data.get('username')
    if not username:
        return "Username is required", 400

    badge_image = add_text_to_badge(username)
    return send_file(badge_image, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
