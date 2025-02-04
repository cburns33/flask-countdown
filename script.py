from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from flask import Flask, send_file
import io

app = Flask(__name__)

# Set your countdown end date
TARGET_DATE = datetime(2025, 6, 3, 0, 0, 0)

def generate_countdown_image():
    # Calculate time remaining
    now = datetime.now()
    delta = TARGET_DATE - now
    days, hours, minutes, seconds = delta.days, delta.seconds // 3600, (delta.seconds % 3600) // 60, delta.seconds % 60

    # Create blank image
    img = Image.new('RGB', (400, 100), color="#8427e2")
    draw = ImageDraw.Draw(img)
    
    # Load font (ensure path is correct)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    # Draw text
    countdown_text = f"{days}d {hours}h {minutes}m {seconds}s"
    text_size = draw.textsize(countdown_text, font=font)
    draw.text(((400 - text_size[0]) / 2, (100 - text_size[1]) / 2), countdown_text, fill="white", font=font)

    # Save image to a byte buffer
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io

@app.route('/countdown.gif')
def serve_countdown():
    return send_file(generate_countdown_image(), mimetype='image/png')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
