from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication
from tkinter import *


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi('gui_login.ui', self)
        self.w1 = CreateAccount()
        self.w2 = MesaurementPuls()
        self.b_createaccount.clicked.connect(self.gotocreateaccount)
        self.b_login.clicked.connect(self.gotomeasurement)

    def gotocreateaccount(self):
        self.w1.show()

    def gotomeasurement(self):
        self.w2.show()

    def messagebox(self):
        QMessageBox.warning(self, 'Komunikat', 'Podany login lub hasło są nieprawidłowe.')


class CreateAccount(QDialog):
    def __init__(self):
        super(CreateAccount, self).__init__()
        loadUi('gui_createaccount.ui', self)
        self.b_create.clicked.connect(self.closewindowcreate)

    def closewindowcreate(self):
        self.destroy()

    # Gotowe komunikaty dotyczące nieprawidłowo podanych danych:

    def messagebox_emptyscope(self):
        QMessageBox.warning(self, 'Komunikat', 'Wszystkie pola muszą być uzupełnione.')

    def messagebox_tooshortlogin(self):
        QMessageBox.warning(self, 'Komunikat', 'Podany login jest za krótki. Musi mieć conajmniej 6 znaków.')

    def messagebox_tooshortpassword(self):
        QMessageBox.warning(self, 'Komunikat', 'Podane hasło jest za krótkie. Musi mieć conajmniej 6 znaków')

    def messagebox_notthesamepassword(self):
        QMessageBox.warning(self, 'Komunikat', 'Podane hasła są różne.')


class MesaurementPuls(QDialog):
    def __init__(self):
        super(MesaurementPuls, self).__init__()
        loadUi('gui_measurement.ui', self)
        self.w4 = Data()
        self.b_seeothers.clicked.connect(self.gotodata)

    def gotodata(self):
        self.w4.show()


class Data(QDialog):
    def __init__(self):
        super(Data, self).__init__()
        loadUi('gui_data.ui', self)


app = QApplication(sys.argv)
window = Login()
window.setWindowTitle('Segmentation')
window.show()
sys.exit(app.exec())
