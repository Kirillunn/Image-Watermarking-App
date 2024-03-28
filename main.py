from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Constants
BG_COLOR = "#DFF5FF"
FONT_COLOR="#5356FF"
FILEPATH = ""
SAVED_IMG = None

# Download image into working zone
def download_image():
    # Choose file from HD
    global FILEPATH
    FILEPATH = filedialog.askopenfilename()

    # Open the image with PIL
    pil_image = Image.open(FILEPATH)

    # Resize the image to fit in the working zone
    pil_image.thumbnail(size=(512, 512))

    # Convert the PIL image to a Tkinter PhotoImage
    new_img = ImageTk.PhotoImage(pil_image)

    # Load image in the working zone
    working_zone.itemconfig(edited_img, image=new_img)
    working_zone.image = new_img


# Add watermarks to the image
def add_text():
    global FILEPATH, SAVED_IMG

    # Get text from entry
    watermark = text_entry.get()

    # Check the filepath exists
    if FILEPATH == "":
        messagebox.showerror(title="Error", message="You don't choose the file")
    else:
        with Image.open(FILEPATH).convert("RGBA") as base:
            # Make a blank image for the text, initialized to transparent text color
            txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

            # Get a font
            fnt = ImageFont.truetype("Arial", 120)
            # Get a drawing context
            d = ImageDraw.Draw(txt)

            # Define spacing and initial coordinates
            spacing = 1200
            x = 10
            y = 10

            # For the whole height of image
            while y < base.height:
                # For the whole width of image
                while x < base.width:
                    # Draw text with spacing
                    d.text((x, y), watermark, font=fnt, fill=(255, 255, 255, 128))
                    x += spacing
                # Reset x to the initial position
                x = 10
                # Move y to the next line
                y += spacing

            # Create image with watermarks
            SAVED_IMG = Image.alpha_composite(base, txt)

            # Create compressed duplicate for displaying into working zone
            duplicate = SAVED_IMG.copy()
            duplicate.thumbnail(size=(512, 512))
            duplicate.thumbnail(size=(512,512))
            watermark_img = ImageTk.PhotoImage(duplicate)

            # Display compressed image with watermarks into working zone
            working_zone.itemconfig(edited_img, image=watermark_img)
            working_zone.image = watermark_img


# Delete text from image
def delete_text():
    global SAVED_IMG
    # Check the image exists
    if SAVED_IMG == None:
        messagebox.showerror(title="Error", message="The file is empty. Please, download the file first")
    else:
        # Download original image without watermarks
        original_image = Image.open(FILEPATH)
        original_image.thumbnail(size=(512, 512))
        new_img = ImageTk.PhotoImage(original_image)
        working_zone.itemconfig(edited_img, image=new_img)
        working_zone.image = new_img


# Saving image with watermarks (NB: App saves image in original size not the compressed one)
def save_image():
    global SAVED_IMG
    filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    # Check the image exists
    if filename and SAVED_IMG is not None:
        SAVED_IMG.save(filename)
    else:
        messagebox.showerror(title="Error", message="The file is empty. Please, download the file first")


# UI Setup
window = Tk()
window.title(string="H2OStamp")
window.config(background=BG_COLOR)
window.config(padx=30, pady=50)

# Canvas
canvas = Canvas(height=256, width=256, background=BG_COLOR, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(128, 128, image=logo)
canvas.grid(column=0, row=0)

# Working zone
working_zone = Canvas(height=512, width=512, background="white", highlightthickness=0)
edited_img = working_zone.create_image(256,256, image=None)
working_zone.grid(column=1, row=0, rowspan=5)

# Select button
select_button = Button(text="Select file", width=15, height=2,
                       font=("Helvetica", 18), foreground=FONT_COLOR,
                       highlightthickness=0, command=download_image)
select_button.grid(column=1, row=5)

# Watermark bar
text_entry = Entry(width=15, highlightthickness=0, background="white", foreground="black")
text_entry.grid(column=0, row=1)
add_text_button = Button(text="Add text", width=10, font=("Helvetica", 16),
                         foreground=FONT_COLOR, highlightthickness=0, command=add_text)
add_text_button.grid(column=0, row=2)
delete_text_button = Button(text="Delete text", width=10, font=("Helvetica", 16),
                         foreground=FONT_COLOR, highlightthickness=0, command=delete_text)
delete_text_button.grid(column=0, row=3)
save_button = Button(text="Save image", width=10, font=("Helvetica", 16),
                     foreground=FONT_COLOR, highlightthickness=0, command=save_image)
save_button.grid(column=0, row=4)


window.mainloop()