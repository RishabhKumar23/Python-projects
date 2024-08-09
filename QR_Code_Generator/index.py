from tkinter import *
import qrcode
from PIL import Image as PILImage, ImageTk

root = Tk()
root.title("QR Code Generator")
root.geometry("1000x550")
root.config(bg="#AE2321")
root.resizable(False, False)


def generate():
    name = title.get()
    text = entry.get()
    if not name or not text:
        print("Please provide both title and text.")
        return

    try:
        qr = qrcode.QRCode(
            version=1,  # Ensure valid version (1 to 40)
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        # Save QR code
        filename = f"QR_code/{name}.png"
        img.save(filename)

        # Display QR code
        pil_img = PILImage.open(filename)
        img_tk = ImageTk.PhotoImage(pil_img)
        Image_view.config(image=img_tk)
        Image_view.image = img_tk

    except Exception as e:
        print(f"An error occurred: {e}")


Image_view = Label(root, bg="#AE2321")
Image_view.pack(padx=50, pady=10, side=RIGHT)

Label(root, text="Title", fg="white", bg="#AE2321", font=15).place(x=50, y=170)

title = Entry(root, width=13, font="arial 15")
title.place(x=50, y=200)

entry = Entry(root, width=28, font="arial 15")
entry.place(x=50, y=250)

Button(root, text="Generate", width=20, height=2, bg="black", fg="white", command=generate).place(x=50, y=300)

root.mainloop()
