from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create a new image with a white background
    size = (256, 256)
    image = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw a blue circle
    margin = 20
    draw.ellipse([margin, margin, size[0]-margin, size[1]-margin], fill='#2196F3')
    
    # Draw "UA" text
    try:
        # Try to use Arial font if available
        font = ImageFont.truetype("arial.ttf", 100)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    text = "UA"
    # Get text size
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Calculate center position
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text in white
    draw.text((x, y), text, fill='white', font=font)
    
    # Save as ICO
    image.save('app_icon.ico', format='ICO', sizes=[(256, 256)])

if __name__ == '__main__':
    create_icon()
