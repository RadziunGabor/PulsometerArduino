from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication
from tkinter import *
import pyodbc

# connection with database
conn = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=DESKTOP-O6OPF2T\MISIASQL;"
    "Database=PulsometerDatabase;"
    "Trusted_Connection=yes;")


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi('gui_login.ui', self)
        self.w1 = CreateAccount()
        self.w2 = MesaurementPuls()
        self.b_createaccount.clicked.connect(self.gotocreateaccount)
        self.b_login.clicked.connect(self.checkdata)

    def checkdata(self):
        login = self.et_login.text()
        password = self.et_password.text()

        print(login)
        print(password)

        cur = conn.cursor()
        query = "select count(login) from dbo.Dane_użytkownika where login = " + "'" + login + "'" + " and password = " + "'" + password + "'" + ";"
        count = cur.execute(query).fetchall()

        for row in count:
            count = row[0]
            print(count)

        if count == 1:
            self.gotomeasurement()

        if count == 0:
            self.messagebox()
        cur.close()

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
        self.b_create.clicked.connect(self.createaccount)

    def createaccount(self):
        newlogin = self.et_putlogin.text()
        newpassword = self.et_putpassword.text()
        repeatpassword = self.et_repeatpassword.text()

        countlogin = len(newlogin)
        countpassword = len(newpassword)

        if newlogin and newpassword and repeatpassword != '':
            if countlogin > 6:
                if countpassword > 6:
                    if newpassword == repeatpassword:
                        cur = conn.cursor()
                        query = "select count(login) from dbo.Dane_użytkownika where login = " + "'" + newlogin + "'" + ";"
                        count = cur.execute(query).fetchall()

                        for row in count:
                            count = row[0]
                            print(count)

                        if count == 1:
                            self.messagebox_exist()

                        if count == 0:
                            cur = conn.cursor()
                            query1 = "insert into dbo.Dane_użytkownika (login, password) values " + "('" + newlogin + "', '" + newpassword + "')"
                            cur.execute(query1)

                            conn.commit()
                            self.messegebox_good()
                            self.closewindowcreate()

                    else:
                        self.messagebox_notthesamepassword()
                else:
                    self.messagebox_tooshortpassword()
            else:
                self.messagebox_tooshortlogin()
        else:
            self.messagebox_emptyscope()

    def closewindowcreate(self):
        self.destroy()

    # Gotowe komunikaty dotyczące nieprawidłowo podanych danych:

    def messegebox_good(self):
        QMessageBox.warning(self, 'Komunikat', 'Rejestracja przebiegła pomyślnie.')

    def messagebox_exist(self):
        QMessageBox.warning(self, 'Komunikat', 'Taki login już istnieje w bazie.')

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
