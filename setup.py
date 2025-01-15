import os
import shutil
import pkg_resources

def setup():
    # Create fonts directory if it doesn't exist
    fonts_dir = 'fonts'
    os.makedirs(fonts_dir, exist_ok=True)

    # Copy Arial font to the fonts directory
    arial_font = pkg_resources.resource_filename('PIL', 'Arial.ttf')
    shutil.copy(arial_font, os.path.join(fonts_dir, 'arial.ttf'))

    # Create backgrounds directory if it doesn't exist
    backgrounds_dir = 'backgrounds'
    os.makedirs(backgrounds_dir, exist_ok=True)

    # Create a simple fancy background
    from PIL import Image, ImageDraw
    fancy_bg = Image.new('RGB', (400, 600), color='white')
    draw = ImageDraw.Draw(fancy_bg)
    for i in range(0, 600, 20):
        draw.line([(0, i), (400, i)], fill=(240, 240, 240), width=1)
    fancy_bg.save(os.path.join(backgrounds_dir, 'fancy.png'))

    print("Setup complete. Arial font has been copied to the 'fonts' directory and a fancy background has been created in the 'backgrounds' directory.")

if __name__ == "__main__":
    setup()

