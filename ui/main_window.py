# ui/main_window.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QTimer, Qt
from core.modbus_controller import ModbusController
from config.settings import APP_TITLE, RELAY_COUNT, COM_PORT

class MainWindow(QMainWindow):
    """
    Main application window for controlling the Modbus relays.
    """
    def __init__(self):
        super().__init__()
        self.modbus_controller = ModbusController()
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.status_label = QLabel("Not Connected")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

        self.relay_widgets = []
        for i in range(1, RELAY_COUNT + 1):
            relay_widget = self.create_relay_widget(i)
            self.relay_widgets.append(relay_widget)
            self.layout.addWidget(relay_widget)

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.toggle_connection)
        self.layout.addWidget(self.connect_button)

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_ui_state)

        # --- กำหนด Stylesheet ---
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5dc; /* สีเบจ (Beige) สำหรับพื้นหลังหน้าต่างหลัก */
            }
            QLabel {
                color: #333; /* สีเทาเข้มสำหรับข้อความ */
                font-size: 14px;
            }
            QPushButton {
                background-color: #a0522d; /* สีน้ำตาลอ่อน (Sienna) สำหรับพื้นหลังปุ่ม */
                color: #fff; /* สีขาวสำหรับข้อความบนปุ่ม */
                border: 1px solid #704214; /* ขอบปุ่ม */
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8b4513; /* สีน้ำตาลเข้มขึ้นเมื่อเมาส์ชี้ */
            }
            QWidget {
                background-color: transparent; /* ทำให้ Widget ภายในโปร่งใสถ้าไม่ต้องการสีพื้นหลัง */
            }
        """)

    def create_relay_widget(self, relay_number):
        """Creates a widget for a single relay with a label and two buttons."""
        h_layout = QHBoxLayout()

        label = QLabel(f"Relay {relay_number}")
        h_layout.addWidget(label)

        on_button = QPushButton("ON")
        on_button.clicked.connect(lambda: self.set_relay_state(relay_number, True))
        h_layout.addWidget(on_button)
        on_button.setStyleSheet("""
            QPushButton {
                background-color: #556b2f; /* สีเขียวเข้ม (DarkOliveGreen) สำหรับปุ่ม ON */
                color: #fff;
                border: 1px solid #3c4f21;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #4a5d29;
            }
        """)

        off_button = QPushButton("OFF")
        off_button.clicked.connect(lambda: self.set_relay_state(relay_number, False))
        h_layout.addWidget(off_button)
        off_button.setStyleSheet("""
            QPushButton {
                background-color: #8b0000; /* สีแดงเข้ม (DarkRed) สำหรับปุ่ม OFF */
                color: #fff;
                border: 1px solid #5e0000;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #730000;
            }
        """)

        widget = QWidget()
        widget.setLayout(h_layout)
        return widget

    def toggle_connection(self):
        """Connects or disconnects from the Modbus device."""
        if self.modbus_controller.is_connected:
            self.modbus_controller.disconnect()
            self.connect_button.setText("Connect")
            self.status_label.setText("Disconnected")
            self.refresh_timer.stop()
            self.connect_button.setStyleSheet("""
                QPushButton {
                    background-color: #a0522d;
                    color: #fff;
                    border: 1px solid #704214;
                    padding: 5px 15px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #8b4513;
                }
            """)
        else:
            if self.modbus_controller.connect():
                self.connect_button.setText("Disconnect")
                self.status_label.setText(f"Connected to {COM_PORT}")
                self.refresh_timer.start(1000)  # Refresh every 1 second
                self.connect_button.setStyleSheet("""
                    QPushButton {
                        background-color: #778899; /* สีเทาอ่อน (LightSlateGray) สำหรับปุ่ม Disconnect */
                        color: #fff;
                        border: 1px solid #4f5b66;
                        padding: 5px 15px;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #606c76;
                    }
                """)
            else:
                self.status_label.setText("Connection Failed!")

    def set_relay_state(self, relay_number, state):
        """Sends a command to turn a relay ON or OFF."""
        success, message = self.modbus_controller.write_relay_state(relay_number, state)
        if not success:
            print(f"Error setting relay {relay_number} state: {message}")
            self.status_label.setText(f"Error: {message}")
        else:
            self.status_label.setText(f"Relay {relay_number} set to {'ON' if state else 'OFF'}.")

    def refresh_ui_state(self):
        """Reads the current state of all relays and updates the UI."""
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())