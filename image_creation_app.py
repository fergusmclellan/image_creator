from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
from codetext import CodeText
import re

FONT_HEIGHT_SIZE_PX = 15
FONT_WIDTH_SIZE_PX = 9
LINE_SPACING_PX = 2
BORDER_PADDING_PX = 6
OPTION_LINE_PADDING_PX = 6
MAX_WIDTH_PX = 950
MAX_DND_WIDTH_PX = 790
MAX_HEIGHT_PX = 600
IMAGE_FONT = ImageFont.truetype('cour.ttf', FONT_HEIGHT_SIZE_PX)


app = Flask(__name__)

def find_lines_and_width(text):
    """
    return the number of lines of text, and the maximum number of characters (including whitespace) found in any line
    """
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

def no_of_target_or_item_lines(text):
    """
    count the number of lines which require extra padding for item boxes or DnD targets
    """
    no_of_padded_lines = 0
    text_by_lines = text.split('\n')
    for line in text_by_lines:
        if '  item ' in line or '  target' in line:
            no_of_padded_lines += 1
    return no_of_padded_lines

@app.route('/api/create_image/<uuid>', methods=['GET', 'POST'])
def create_image(uuid):
    content = request.json
    initial_text = content['code_text']
    target_width, target_no_of_lines = find_lines_and_width(content['target_text'])
    print(content['target_text'])
    print("target max width: " + str(target_width))
    print("target max lines: " + str(target_no_of_lines))

    padding_text = max(0,(target_width - 5))
    replacement_target_text = "  target" + ('_' * padding_text) + "  "
    print(replacement_target_text)
    new_text = re.sub('\s\starget\s\s', replacement_target_text, initial_text, flags=re.DOTALL)
    print(new_text)
    max_width, no_of_lines = find_lines_and_width(new_text)
    my_code = CodeText(new_text, max_width, no_of_lines)
    image_filename = 'output.png'
    print(my_code.text)
    
    # check for " item X ", where X is a number, or for "  target  ". Text must be surrounded by 2x spaces either side
    item_target_pattern = re.compile(r'\s\sitem\s[0-9]*\s\s')
    dnd_target_pattern = re.compile(r'\s\starget')
    no_of_items = len(item_target_pattern.findall(my_code.text))
    no_of_targets = len(dnd_target_pattern.findall(my_code.text))
    if no_of_items > 0:
        my_code.no_of_padded_lines = no_of_target_or_item_lines(my_code.text)
    elif no_of_targets > 0:
        my_code.no_of_padded_lines = no_of_target_or_item_lines(my_code.text)

    print("padding for option lines:" + str(OPTION_LINE_PADDING_PX))
    print("no of padded lines:" + str(my_code.no_of_padded_lines))
    my_code.width_pixels = (my_code.width * FONT_WIDTH_SIZE_PX) + (BORDER_PADDING_PX * 2)
    my_code.height_pixels = (my_code.lines * (FONT_HEIGHT_SIZE_PX + LINE_SPACING_PX)) + (BORDER_PADDING_PX * 2) + (my_code.no_of_padded_lines * (2 *  OPTION_LINE_PADDING_PX))

    if no_of_targets > 0 and my_code.width_pixels > MAX_DND_WIDTH_PX:
        my_code.state = "DND TOO WIDE!"
    elif my_code.width_pixels > MAX_WIDTH_PX:
        my_code.state = "TOO WIDE!"
    elif my_code.height_pixels > MAX_HEIGHT_PX:
        my_code.state = "TOO MANY LINES!"

    if my_code.state != "OK":
        my_code.text = my_code.state
        my_code.width_pixels = 160
        my_code.height_pixels = 50

    print("image width:" + str(my_code.width_pixels))
    print("image height:" + str(my_code.height_pixels))
    text_start_height = BORDER_PADDING_PX
    img = Image.new('RGB', (my_code.width_pixels, my_code.height_pixels), color = ('white'))
    
    drawing = ImageDraw.Draw(img)
    text_by_lines = my_code.text.split('\n')
    for line in text_by_lines:
        print(line)
        print(text_start_height)
        item_targets = item_target_pattern.findall(line)
        dnd_targets = dnd_target_pattern.findall(line)
        if (len(item_targets) > 0) or (len(dnd_targets) > 0):
            box_y_start_pos = text_start_height + 3
            print("box_y_start_pos:" + str(box_y_start_pos))
            text_start_height = text_start_height + OPTION_LINE_PADDING_PX
            print("text_start_height:" + str(text_start_height))
            drawing.text((BORDER_PADDING_PX, text_start_height), line, font=IMAGE_FONT, fill=('black'))
            text_start_height = text_start_height + FONT_HEIGHT_SIZE_PX + LINE_SPACING_PX + OPTION_LINE_PADDING_PX
            match_count = 0
            # Add a box around the " item 1/2/3... " text
            for pattern_match in item_target_pattern.finditer(line):
                #print(pattern_match)
                box_x_start_pos = (pattern_match.start(match_count) + 1.75) * FONT_WIDTH_SIZE_PX
                box_x_end_pos = box_x_start_pos + ((pattern_match.end(match_count) - pattern_match.start(match_count) - 2.25) * FONT_WIDTH_SIZE_PX)
                #print(str(box_x_start_pos))
                #print(str(box_x_end_pos))
                drawing.rectangle([(box_x_start_pos, box_y_start_pos), box_x_end_pos, (box_y_start_pos + FONT_HEIGHT_SIZE_PX + 7)], fill=None, outline='black', width=2)
        else:
            drawing.text((BORDER_PADDING_PX, text_start_height), line, font=IMAGE_FONT, fill=('black'))
            text_start_height = text_start_height + FONT_HEIGHT_SIZE_PX + LINE_SPACING_PX

    #drawing.text((BORDER_PADDING_PX, BORDER_PADDING_PX), my_code.text, font=IMAGE_FONT, fill=('black'))
    drawing.rectangle([(0,0), (my_code.width_pixels, my_code.height_pixels)], fill=None, outline='black',width=2)
    # border appears as only 1 pixel width along right and bottom sides, so draw an extra line
    drawing.line((1, my_code.height_pixels-2, my_code.width_pixels-1, my_code.height_pixels-2), width=1, fill='black')
    drawing.line((my_code.width_pixels-2, 1, my_code.width_pixels-2, my_code.width_pixels-1), width=1, fill='black')
    img.save(image_filename)

    return send_file(image_filename, mimetype='image/png')

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
