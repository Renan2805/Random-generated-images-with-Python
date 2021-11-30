from PIL import Image, ImageDraw, ImageChops, ImageFont
import random
import colorsys


def random_color():
    h = random.random()
    s = 1
    v = 1

    float_rgb = colorsys.hsv_to_rgb(h, s, v)
    rgb = [int(x * 255) for x in float_rgb]

    return tuple(rgb)


def fade(start_color, end_color, factor: float):
    recip = 1 - factor
    return (
        int(start_color[0] * recip + end_color[0] * factor),
        int(start_color[1] * recip + end_color[1] * factor),
        int(start_color[2] * recip + end_color[2] * factor)
    )


def generate_image(path: str, n: int):
    print("Generationg art")

    target_size = 256
    scale_factor = 2
    image_size = (target_size * scale_factor, target_size * scale_factor)
    image_padding = 25 * scale_factor
    image_bg_color = random_color()

    image = Image.new(mode="RGB", size=image_size, color=image_bg_color)

    # Draw some lines
    draw = ImageDraw.Draw(image)
    start_color = random_color()
    end_color = random_color()
    points = []
    for _ in range(10):
        random_point = (
            random.randint(image_padding, image_size[0] - image_padding),
            random.randint(image_padding, image_size[1] - image_padding)
        )
        points.append(random_point)

    # Center the image
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])
    delta_x = min_x - (image_size[0] - max_x)
    delta_y = min_y - (image_size[0] - max_y)
    for i, point in enumerate(points):
        points[i] = (point[0] - delta_x // 2, point[1] - delta_y // 2)

    thickness = 0
    n_points = len(points) - 1
    for i, point in enumerate(points):
        if i == 0:
            font = ImageFont.truetype('font/PressStart2P-Regular.ttf', 18 * scale_factor)
            font_color = random_color()
            draw.text((10, 10), text="line", font=font,
                      fill=font_color, anchor='lt')
            draw.text((image_size[0] - 10, image_size[0] - 10),
                      text=f'#{str(n)}', font=font, fill=font_color, anchor='rb')

        overlay_image = Image.new(mode="RGB", size=image_size, color=(0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay_image)

        p1 = point

        if i == n_points:
            p2 = points[0]
        else:
            p2 = points[i + 1]

        line_xy = (p1, p2)

        thickness += scale_factor
        color_factor = i / n_points
        line_color = fade(start_color, end_color, color_factor)
        overlay_draw.line(line_xy, fill=line_color, width=thickness)
        image = ImageChops.add(image, overlay_image)

    # Save the image
    image = image.resize((target_size, target_size), resample=Image.ANTIALIAS)
    image.save(path)


if __name__ == '__main__':
    for i in range(10000):
        generate_image(f'images/image_{str(i)}.png', i + 1)
