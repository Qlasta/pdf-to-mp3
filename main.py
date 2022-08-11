from google.cloud import texttospeech  #install pip install --upgrade google-cloud-texttospeech
import os
import PyPDF2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

BACKGROUND_C = "#D6EFED"
TITLE_C = "#C9BBCF"
TEXT_C = "#898AA6"
TITLE_F = ("Terminal", 24, "normal")
TEXT_F = ("Helvetica", 14, "normal")
TEXT_F_s = ("Helvetica", 10, "normal")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ["GOOGLE_SECRETS"]


def file_open():
    """Opens directory dialog to select an image. Shows path of selected image."""
    global selected_file
    selected_file = filedialog.askopenfilename()
    # show file path
    label_f_uploaded["text"] = "Selected file:"
    label_file_path["text"] = selected_file
    label_f_uploaded.grid(row=3, column=0)
    label_file_path.grid(row=3, column=2)

def choose_location():
    global save_directory
    save_directory = filedialog.askdirectory()
    label_location["text"] = "Selected location:"
    label_location_path["text"] = save_directory
    label_location.grid(row=9, column=0)
    label_location_path.grid(row=9, column=2)


def execute():
    book = ""
    # Open pdf file and convert to text file
    with open(f"{selected_file}", "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        pages = reader.getNumPages()

        for n in range(0,pages):
            page = reader.getPage(n)
            textas = page.extractText()
            book += f"\n{textas}"


    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=book)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    output = entry_w_text.get()
    with open(f"{save_directory}/{output}.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f'Audio content written to file "{output}.mp3"')
        label_completed = tk.Label(text=f'Audio content written to: "{save_directory}/{output}.mp3"', font=TEXT_F, fg=TITLE_C, bg=BACKGROUND_C, anchor="nw",
                                  justify="center")
        label_completed.grid(row=11, column=0, columnspan=3)
        label_completed.config(pady=10)


# title and background
window = tk.Tk()
window.title("PDF to Speech")
window.minsize(width=500, height=300)
window.config(padx=50, pady=50, bg=BACKGROUND_C)
title_label = tk.Label(text="Convert PDF to MP3", fg=TITLE_C, pady=20, bg=BACKGROUND_C)
title_label["font"]=TITLE_F
title_label.grid(row=0, column=0, columnspan=3)
canvas = tk.Canvas(width=300, height=120)
img = tk.PhotoImage(file="book.png")
cover_img = img.subsample(4, 4)
canvas.config(bg=BACKGROUND_C, highlightthickness=0)
canvas.create_image(130,64, image=cover_img)
canvas.grid(row=1, column=1)

# enter m3 file name
label_w_text = tk.Label(text="Give name to your MP3 file:", font=TEXT_F, fg=TEXT_C, bg=BACKGROUND_C)
label_w_text.grid(row=6, column=0)
label_w_text.focus()
entry_w_text = tk.Entry(width=30)
entry_w_text.grid(row=6, column=2)



# select PDF file
label_w_upload = tk.Label(text="Select your PDF file:", font=TEXT_F, fg=TEXT_C, bg=BACKGROUND_C, anchor="nw", justify="left")
label_w_upload.grid(row=2, column=0)

button_w_upload = tk.Button(text="Open PDF", font=TEXT_F, fg=TEXT_C, width=15, command=file_open, activeforeground=TEXT_C, height=1)
button_w_upload.grid(row=2, column=2)

# path of selected file
label_f_uploaded = tk.Label(text="", font=TEXT_F, fg=TEXT_C, bg=BACKGROUND_C)
label_file_path = tk.Label(text="", bg=BACKGROUND_C)

# select MP3 file location
label_w_upload = tk.Label(text="Select where to save MP3:", font=TEXT_F, fg=TEXT_C, bg=BACKGROUND_C, anchor="nw", justify="left")
label_w_upload.grid(row=8, column=0)

button_w_upload = tk.Button(text="Choose directory", font=TEXT_F, fg=TEXT_C, width=15, command=choose_location, activeforeground=TEXT_C, height=1)
button_w_upload.grid(row=8, column=2)

# path of Mp3
label_location = tk.Label(text="", font=TEXT_F, fg=TEXT_C, bg=BACKGROUND_C)
label_location_path = tk.Label(text="", bg=BACKGROUND_C)

# convert to MP3
execute_button = tk.Button(text="Convert to MP3", font=TEXT_F, fg=TEXT_C, width=30, command=execute,
                           activeforeground=TEXT_C)
execute_button.grid(row=10, column=0, columnspan=3)


window.mainloop()
