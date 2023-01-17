import tkinter as tk
import requests
from tkinter import filedialog
from PIL import ImageTk, Image
import io
import urllib.request

# Initialize the GUI
window = tk.Tk()
window.title("Lite Stable Generator")
window.geometry("932x1232")
window.config(bg="#979797")

# Add a label and text box for the user to enter a text description
label = tk.Label(master=window, bg="#cfcfcf", text="Enter Your Prompt:", font=("Consolas", 14))
label.pack(pady=20)

text_box = tk.Text(master=window, bg="#addb9c", height=10, width=50, font=("Consolas", 12))
text_box.pack(pady=10)

# Add a generate button
def generate():
  # Get the text from the text box
  text = text_box.get("1.0", "end")

  # Use the Stable Diffusion API to generate an image from the text
  headers = {
    "Authorization": "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"
  }
  data = {
    "text": text
  }
  response = requests.post("https://api.newnative.ai/stable-diffusion?prompt=futuristic spce station, 4k digital art", headers=headers, json=data)
  image = response.content

  urllib.request.urlretrieve("https://storage.googleapis.com/lablab-static-eu/stable-diffusion/futuristic%20space%20station.png", "local-filename.jpg")

  # Convert the image to a PhotoImage object
  image = ImageTk.PhotoImage(image=Image.open(io.BytesIO(image)))

  # Display the image in a label
  image_label = tk.Label(master=window, image=image)
  image_label.image = image
  image_label.pack(pady=20)

button = tk.Button(master=window, bg="#d3d3d3",text="Generate", command=generate)
button.pack()

# Run the GUI
window.mainloop()
