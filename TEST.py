import tkinter as tk
from tkinter import filedialog
import replicate
import urllib.request
from PIL import ImageTk, Image
import os,io
import json
import requests
import urllib.parse


# Set the API token
api_key = "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"


# Initialize the GUI
window = tk.Tk()
window.title("Lite Stable Diffusion")
window.geometry("932x1232")
window.config(bg="#979797")

# Add a label and text box for the user to enter a text description
label = tk.Label(master=window, bg="#cfcfcf", text="Enter Your Prompt:", font=("Consolas", 14))
label.pack(pady=20)

text_box = tk.Text(master=window, bg="#addb9c", height=3, width=70, font=("Consolas", 12))
text_box.pack(pady=10)

image_label = None

# Add a generate button
def generate():
    global image_label
    # Get the text from the text box
    text = text_box.get("1.0", "end")

    # Stable Diffusion API to generate an image
    try:
        response = requests.post('https://api.openai.com/v1/images/generations',
            headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'},
            json={
                "model": "image-alpha-001",
                "prompt": text,
                "num_images":1,
                "size":"256x256"
            })
        response_json = json.loads(response.text)
        output_url = response_json["data"][0]["url"]

    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred while generating the image: {e}")
        return
    # Delete previeus image    
    if image_label:
        image_label.destroy()
    # Display the generated image in the GUI
    try:
        image_byt = urllib.request.urlopen(output_url).read()
        image = Image.open(io.BytesIO(image_byt))
        # Resize the image to a medium size
        image = image.resize((512, 512), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        image_label = tk.Label(master=window, image=image)
        image_label.image = image
        image_label.pack(pady=30)
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred while displaying the image: {e}")

button = tk.Button(master=window, bg="#d3d3d3",text="Generate", command=generate, font=("Consolas", 12))
button.config(height = 1, width = 12, relief = "groove", bd = 3)
button.pack()

def save():
    try:
        response = requests.post('https://api.openai.com/v1/images/generations',
            headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'},
            json={
                "model": "image-alpha-001",
                "prompt": text,
                "num_images":1,
                "size":"256x256"
            })
        response_json = json.loads(response.text)
        output_url = response_json["data"][0]["url"]
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG file", "*.png")])
        text = text_box.get("1.0", "end")
        img = Image.open(io.BytesIO(urllib.request.urlopen(output_url).read()))
        img.save(filename)
        tk.messagebox.showinfo("Success", "Image saved successfully")
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred while saving the image: {e}")

save_button = tk.Button(master=window, bg="#d3d3d3", text="Save", command=save, font=("Consolas", 12))
save_button.config(height = 1, width = 7, relief = "groove", bd = 3)
save_button.pack(pady=7)

# Run the GUI
window.mainloop()
