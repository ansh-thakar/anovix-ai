from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QPushButton,
    QVBoxLayout, QWidget, QMessageBox, QTextEdit
)
from core.config import load_config
from features.notes import add_note, read_notes
from features.focus_timer import FocusTimer
from features.system_status import get_system_status
from core.permission import is_enabled
from PyQt6.QtWidgets import QInputDialog
from core.permission import is_enabled
from features.automation.whatsapp import send_whatsapp_message
from features.voice.voice_engine import VoiceEngine



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ANOVIX AI")
        self.setMinimumSize(800, 500)

        self.config = load_config()

        layout = QVBoxLayout()

        self.info = QLabel("ANOVIX AI is running safely.")
        layout.addWidget(self.info)

        self.test_btn = QPushButton("Test App")
        self.test_btn.clicked.connect(self.test_click)
        layout.addWidget(self.test_btn)

        # ---------- NOTES UI ----------
        self.notes_box = QTextEdit()
        self.notes_box.setPlaceholderText("Write a note here...")
        layout.addWidget(self.notes_box)

        self.save_note_btn = QPushButton("Save Note")
        self.save_note_btn.clicked.connect(self.save_note)
        layout.addWidget(self.save_note_btn)

        self.show_notes_btn = QPushButton("Show Notes")
        self.show_notes_btn.clicked.connect(self.show_notes)
        layout.addWidget(self.show_notes_btn)

        # ---------- FOCUS TIMER UI ----------
        self.focus_25_btn = QPushButton("Start 25 min Focus")
        self.focus_25_btn.clicked.connect(lambda: self.start_focus(25))
        layout.addWidget(self.focus_25_btn)

        self.focus_5_btn = QPushButton("Start 5 min Break")
        self.focus_5_btn.clicked.connect(lambda: self.start_focus(5))
        layout.addWidget(self.focus_5_btn)

        # ---------- SYSTEM STATUS UI ----------
        self.status_btn = QPushButton("Show System Status")
        self.status_btn.clicked.connect(self.show_status)
        layout.addWidget(self.status_btn)

        # ---------- WHATSAPP UI ----------
        self.whatsapp_btn = QPushButton("Send WhatsApp Message")
        self.whatsapp_btn.clicked.connect(self.send_whatsapp)
        layout.addWidget(self.whatsapp_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        #------------------voice ui----------------------
        self.start_voice_btn = QPushButton("Start Voice Listening")
        self.start_voice_btn.clicked.connect(self.start_voice)
        layout.addWidget(self.start_voice_btn)
        self.stop_voice_btn = QPushButton("Stop Voice Listening")
        self.stop_voice_btn.clicked.connect(self.stop_voice)
        self.stop_voice_btn.setEnabled(False)
        layout.addWidget(self.stop_voice_btn)
        self.voice_engine = None

    def test_click(self):
        QMessageBox.information(self, "OK", "App structure working correctly.")

    def save_note(self):
        text = self.notes_box.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Empty", "Note is empty")
            return
        add_note(text)
        self.notes_box.clear()
        QMessageBox.information(self, "Saved", "Note saved successfully")

    def show_notes(self):
        notes = read_notes()
        QMessageBox.information(self, "Notes", notes)

    def start_focus(self, minutes):
        self.focus_timer = FocusTimer(minutes, self.focus_finished)
        self.focus_timer.start()
        QMessageBox.information(
            self,
            "Focus Started",
            f"{minutes} minute timer started. Stay focused!"
        )

    def focus_finished(self):
        QMessageBox.information(
            self,
            "Time Up",
            "Great work! Your focus session is complete."
        )

    def show_status(self):
        config = load_config()
        if not is_enabled(self.config, "system"):
            QMessageBox.warning(
            self,
            "Disabled",
            "System features are disabled in settings."
        )
            return
        status = get_system_status()
        msg = (
            f"CPU Usage: {status['cpu']}%\n"
            f"RAM Usage: {status['ram']}%\n"
            f"Battery: {status['battery']}%"
        )
        QMessageBox.information(self, "System Status", msg)

    def send_whatsapp(self):
        config = load_config()

        if not is_enabled(config, "whatsapp"):
            QMessageBox.warning(
            self,
            "Disabled",
            "WhatsApp feature is disabled in settings."
            )
            return

        number, ok = QInputDialog.getText(
           self,
           "WhatsApp",
           "Enter phone number (without country code):"
         )
        if not ok or not number.strip():
            return

        message, ok = QInputDialog.getMultiLineText(
            self,
        "WhatsApp Message",
        "Enter message:"
    )
        if not ok or not message.strip():
          return

        confirm = QMessageBox.question(
            self,
            "Confirm",
            f"Send this message to {number}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            send_whatsapp_message(
               config["whatsapp"]["country_code"],
               number.strip(),
               message.strip()
             )
            QMessageBox.information(self, "Success", "WhatsApp message sent.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def start_voice(self):
        config = load_config()

        if not is_enabled(config, "voice"):
            QMessageBox.warning(
             self,
            "Disabled",
            "Voice recognition is disabled in settings."
        )
            return

        try:
            self.voice_engine = VoiceEngine(
            language=config["voice"].get("language", "en-IN")
        )
            self.start_voice_btn.setEnabled(False)
            self.stop_voice_btn.setEnabled(True)

            text = self.voice_engine.listen_once()
            QMessageBox.information(self, "You said", text)

        except Exception as e:
            QMessageBox.critical(self, "Voice Error", str(e))
            self.stop_voice()

    def stop_voice(self):
        self.voice_engine = None
        self.start_voice_btn.setEnabled(True)
        self.stop_voice_btn.setEnabled(False)

