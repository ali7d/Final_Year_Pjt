import tkinter as tk
from tkinter import filedialog
import replicate
import urllib.request
from PIL import ImageTk, Image
from PIL.Image import Resampling
import os
import io

# Set the API token
os.environ["REPLICATE_API_TOKEN"] = "6b77e36dce0a22124b958dea44d2336f3c7ca6c3"

# Initialize the GUI
window = tk.Tk()
window.title("Lite Stable Diffusion")
window.geometry("932x1232")
window.config(bg="#979797")

# Text box for the user to enter a text description
label = tk.Label(master=window, bg="#cfcfcf", text="Enter Your Prompt:", font=("Consolas", 14))
label.pack(pady=20)

text_box = tk.Text(master=window, bg="#addb9c", height=2, width=70, font=("Consolas", 12))
text_box.pack(pady=10)

image_label = None

# Generate button
def generate():
    global image_label
    # Get the text from the text box
    text = text_box.get("1.0", "end")
    num_images = int(num_images_input.get())

    # Use the Replicate Stable Diffusion API
    try:
        model = replicate.models.get("stability-ai/stable-diffusion")
        for i in range(num_images):
            output_url = model.predict(prompt=text)[0]
        # Delete previeus image
        if image_label:
            image_label.destroy()
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred while generating the image: {e}")
        return
    # Display the generated image
    try:
        image_byt = urllib.request.urlopen(output_url).read()
        image = Image.open(io.BytesIO(image_byt))
        # Resize the image
        image = image.resize((256, 256), Resampling.LANCZOS)
        image = ImageTk.PhotoImage(image)
        image_label = tk.Label(master=window, image=image)
        image_label.image = image
        image_label.pack(pady=20)
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred while displaying the image: {e}")
button = tk.Button(master=window, bg="#d3d3d3",text="Generate", command=generate, font=("Consolas", 12))
num_images_input = tk.Spinbox(master=window, from_=1, to=10)
num_images_input.pack()
button.pack(pady=10)

def save():
    try:
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG file", "*.png")])
        model = replicate.models.get("stability-ai/stable-diffusion")
        text = text_box.get("1.0", "end")
        output_url = model.predict(prompt=text)[0]
        img = Image.open(io.BytesIO(urllib.request.urlopen(output_url).read()))
        img.save(filename)
        tk.messagebox.showinfo("Success", "Image saved successfully")
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred while saving the image: {e}")
# Save button
save_button = tk.Button(master=window, bg="#d3d3d3", text="Save", command=save, font=("Consolas", 11))
save_button.pack(pady=10)

# Run the GUI
window.mainloop()
