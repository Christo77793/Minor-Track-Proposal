import sys
import os
from PyQt5 import uic
from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtGui as Qtg
from PyQt5 import QtCore as Qtc

# Code to show error, if the app crashes
import cgitb

cgitb.enable(format='text')


class ReportApp(Qtw.QMainWindow):

    def __init__(self):
        super().__init__()  # avoid code redundancy

        uic.loadUi(r"UI\\main_2.ui", self)

        self.setWindowFlag(Qtc.Qt.FramelessWindowHint)

        self.header_frame.mouseMoveEvent = self.move_with_click_title_bar

        self.show()  # show the UI
        self.showMaximized()  # loads the app in full-screen

        self.accepted_file_types = "JPEG (*.jpeg), JPG (*.jpg), PNG (*.png)"

        self.minimiseButton.clicked.connect(lambda: self.showMinimized())
        self.closeButton.clicked.connect(lambda: self.close())

        self.onlyInt = Qtg.QIntValidator()
        self.repeatedCount.setValidator(self.onlyInt)

        self.uploadImage.clicked.connect(self.open_file)

        self.sendReport.clicked.connect(self.send_report)

    def move_with_click_title_bar(self, event):
        if event.buttons() == Qtc.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def open_file(self):
        '''
        Function to open a file
        '''

        print("Before", self.userUploadedImage.width())

        path, test = Qtw.QFileDialog.getOpenFileName(
            parent=self,
            caption="Open File",
            directory="",
            filter=self.accepted_file_types
        )

        print("After", self.userUploadedImage.width())

        pixmap_ = Qtg.QPixmap(path)
        # self.userUploadedImage.setScaledContents(True)
        self.userUploadedImage.setPixmap(pixmap_)
        self.userUploadedImage.repaint()
        Qtw.QApplication.processEvents()

    def send_report(self):
        self.countLabel.setText("")

        name = self.violatorName.toPlainText()
        place = self.violationPlace.toPlainText()
        address = self.violationAddress.toPlainText()
        count = self.repeatedCount.text()

        print("Name", name)
        print("Place", place)
        print("Address", address)
        print("Count", count)

        if name != "" and place != "" and address != "" and count != "":
            count = int(count)
            if count > 5:
                message = "As the count is over 5 times this has been given high priority"
                self.countLabel.setText(message)

            elif 5 >= count >= 0:
                message = "Report submitted"
                self.countLabel.setText(message)

            elif count < 0:
                message = "Invalid input {count}"
                self.countLabel.setText(message)


if __name__ == "__main__":
    app = Qtw.QApplication(sys.argv)
    chat_box = ReportApp()
    sys.exit(app.exec())
