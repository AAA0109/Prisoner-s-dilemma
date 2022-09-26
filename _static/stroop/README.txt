Note: you can generate new images by doing "pip3 install pillow"

Then running this function:

def generate_image(decoy_text, color, image_id, is_congruent):
    from PIL import Image, ImageDraw, ImageFont

    rgb = dict(red=(255, 0, 0), yellow=(255, 255, 0), blue=(0, 0, 255), green=(0, 255, 0))
    img = Image.new('RGB', (220, 100), color=(155, 155, 155))
    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype('arial.ttf', 70)
    d.text((10, 10), decoy_text, fill=rgb[color], font=fnt)
    img.save(f'_static/stroop/{name}.png')

for combo in generate_combos():
    generate_image(**combo)
