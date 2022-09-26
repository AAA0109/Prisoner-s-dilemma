from pathlib import Path

# https://upload.wikimedia.org/wikipedia/commons/a/a0/Circle_-_black_simple.svg
CIRCLE = """
<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500">
<circle cx="250" cy="250" r="210" fill="{fill}" stroke="#000" stroke-width="8"/>
</svg>
"""

# https://upload.wikimedia.org/wikipedia/commons/4/4f/Simple_triangle.svg
TRIANGLE = """
<svg xmlns="http://www.w3.org/2000/svg" version="1.0" width="100" height="100">
  <polygon points="50,16 85,85 15,85 50,16" 
  fill="{fill}" stroke="black" stroke-width="1.2" />
</svg>
"""

# https://upload.wikimedia.org/wikipedia/commons/1/18/Five-pointed_star.svg
STAR = """
<svg xmlns="http://www.w3.org/2000/svg" width="255" height="240" viewBox="0 0 51 48">
<path 
    fill="{fill}" 
    stroke="black" 
    d="m25,1 6,17h18l-14,11 5,17-15-10-15,10 5-17-14-11h18z"/>
</svg>    
"""

# https://upload.wikimedia.org/wikipedia/commons/f/f9/Plus_sign.svg
PLUS = """
<svg xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink"
width="200px" height="200px" viewbox="0 0 200 200"
preserveAspectRatio="none">

<path 
    d="m60,10 L60,60 L10,60 L10,135 L10,135 L60,135 L60,185 L135,185 L135,135 L185,135 L185,60 L135,60 L135,10Z" 
    fill="{fill}" stroke="black" stroke-width="5" /> 
</svg>
"""


def make_shape(shape_type, color):
    return dict(CIRCLE=CIRCLE, TRIANGLE=TRIANGLE, PLUS=PLUS, STAR=STAR)[shape_type].format(
        fill=color
    )


for shape_type in ['circle', 'triangle', 'star', 'plus']:
    for color in ['blue', 'green', 'red', 'yellow']:
        Path(f'{shape_type}-{color}.svg').write_text(
            make_shape(shape_type=shape_type.upper(), color=color)
        )
