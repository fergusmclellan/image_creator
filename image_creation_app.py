from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
from codetext import CodeText

FONT_HEIGHT_SIZE_PX = 15
FONT_WIDTH_SIZE_PX = 9
LINE_SPACING_PX = 2
BORDER_PADDING_PX = 6
MAX_WIDTH_PX = 950
MAX_HEIGHT_PX = 600
IMAGE_FONT = ImageFont.truetype('cour.ttf', FONT_HEIGHT_SIZE_PX)


app = Flask(__name__)

def find_lines_and_width(text):
    max_width = 0
    no_of_lines = 0
    lines = text.split('\n')
    for line in lines:
        no_of_lines += 1
        length = len(line)
        if length > max_width:
            max_width = length

    if no_of_lines == 0:
        no_of_lines = 1
    return max_width, no_of_lines

@app.route('/api/create_image/<uuid>', methods=['GET', 'POST'])
def create_image(uuid):
    content = request.json
    max_width, no_of_lines = find_lines_and_width(content['code_text'])
    #print("max width: " + str(max_width))
    #print("max lines: " + str(no_of_lines))
    my_code = CodeText(content['code_text'], max_width, no_of_lines)
    image_filename = 'output.png'

    my_code.width_pixels = (my_code.width * FONT_WIDTH_SIZE_PX) + (BORDER_PADDING_PX * 2)
    my_code.height_pixels = ((my_code.lines - 1) * (FONT_HEIGHT_SIZE_PX + LINE_SPACING_PX)) + FONT_HEIGHT_SIZE_PX + (BORDER_PADDING_PX * 2)

    if my_code.width_pixels > MAX_WIDTH_PX:
        my_code.state = "TOO WIDE!"
    elif my_code.height_pixels > MAX_HEIGHT_PX:
        my_code.state = "TOO MANY LINES!"

    if my_code.state != "OK":
        my_code.text = my_code.state
        my_code.width_pixels = 160
        my_code.height_pixels = 50

    img = Image.new('RGB', (my_code.width_pixels, my_code.height_pixels), color = ('white'))

    drawing = ImageDraw.Draw(img)
    drawing.text((BORDER_PADDING_PX, BORDER_PADDING_PX), my_code.text, font=IMAGE_FONT, fill=('black'))
    drawing.rectangle([(0,0), (my_code.width_pixels, my_code.height_pixels)], fill=None, outline='black',width=2)
    # border appears as only 1 pixel width along right and bottom sides, so draw an extra line
    drawing.line((1, my_code.height_pixels-2, my_code.width_pixels-1, my_code.height_pixels-2), width=1, fill='black')
    drawing.line((my_code.width_pixels-2, 1, my_code.width_pixels-2, my_code.width_pixels-1), width=1, fill='black')
    img.save(image_filename)

    return send_file(image_filename, mimetype='image/png')

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
