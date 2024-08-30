from PIL import Image, ImageDraw, ImageFont

# Create a blank white image
image = Image.new('RGB', (512, 512), 'blue')
draw = ImageDraw.Draw(image)

# Draw the doctor's coat (simple rectangle)
draw.rectangle([150, 150, 350, 450], fill="white", outline="red")

# Draw the stethoscope (simplified version)
draw.ellipse([200, 100, 300, 200], outline="black", width=5)  # head of stethoscope
draw.line([250, 200, 250, 300], fill="yellow", width=5)  # tube
draw.line([250, 300, 200, 400], fill="yellow", width=5)  # tube to right
draw.line([250, 300, 300, 400], fill="yellow", width=5)  # tube to left

# Draw hands (simplified)
draw.ellipse([100, 400, 200, 500], fill="peachpuff", outline="black")
draw.ellipse([300, 400, 400, 500], fill="peachpuff", outline="black")

# Draw table
draw.rectangle([0, 450, 512, 512], fill="lightgrey", outline="black")

# Optionally, add some text
font = ImageFont.load_default()
draw.text((200, 460), "Doctor's Desk", fill="black", font=font)

# Save or show the image
image.show()
image.save('/mnt/data/doctor_simplified.png')
