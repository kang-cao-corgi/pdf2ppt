import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QMessageBox
import traceback
from functools import partial
import time
from convert import convert
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
import platform


DEBUG = 0


class WorkerThread(QThread):
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)

    def run(self):
        try:
            self.parent().convert_pdf()

            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))


class FileCopyApp(QWidget):
    def __init__(self):
        super(FileCopyApp, self).__init__()

        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.label_source = QLabel('Select .pdf file:')
        self.label_destination = QLabel('Destination folder:')
        self.label_status = QLabel('Status:')

        self.btn_browse_source = QPushButton('Browse File')
        self.btn_browse_destination = QPushButton('Browse Folder')
        # self.btn_copy_file = QPushButton('Copy File')
        self.btn_convert_pdf = QPushButton('Convert .pdf to .pptx')  # New button

        # Connect buttons to functions
        self.btn_browse_source.clicked.connect(self.browse_source)
        self.btn_browse_destination.clicked.connect(self.browse_destination)
        self.btn_convert_pdf.clicked.connect(self.start_conversion)  # Connect the new button

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_source)
        layout.addWidget(self.btn_browse_source)
        layout.addWidget(self.label_destination)
        layout.addWidget(self.btn_browse_destination)
        # layout.addWidget(self.btn_copy_file)
        layout.addWidget(self.btn_convert_pdf)  # Add the new button to the layout
        layout.addWidget(self.label_status)

        self.setLayout(layout)

        # Set up window
        self.setGeometry(300, 300, 400, 250)  # Increased height for the new button
        self.setWindowTitle('pdf2pptx converter')
        self.show()

        self.source_path = None
        self.destination_path = None

        # Create worker thread
        self.worker_thread = WorkerThread(self)


    def browse_source(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select PDF file')
        if file_path:
            self.label_source.setText(f'PDF file: {file_path}')
            self.source_path = file_path

    def browse_destination(self):
        folder_dialog = QFileDialog()
        folder_path = folder_dialog.getExistingDirectory(self, 'Select Destination Folder')
        if folder_path:
            self.label_destination.setText(f'Destination Folder: {folder_path}')
            self.destination_path = folder_path


    def check_path(self):
        # print(f"{self.source_path=}")
        # print(f"{self.destination_path=}")

        assert self.source_path is not None, "Please select a .pdf file"
        assert self.source_path[-4:].lower() == ".pdf", "File has to be .pdf"
        assert self.destination_path is not None, "Please select where to save .pptx"


    def set_status(self, msg: str):
        self.label_status.setText(f"Status: {msg}")


    def start_conversion(self):
        self.set_status('Busy')
        busy_message_box = self.show_busy_message('Converting...')

        self.worker_thread.finished_signal.connect(partial(self.on_worker_finished, busy_message_box=busy_message_box))
        self.worker_thread.error_signal.connect(partial(self.on_worker_error, busy_message_box=busy_message_box))

        self.worker_thread.start()


    def on_worker_finished(self, busy_message_box: QMessageBox):
        busy_message_box.accept()
        self.set_status('Finished')
        self.show_message('Finished')

    def on_worker_error(self, err_msg: str, busy_message_box: QMessageBox):
        busy_message_box.accept()
        self.set_status('Error')
        self.show_message(f"Error: {err_msg}")


    def sleep(self, amount: int = 2):
        print(f"sleeping {amount}s")
        time.sleep(amount)

    def convert_pdf(self):
        if DEBUG:
            import time
            amount = 2
            print(f"sleeping {amount}s")
            time.sleep(amount)
            return

        self.check_path()
        convert(self.source_path, self.destination_path)
        open_file_explorer(self.destination_path)


    def show_busy_message(self, msg: str):
        busy_message_box = QMessageBox()
        # busy_message_box.setIcon(QMessageBox.Information)
        # busy_message_box.setWindowTitle("Busy")
        busy_message_box.setText(msg)
        busy_message_box.setStandardButtons(QMessageBox.NoButton)
        busy_message_box.show()
        return busy_message_box


    def show_message(self, msg: str):
        success_message = QMessageBox()
        success_message.setIcon(QMessageBox.Information)
        # success_message.setWindowTitle("Success")
        success_message.setText(msg)
        success_message.exec_()


    def get_filename_from_path(self, file_path):
        # Extracts the filename from the given file path
        return file_path.split("/")[-1]



def open_file_explorer(path):
    system_platform = platform.system().lower()

    if system_platform == 'windows':
        subprocess.Popen(['explorer', path], shell=True)
    elif system_platform == 'darwin':
        subprocess.Popen(['open', path])
    else:
        raise Exception(f"Unsupported operating system {system_platform}")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileCopyApp()
    sys.exit(app.exec_())
