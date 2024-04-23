import sys
import time
from threading import Thread
from goose_lib.optional_gui_goose import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class GooseTab(QWidget):
    def __init__(self):
        super().__init__()

        self.instance = GOOSE()
        self.gooseTab_layout = QVBoxLayout()
        self.setLayout(self.gooseTab_layout)

        self.textbox_label_map = {}
        self.all_data_widgets = {}

        goose_msg = {
            "Source MAC": {"type": "string", "default": self.instance.get_src_mac()},
            "Destination MAC": {"type": "string", "default": "FF:FF:FF:FF:FF:FF"},
            "appId": {"type": "integer", "default": "1"},
            "gocbRef": {"type": "string", "default": "GEDeviceF650/LLN0$GO$gcb01"},
            "timeAllowedToLive": {"type": "integer", "default": "4000"},
            "datSet": {"type": "string", "default": "GEDeviceF650/LLN0$GOOSE1"},
            "goId": {"type": "string", "default": "GEDevGOOSE1"},
            "t": {"type": "time", "default": time.time()},
            "stNum": {"type": "integer", "default": "1"},
            "sqNum": {"type": "integer", "default": "1"},
            "simulation": {"type": "boolean", "default": False},
            "confRev": {"type": "integer", "default": "1"},
            "ndsCom": {"type": "boolean", "default": False},
            "numDatSetEntries": {"type": "integer", "default": "0"},
            "allData": {"type": "array"},
        }

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.on_send_button_clicked)
        self.gooseTab_layout.addWidget(send_button)

        for key, value in goose_msg.items():
            hbox = QHBoxLayout()
            label = QLabel(f"{key}:")
            label.setMinimumWidth(120)

            if value["type"] == "array":
                all_data_combo = QComboBox()
                all_data_combo.addItems(["Boolean", "Int", "Visible String"])
                hbox.addWidget(label)
                hbox.addWidget(all_data_combo)
                add_button = QPushButton("+")
                add_button.setFixedWidth(50)
                add_button.clicked.connect(self.add_new_data_widget)
                hbox.addWidget(add_button)
                self.gooseTab_layout.addLayout(hbox)
            elif value["type"] == "time":
                self.time_edit = QDateTimeEdit(self)
                self.time_edit.setDateTime(QDateTime.currentDateTime())
                self.time_edit.setFixedWidth(400)
                hbox.addWidget(label)
                hbox.addWidget(self.time_edit)
                self.gooseTab_layout.addLayout(hbox)
                self.time_edit.editingFinished.connect(self.update_time)
            elif value["type"] == "integer" or value["type"] == "string":
                textbox = QLineEdit(value["default"])
                textbox.setStyleSheet("QLineEdit { border: 1px solid gray; }")
                textbox.setFixedWidth(400)
                hbox.addWidget(label)
                hbox.addWidget(textbox)
                self.gooseTab_layout.addLayout(hbox)
                self.textbox_label_map[textbox] = label
                textbox.textChanged.connect(self.on_textbox_or_radiobutton_changed)
            elif value["type"] == "boolean":
                groupbox = QButtonGroup(self)
                radio_true = QRadioButton("True")
                radio_false = QRadioButton("False")
                radio_false.setChecked(True)
                hbox.addWidget(label)
                hbox.addWidget(radio_true)
                hbox.addWidget(radio_false)
                self.gooseTab_layout.addLayout(hbox)
                self.textbox_label_map[radio_true] = label
                groupbox.addButton(radio_true)
                groupbox.addButton(radio_false)
                radio_true.toggled.connect(self.on_textbox_or_radiobutton_changed)

    def add_new_data_widget(self):
        combo_box = self.sender().parent().findChild(QComboBox)
        data_type = combo_box.currentText()
        count = len(self.all_data_widgets)

        hbox = QHBoxLayout()
        label = QLabel(f"{count}_{data_type}:")
        if data_type != "Boolean":
            textbox = QLineEdit()
            textbox.setStyleSheet("QLineEdit { border: 1px solid gray; }")
            textbox.setFixedWidth(400)
            hbox.addWidget(label)
            hbox.addWidget(textbox)
            self.all_data_widgets[textbox] = label

        else:
            groupbox = QButtonGroup(self)
            radio_true = QRadioButton("True")
            radio_false = QRadioButton("False")
            radio_false.setChecked(True)
            hbox.addWidget(label)
            hbox.addWidget(radio_true)
            hbox.addWidget(radio_false)
            groupbox.addButton(radio_true)
            groupbox.addButton(radio_false)
            self.all_data_widgets[radio_true] = label

        self.gooseTab_layout.addLayout(hbox)

    def set_allData(self):
        value = None
        msg = b""
        for widget, label in self.all_data_widgets.items():
            allDataType = label.text()[2:-1:]
            if isinstance(widget, QLineEdit):
                value = widget.text()
                if value.strip() == "":
                    continue
            elif isinstance(widget, QRadioButton):
                value = widget.isChecked()
            match allDataType:
                case "Boolean":
                    msg += (b"\x83\x01" + bytes([value]))
                case "Int":
                    msg += (b"\x85\x04" + int(value).to_bytes(4, byteorder="big"))
                case "Visible String":
                    byte_string = [ord(i) for i in widget.text()]
                    msg += (b"\x8a" + bytes([len(value) + 1]) + bytes(byte_string))
        self.instance.goose_msg["allData"] = msg

    def on_send_button_clicked(self):
        self.set_allData()
        Thread(target=self.instance.send).start()

    def update_time(self):
        self.instance.goose_msg["t"] = self.time_edit.dateTime().toSecsSinceEpoch()

    def on_textbox_or_radiobutton_changed(self):
        widget = self.sender()
        label = self.textbox_label_map[widget]
        key = label.text()[:-1]

        value = None
        if isinstance(widget, QLineEdit):
            value = widget.text()
        elif isinstance(widget, QRadioButton):
            value = widget.isChecked()
        if key in ["appId", "stNum", "sqNum", "confRev", "numDatSetEntries"]:
            value = int(value)
            if value >= (2**8) or value < 0:
                value = 0
                widget.setText(str(value))
        elif key == "timeAllowedToLive":
            value = int(value)
            if value >= (2**16) or value < 0:
                value = 0
                widget.setText(str(value))
        elif key in ["gocbRef", "datSet", "goId"]:
            value = value.encode("utf-8")

        if key in ["Source MAC", "Destination MAC"]:
            if key == "Source MAC":
                self.instance.src_mac = value
            else:
                self.instance.dest_mac = value
        else:
            self.instance.goose_msg[key] = value


class MainTab(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tab Example")
        self.setGeometry(100, 100, 900, 600)
        self.setFixedSize(800, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab1 = QWidget()
        self.goose_tab = GooseTab()

        self.tabs.addTab(self.goose_tab, "GOOSE")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainTab()
    window.show()
    sys.exit(app.exec_())
