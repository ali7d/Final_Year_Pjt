import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import replicate
import urllib.request
from PIL import ImageTk, Image
from PIL.Image import Resampling
import os
import io

# Set the API token
os.environ["REPLICATE_API_TOKEN"] = "3f845265fa106c6558532441b42bf235f9314f68"

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

image_labels = []

def generate():
    global output_url
    # Get the text from the text box
    text = text_box.get("1.0", "end")    
    if not text:
        tk.messagebox.showerror("Error", "Please enter a prompt")
        return
    
    api_token = os.environ.get("REPLICATE_API_TOKEN")

    # Use the Replicate Stable Diffusion API
    try:
        model = replicate.models.get("stability-ai/stable-diffusion")
        output_url = model.predict(prompt=text)[0]
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
        # Add the image_url key to the label object
        image_label.image_url = output_url
        image_label.image = photo_image
        image_labels.append(image_label)
        # Display images horizontally
        x_offset = 20
        for i, label in enumerate(image_labels):
            if i >= 4:
                # Remove the oldest image
                label.pack_forget()
            else:
                label.place(x=x_offset, y=200)
                x_offset += 300
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred while displaying the image: {e}")          
            
button = tk.Button(master=window, bg="#d3d3d3",text="Generate", command=generate, font=("Consolas", 12))
button.place(relx=0.8, rely=0.9, anchor='center')


def save():
    if not image_labels:
       tk.messagebox.showerror( "Error", "No image URL found to save" )
       return
    # Create a list of tuples containing the index and label for each image
    image_choices = [(i, label) for i, label in enumerate(image_labels)]
    
    # Display a dialog box with a list of image choices for the user to select from
    choice = tk.messagebox.askquestion("Save Image", "Which image do you want to save?", icon='question', 
                                        type=tk.messagebox.YESNO, 
                                        detail="\n".join([f"{i+1}: {label['text']}" for i, label in image_choices]))
    if choice == tk.messagebox.NO:
        return
    
    # Get the selected image label
    selected_label = None
    while not selected_label:
        choice = simpledialog.askstring("Save Image", "Enter the number of the image you want to save:")
        try:
            choice = int(choice)
            selected_label = image_choices[choice - 1][1]
        except (ValueError, IndexError):
            tk.messagebox.showerror("Error", "Invalid selection")

    # Save the selected image
        try:
            filename = filedialog.asksaveasfilename(defaultextension='.png')
            if filename:
                img = Image.open(io.BytesIO(urllib.request.urlopen(selected_label.image_url).read()))
                img.save(filename)
                tk.messagebox.showinfo("Success", "Image saved successfully")
            else:
                tk.messagebox.showinfo("Info", "Save operation cancelled")    
        except Exception as e:
           tk.messagebox.showerror("Error", f"An error occurred while saving the image: {e}")
# Save button
save_button = tk.Button(master=window, bg="#d3d3d3", text="Save", command=save, font=("Consolas", 11))
save_button.place(relx=0.9, rely=0.9, anchor='center')

# Run the GUI
window.mainloop()
