import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from main import lzv_compress, lzv_decompress
from main_window import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)

        self.openFileButton.clicked.connect(self.open_file)
        self.codeTextButton.clicked.connect(self.code_text)
        self.saveCodedTextButton.clicked.connect(self.save_coded_file)

        self.openCodedFileButton.clicked.connect(self.open_coded_file)
        self.decodeTextButton.clicked.connect(self.decode_text)

        self.text = ""
        self.coded_data = ""

    def open_file(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                        'Open File',
                                                        './',
                                                        'Text Files (*.txt)')
        if not file:
            return
        with open(file, 'r') as f:
            self.text = f.read()
        self.textOriginal.setText(self.text)
        self.codeTextButton.setEnabled(True)

    def code_text(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.coded_data = lzv_compress(self.text)
        coded_text = " ".join(map(str, self.coded_data))
        self.textCoded.setText(coded_text[:100_000])
        self.saveCodedTextButton.setEnabled(True)
        QApplication.restoreOverrideCursor()

    def save_coded_file(self):
        try:
            with open('great.txt', 'w') as f:
                f.write(" ".join(map(str, self.coded_data)))
        except Exception as e:
            print(e)

    def open_coded_file(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        with open('great.txt', 'r') as f:
            coded_text = f.read()
        self.coded_data = list(map(int, coded_text.split()))
        self.textOriginal_2.setText(coded_text[:100_000])
        self.decodeTextButton.setEnabled(True)
        QApplication.restoreOverrideCursor()

    def decode_text(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        decoded_text = lzv_decompress(self.coded_data)
        self.textCoded_2.setText(decoded_text)
        QApplication.restoreOverrideCursor()


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()