import os
from PIL import Image, ImageDraw, ImageFont


def generate_font_images(font_path, output_dir, font_pixel_size=24, max_size=14, test=True):
    """
    Generate images for specified characters in the font file.

    Args:
        font_path (str): Path to the font file.
        output_dir (str): Directory to save the output images.
        font_pixel_size (int): Font size in pixels.
        max_size (int): Maximum width and height of the image (square).
    """

    # Load the font
    font = ImageFont.truetype(font_path, font_pixel_size)

    # Create the output directory
    os.makedirs(output_dir, exist_ok=True)

    # testing characters
    unicode_chars = [0x5173, 0x95ED, 0x8FD4, 0x56DE]  # 关，闭，返，回
    characters_range = (
        list(range(0x4E00, 0x9FFF + 1)) +  # Common Chinese characters
        list(range(0x3000, 0x303F + 1)) +  # Full-width punctuation
        list(range(0xFF00, 0xFFEF + 1))    # CJK symbols and punctuation
        if not test else unicode_chars
    )

    # Define the palette
    palette = [0, 0, 0,  # black
               0, 211, 247,  # fill_color #00d3f7
               255, 0, 143]  # bg_color #ff008f

    # Generate images for all Chinese characters
    for codepoint in characters_range:
        char = chr(codepoint)
        # Create the initial image for the font
        image = Image.new("P", (max_size, max_size), 2)
        image.putpalette(palette)
        draw = ImageDraw.Draw(image)

        # Characters offset on the y-axis
        y_offset = -2

        # Draw the shadow
        # fill=0 corresponds to black in the palette
        draw.text((1, 0 + y_offset), char, font=font, fill=0)
        draw.text((1, 1 + y_offset), char, font=font, fill=0)

        # Draw the text (fill color)
        # fill=1 corresponds to fill_color in the palette
        draw.text((0, 0 + y_offset), char, font=font, fill=1)

        # Save the image
        filename = f"U+{hex(codepoint)[2:].upper()}.player.nx0.ny0.bmp"
        image.save(os.path.join(output_dir, filename), "BMP")

    print(f"Images have been saved to {output_dir}")


if __name__ == "__main__":
    font_path = "./SourceHanSansCN-Bold.otf"
    output_dir = "0.output"
    font_pixel_size = 8
    max_size = 9
    test = False
    generate_font_images(font_path, output_dir, font_pixel_size=font_pixel_size,
                         max_size=max_size, test=test)
