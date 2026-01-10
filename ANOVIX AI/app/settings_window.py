from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QCheckBox, QPushButton, QMessageBox
)
from core.config import load_config, save_config


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ANOVIX AI Settings")
        self.setMinimumSize(300, 200)

        self.config = load_config()

        layout = QVBoxLayout()

        self.whatsapp_cb = QCheckBox("Enable WhatsApp Automation")
        self.whatsapp_cb.setChecked(
            self.config.get("whatsapp", {}).get("enabled", False)
        )
        layout.addWidget(self.whatsapp_cb)

        self.voice_cb = QCheckBox("Enable Voice Recognition")
        self.voice_cb.setChecked(
            self.config.get("voice", {}).get("enabled", False)
        )
        layout.addWidget(self.voice_cb)

        self.system_cb = QCheckBox("Enable System Status")
        self.system_cb.setChecked(
            self.config.get("system", {}).get("enabled", False)
        )
        layout.addWidget(self.system_cb)

        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def save(self):
        self.config["whatsapp"]["enabled"] = self.whatsapp_cb.isChecked()
        self.config["voice"]["enabled"] = self.voice_cb.isChecked()
        self.config["system"]["enabled"] = self.system_cb.isChecked()

        save_config(self.config)
        QMessageBox.information(self, "Saved", "Settings saved successfully.")
