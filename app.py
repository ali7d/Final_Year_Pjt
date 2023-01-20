import tkinter as tk
from tkinter import filedialog
import replicate
import urllib.request
from PIL import ImageTk, Image
import os,io

# Set the API token
os.environ["REPLICATE_API_TOKEN"] = "f9e5970c7b6721d2c2676bb3cd55cc80bee31588"

# Initialize the GUI
window = tk.Tk()
window.title("Lite Stable Diffusion")
window.geometry("932x1232")
window.config(bg="#979797")

# Add a label and text box for the user to enter a text description
label = tk.Label(master=window, bg="#cfcfcf", text="Enter Your Prompt:", font=("Consolas", 14))
label.pack(pady=20)

text_box = tk.Text(master=window, bg="#addb9c", height=10, width=50, font=("Consolas", 12))
text_box.pack(pady=10)

image_label = None

# Add a generate button
def generate():
    global image_label
    # Get the text from the text box
    text = text_box.get("1.0", "end")

    # Use the Replicate Stable Diffusion API to generate an image
    try:
        model = replicate.models.get("stability-ai/stable-diffusion")
        output_url = model.predict(prompt=text)[0]
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
        image_label.pack(pady=20)
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred while displaying the image: {e}")

button = tk.Button(master=window, bg="#d3d3d3",text="Generate", command=generate)
button.pack()

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

save_button = tk.Button(master=window, bg="#d3d3d3", text="Save", command=save)
save_button.pack()

# Run the GUI
window.mainloop()
