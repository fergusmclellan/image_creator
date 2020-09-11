from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont

FONT_SIZE_PX = 15
BORDER_PADDING_PX = 6
IMAGE_FONT = ImageFont.truetype('cour.ttf', FONT_SIZE_PX)

app = Flask(__name__)

@app.route('/api/add_message/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
    content = request.json
    image_text = content['mytext']

    image_filename = 'output.png'
    print("image text: " + image_text)
    print("image name: " + image_filename)

    text_pixel_width = 500
    text_pixel_height = 200

    img = Image.new('RGB', (text_pixel_width, text_pixel_height), color = ('white'))

    drawing = ImageDraw.Draw(img)
    drawing.text((BORDER_PADDING_PX, BORDER_PADDING_PX), image_text, font=IMAGE_FONT, fill=('black'))
    drawing.rectangle([(0,0), (text_pixel_width, text_pixel_height)], fill=None, outline='black',
        width=2)
    # border appears as only 1 pixel width along right and bottom sides, so draw an extra line
    drawing.line((1, text_pixel_height-2, text_pixel_width-1, text_pixel_height-2), width=1,
        fill='black')
    drawing.line((text_pixel_width-2, 1, text_pixel_width-2, text_pixel_height-1), width=1,
        fill='black')
    img.save(image_filename)

    return send_file(image_filename, mimetype='image/png')

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
