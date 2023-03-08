import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import replicate
import urllib.request
from PIL import ImageTk, Image
from PIL.Image import Resampling
import os
import io

# Set the API token
os.environ["REPLICATE_API_TOKEN"] = "f9e5970c7b6721d2c2676bb3cd55cc80bee31588"

# Initialize the GUI
window = tk.Tk()
window.configure(bg="#808080")
window.title("Lite Stable Diffusion")
window.wm_attributes('-fullscreen', 'true')
window.resizable(width=True, height=True)

# Text box for the user to enter a text description
label = tk.Label(master=window, bg="#cfcfcf", text="Enter Your Prompt:", font=("Consolas", 14))
label.pack(pady=20)

text_box = tk.Text(master=window, bg="#addb9c", height=2, width=70, font=("Consolas", 12))
text_box.pack(pady=10)

close_button = tk.Button(master=window, bg="#d3d3d3", text="Close", command=window.destroy, font=("Consolas", 12))
close_button.place(relx=0.1, rely=0.9, anchor='center')

image_label = None
output_url = None

image_history = []

def generate():
    global image_label
    global output_url
    # Get the text from the text box
    text = text_box.get("1.0", "end")
    #num_images = int(num_images_input.get())

    # Use the Replicate Stable Diffusion API
    try:
        model = replicate.models.get("stability-ai/stable-diffusion")
        #for i in range(num_images):
        output_url = model.predict(prompt=text)[0]
        # Delete previeus image
        if image_label:
            image_label.destroy()
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred while generating the image: {e}")
        return
    # Display the generated image
    try:
        with urllib.request.urlopen(output_url) as url:
            image_bytes = url.read()
        image = Image.open(io.BytesIO(image_bytes))
        # Resize the image
        image = image.resize((256, 256), Resampling.LANCZOS)
        photo_image = ImageTk.PhotoImage(image)
        image_label = tk.Label(master=window, image=photo_image)
        image_label.image = photo_image
        image_label.pack(pady=180)
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred while displaying the image: {e}")
        
def update_ui_from_history():
    for prompt, url, image in image_history:
            add_image_to_history(prompt, url, image)
            
def add_image_to_history(prompt, url, image):
    # Append the new image to the history
    image_history.append((prompt, url, image))
    if len(image_history) > 5:
        image_history.pop(0)           
            
button = tk.Button(master=window, bg="#d3d3d3",text="Generate", command=generate, font=("Consolas", 12))
button.place(relx=0.8, rely=0.9, anchor='center')


def save():
    if output_url is None:
       tk.messagebox.showerror( "Error", "No image URL found to save" )
    else:
        try:
           filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG file", "*.png")])
           img = Image.open(io.BytesIO(urllib.request.urlopen(output_url).read()))
           img.save(filename)
           tk.messagebox.showinfo("Success", "Image saved successfully")
        except Exception as e:
           tk.messagebox.showerror("Error", f"An error occurred while saving the image: {e}")
# Save button
save_button = tk.Button(master=window, bg="#d3d3d3", text="Save", command=save, font=("Consolas", 11))
save_button.place(relx=0.9, rely=0.9, anchor='center')

# Run the GUI
window.mainloop()
