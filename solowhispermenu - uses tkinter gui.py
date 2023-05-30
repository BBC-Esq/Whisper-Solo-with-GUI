import os
import subprocess
import shutil
from tkinter import *
from tkinter import ttk
from tkinter import filedialog


def run_batch_script():
    script_name = "solowhisper.bat"
    script_path = shutil.which(script_name)

    if script_path is None:
        print(f"{script_name} not found in the system path. Please check the system path configuration.")
        return

    selected_model = model_var.get() or ""
    selected_format = format_var.get() or ""
    selected_file_path = selected_file_var.get() or ""

    if not selected_file_path:
        print("No file selected. Exiting...")
        return

    if translate_var.get():
        task_flag = "--task translate"
        source_language_flag = f"--language {language_var.get()}"
    else:
        task_flag = ""
        source_language_flag = ""

    command = f"{script_path} \"{selected_model}\" \"{selected_file_path}\" \"{selected_format}\" \"{task_flag}\" \"{source_language_flag}\""
    subprocess.run(command, shell=True)


def toggle_language_menu():
    if translate_var.get():
        language_menu.config(state="readonly")
    else:
        language_menu.config(state="disabled")

root = Tk()
root.title("Whisper GUI")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

min_window_width = 400
root.minsize(min_window_width, -1)

root.update_idletasks()

window_width = root.winfo_width()
window_height = root.winfo_height()
window_height += 5  # Increase window height by 50 pixels
x_position = int((screen_width / 2) - (window_width / 2))
y_position = int((screen_height / 2) - (window_height / 2))

root.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')

frame = Frame(root)
frame.pack(padx=10, pady=10)

Label(frame, text="Choose the Whisper model:").grid(row=0, column=0, sticky=W)

model_var = StringVar()
model_var.set("large-v2")

model_options = [
    "tiny.en", "tiny", "base.en", "base", "small.en", "small",
    "medium.en", "medium", "large", "large-v1", "large-v2"
]

model_menu = ttk.Combobox(frame, textvariable=model_var, values=model_options, state="readonly", justify="left")
model_menu.grid(row=0, column=1, sticky=W)

Label(frame, text="Choose the output format:").grid(row=1, column=0, sticky=W)

format_var = StringVar()
format_var.set("vtt")

format_options = [
    "txt", "vtt", "srt", "tsv", "json", "all"
]

format_menu = ttk.Combobox(frame, textvariable=format_var, values=format_options, state="readonly", justify="left")
format_menu.grid(row=1, column=1, sticky=W)

translate_var = BooleanVar()
translate_var.set(False)

translate_checkbox = Checkbutton(frame, text="Translate to English", variable=translate_var, command=toggle_language_menu, justify="left")
translate_checkbox.grid(row=2, columnspan=2, sticky=W)

Label(frame, text="Choose the source language:").grid(row=3, column=0, sticky=W)

language_var = StringVar()

language_options = [
    "Afrikaans","Albanian","Amharic","Arabic","Armenian","Assamese","Azerbaijani","Bashkir","Basque","Belarusian",
    "Bengali","Bosnian","Breton","Bulgarian","Burmese","Castilian","Catalan","Chinese","Croatian","Czech",
    "Danish","Dutch","English","Estonian","Faroese","Finnish","Flemish","French","Galician","Georgian",
    "German","Greek","Gujarati","Haitian","Haitian Creole","Hausa","Hawaiian","Hebrew","Hindi","Hungarian",
    "Icelandic","Indonesian","Italian","Japanese","Javanese","Kannada","Kazakh","Khmer","Korean","Lao",
    "Latin","Latvian","Letzeburgesch","Lingala","Lithuanian","Luxembourgish","Macedonian","Malagasy","Malay",
    "Malayalam","Maltese","Maori","Marathi","Moldavian","Moldovan","Mongolian","Myanmar","Nepali","Norwegian",
    "Nynorsk","Occitan","Panjabi","Pashto","Persian","Polish","Portuguese","Punjabi","Pushto","Romanian","Russian",
    "Sanskrit","Serbian","Shona","Sindhi","Sinhala","Sinhalese","Slovak","Slovenian","Somali","Spanish","Sundanese",
    "Swahili","Swedish","Tagalog","Tajik","Tamil","Tatar","Telugu","Thai","Tibetan","Turkish","Turkmen","Ukrainian",
    "Urdu","Uzbek","Valencian","Vietnamese","Welsh","Yiddish","Yoruba"
]

language_menu = ttk.Combobox(frame, textvariable=language_var, values=language_options, state="disabled", justify="left")
language_menu.grid(row=3, column=1, sticky=W)

selected_file_var = StringVar()

selected_file_menu = ttk.Combobox(frame, textvariable=selected_file_var, state="readonly", justify="left")
selected_file_menu.grid(row=4, column=0, columnspan=2, sticky=W+E)


def browse_files():
    selected_file_path = filedialog.askopenfilename(initialdir='.')
    selected_file_name = os.path.basename(selected_file_path)
    selected_file_var.set(selected_file_name)


audio_file_button = Button(frame, text="Select audio file", command=browse_files)
audio_file_button.grid(row=5, columnspan=2, pady=10)

run_button = Button(frame, text="Run", command=run_batch_script)
run_button.grid(row=6, columnspan=2, pady=10)

root.mainloop()
