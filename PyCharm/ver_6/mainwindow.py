from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication
from tkinter import *
import pyodbc
from datetime import datetime

# connection with database:
conn = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=DESKTOP-O6OPF2T\MISIASQL;"
    "Database=PulsometerDatabase;"
    "Trusted_Connection=yes;")

# variable:
nowid = 0


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

        cur = conn.cursor()
        query1 = "select id_użytkownika from dbo.Dane_użytkownika where login = " + "'" + login + "'" + " and password = " + "'" + password + "'" + ";"
        id_user = cur.execute(query1).fetchall()

        for row in id_user:
            id_user = row[0]
            print(id_user)

        for row in count:
            count = row[0]
            print(count)

        if count == 1:
            global nowid
            nowid = id_user
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
        self.b_start.clicked.connect(self.enabledsavedata)
        self.b_save.clicked.connect(self.savedata)

    def gotodata(self):
        self.w4.show()

    def enabledsavedata(self):
        self.b_save.setEnabled(True)

    def savedata(self):
        todaydate = datetime.today().strftime('%Y-%m-%d')
        measurevalue = self.l_puls.text()
        iduser = nowid
        cur = conn.cursor()
        query4 = "Insert into dbo.Pomiar(id_użytkownika, value, data) values('" + str(iduser) + "', '" + measurevalue + "', '" + todaydate + "')"
        cur.execute(query4)
        conn.commit()

        QMessageBox.warning(self, 'Komunikat', 'Pomiar o wartości: ' + measurevalue + ' BPM w dniu: ' + todaydate + ' dodano poprawnie.')


class Data(QDialog):
    def __init__(self):
        super(Data, self).__init__()
        loadUi('gui_data.ui', self)
        self.b_show.clicked.connect(self.downloaddata)

    def downloaddata(self):
        choosedata = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        print(choosedata)
        cur = conn.cursor()
        query1 = "select COUNT(value) from dbo.Pomiar where id_użytkownika = '" + str(nowid) + "' and  data = '" + choosedata + "'"
        count = cur.execute(query1).fetchall()

        for row in count:
            count = row[0]
            print(count)

        if count != 0:
            query2 = "select value from dbo.Pomiar where id_użytkownika = '" + str(nowid) + "' and data = '" + choosedata + "'"
            value = cur.execute(query2).fetchall()

            for row in value:
                value = row[0]
                # trzeba rozwiązać problem więcej niż jedna wartość
                self.l_value.setText(str(value))
                self.l_bpm.setText('BPM')
                print("Value: " + str(value))

        else:
            self.l_bpm.setText('')
            self.l_value.setText('Brak')


app = QApplication(sys.argv)
window = Login()
window.setWindowTitle('Segmentation')
window.show()
sys.exit(app.exec())
