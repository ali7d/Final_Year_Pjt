import tkinter as tk
import requests
from tkinter import filedialog
from PIL import ImageTk, Image
import io

# Initialize the GUI
window = tk.Tk()
window.title("Text to Image Generator")
window.geometry("800x600")

# Add a label and text box for the user to enter a text description
label = tk.Label(master=window, text="Enter a text description:", font=("Arial", 14))
label.pack(pady=20)

text_box = tk.Text(master=window, height=10, width=50, font=("Arial", 12))
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

  # Convert the image to a PhotoImage object
  image = ImageTk.PhotoImage(image=Image.open(io.BytesIO(image)))

  # Display the image in a label
  image_label = tk.Label(master=window, image=image)
  image_label.image = image
  image_label.pack(pady=20)

button = tk.Button(master=window, text="Generate", command=generate)
button.pack()

# Run the GUI
window.mainloop()
