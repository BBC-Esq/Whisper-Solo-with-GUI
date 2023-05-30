import os
import subprocess
import shutil
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # create frame
        frame = QWidget(self)
        self.setCentralWidget(frame)
        layout = QGridLayout(frame)

        # Set up the main window
        self.setWindowTitle('Whisper GUI')

        self.model_var = QComboBox()
        self.model_var.addItems([
            "tiny.en", "tiny", "base.en", "base", "small.en", "small",
            "medium.en", "medium", "large", "large-v1", "large-v2"
        ])
        layout.addWidget(QLabel("Choose the Whisper model:"), 0, 0)
        layout.addWidget(self.model_var, 0, 1)

        self.format_var = QComboBox()
        self.format_var.addItems(["txt", "vtt", "srt", "tsv", "json", "all"])
        layout.addWidget(QLabel("Choose the output format:"), 1, 0)
        layout.addWidget(self.format_var, 1, 1)

        self.translate_var = QCheckBox("Translate to English")
        self.translate_var.stateChanged.connect(self.toggle_language_menu)
        layout.addWidget(self.translate_var, 2, 0, 1, 2)

        self.language_var = QComboBox()
        self.language_var.addItems([
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
        ])
        self.language_var.setDisabled(True)
        layout.addWidget(QLabel("Choose the source language:"), 3, 0)
        layout.addWidget(self.language_var, 3, 1)

        self.selected_file_var = QLineEdit()
        self.selected_file_var.setReadOnly(True)
        layout.addWidget(self.selected_file_var, 4, 0, 1, 2)

        file_button = QPushButton('Select audio file')
        file_button.clicked.connect(self.browse_files)
        layout.addWidget(file_button, 5, 0, 1, 2)

        run_button = QPushButton('Run')
        run_button.clicked.connect(self.run_batch_script)
        layout.addWidget(run_button, 6, 0, 1, 2)

    def browse_files(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select an audio file", "", "All Files (*)")
        if fileName:
            self.selected_file_var.setText(fileName)

    def toggle_language_menu(self):
        if self.translate_var.isChecked():
            self.language_var.setEnabled(True)
        else:
            self.language_var.setDisabled(True)
            
    def run_batch_script(self):
        script_name = "solowhisper.bat"
        script_path = shutil.which(script_name)

        if script_path is None:
            print(f"{script_name} not found in the system path. Please check the system path configuration.")
            return

        selected_model = self.model_var.currentText() or ""
        selected_format = self.format_var.currentText() or ""
        selected_file_path = self.selected_file_var.text() or ""

        if not selected_file_path:
            print("No file selected. Exiting...")
            return

        if self.translate_var.isChecked():
            task_flag = "--task translate"
            source_language_flag = f"--language {self.language_var.currentText()}"
        else:
            task_flag = ""
            source_language_flag = ""

        command = f"{script_path} \"{selected_model}\" \"{selected_file_path}\" \"{selected_format}\" \"{task_flag}\" \"{source_language_flag}\""
        subprocess.run(command, shell=True)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
