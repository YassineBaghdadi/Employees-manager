import webbrowser

import pymysql, sys, os, selenium
from firebase import firebase


from PyQt5 import uic, QtCore, QtWidgets, QtGui

# ADMIN_ALLOWED = bool(firebase.FirebaseApplication('https://p-e-i-5ea0c.firebaseio.com', None).get('/HadefGaz/empoyee_salary_manager', ''))
CURRENT_USER = 'Anonymous'

#todo create the tables if not exists




class Err(QtWidgets.QWidget):
    def __init__(self, err=None):
        super(Err, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'err.ui'), self)
        self.move(300, 200)

        self.err_icon.setPixmap(QtGui.QPixmap('src/img/err.png'))
        self.err_icon.setScaledContents(True)
        self.err_txt = ''
        if not err:
            self.err_txt = 'الخطلأ غير معروف'

        self.err_txt = err
        self.err_msg.setText(self.err_txt)
        self.err_title.installEventFilter(self)

    def eventFilter(self, o, e):
        if e.type() == QtCore.QEvent.MouseButtonPress:
            if o is self.err_title:
                webbrowser.open('https://yassinebaghdadi.github.io/')

        return super(Err, self).eventFilter(o, e)



# class Index(QtWidgets.QWidget):
#     def __init__(self):
#         super(Index, self).__init__()
#         uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'index.ui'), self)
#         self.setGeometry(200, 200, 717, 398)
#         self.change_widget(Main())
#         print('app starting ...')
#
#
#     def change_widget(self, widget):
#         for i in reversed(range(self.index_content.count())):
#             self.index_content.itemAt(i).widget().setParent(None)
#         self.index_content.addWidget(widget)


class Login(QtWidgets.QWidget):
    def __init__(self):
        super(Login, self).__init__(None)
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'login.ui'), self)
        self.move(300, 200)
        self.enter.setFocus(True)

        self.enter.clicked.connect(self.login)



    def login(self):
        try:
            print('opening main page ...')
            self.main = Main()
            self.close()
            self.main.show()
        except Exception as e:
            self.err = Err(err=e)
            self.close()
            self.err.show()

        # try:
        #     if self.username.text() and self.passwrd.text():
        #
        #         conn = pymysql.connect()
        #         curs = conn.cursor()
        #         usr = curs.execute(f'SELECT F_name, L_name FROM users WHERE username like "{self.username.text()}, and passwrd like "{self.passwrd.text()}"')
        # except Exception as e:
        #     err(e)


class Main(QtWidgets.QFrame):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'main.ui'), self)
        self.move(300, 200)
        self.history_icon.setPixmap(QtGui.QPixmap('src/img/history.png'))
        self.omal_icon.setPixmap(QtGui.QPixmap('src/img/empl.png'))
        self.history_icon.setScaledContents(True)
        self.omal_icon.setScaledContents(True)
        self.omal_btn.installEventFilter(self)
        self.history_btn.installEventFilter(self)


    def eventFilter(self, o, e) -> bool:
        if (e.type() == QtCore.QEvent.MouseButtonPress):
            if o is self.omal_btn :
                print('opening omal ...')
                self.omal = Omal()
                self.close()
                self.omal.show()

            if o is self.history_btn:
                print('opening history ...')
                self.history = History()
                self.close()
                self.history.show()


        #
        # if e.type() == QtCore.QEvent.HoverEnter:
        #     if o == self.omal_btn :
        #         self.omal_btn.setStyleSheet('border: 5px solid blue;')
        #     if o == self.history_btn :
        #         self.history_btn.setStyleSheet('border: 1px solid blue;')


        if e.type() == QtCore.QEvent.HoverEnter:
            if o == self.omal_btn :
                print('omal hover in successfully')
                self.hover_in(self.omal_btn)
            if o == self.history_btn :
                self.hover_in(self.history_btn)




        return super(Main, self).eventFilter(o, e)

    def hover_in(self, o):
        o.setStyleSheet('border: 5px solid blue;')

    def hover_out(self, o):
        o.setStyleSheet('border: 5px solid blue;')




class Omal(QtWidgets.QWidget):
    def __init__(self):
        super(Omal, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'omal.ui'), self)
        self.move(300, 200)
        self.check_ico.setPixmap(QtGui.QPixmap('src/img/ghiyab.png'))
        self.check_ico.setScaledContents(True)
        self.add_ico.setPixmap(QtGui.QPixmap('src/img/add.png'))
        self.add_ico.setScaledContents(True)
        self.pay_ico.setPixmap(QtGui.QPixmap('src/img/pay.png'))
        self.pay_ico.setScaledContents(True)
        self.list_ico.setPixmap(QtGui.QPixmap('src/img/list.png'))
        self.list_ico.setScaledContents(True)
        self.check.installEventFilter(self)
        self.add.installEventFilter(self)
        self.pay.installEventFilter(self)
        self.empl_list.installEventFilter(self)
        self.back_btn.clicked.connect(self.back)

    def back(self):
        self.main = Main()
        self.close()
        self.main.show()

    def eventFilter(self, o, e) -> bool:
        if e.type() == QtCore.QEvent.MouseButtonPress:
            if o is self.add:
                print('opening history ...')
                self.add = Add()
                self.close()
                self.add.show()
            if o is self.empl_list:
                print('opening empl list ...')
                self.emlL =Omal_list()
                self.close()
                self.emlL.show()

            if o is self.pay:
                print('opening Paying page ...')
                self.pay_ = Pay()
                self.close()
                self.pay_.show()

            if o is self.check:
                print('opening Check in page ...')
                self.checkin = Checkin()
                self.close()
                self.checkin.show()

        if e.type() == QtCore.QEvent.HoverEnter:
            if o == self.check:
                self.check.setStyleSheet('border: 1px solid blue;')
            if o == self.pay:
                self.pay.setStyleSheet('border: 1px solid blue;')
            if o == self.empl_list:
                self.empl_list.setStyleSheet('border: 1px solid blue;')
            if o == self.add:
                self.add.setStyleSheet('border: 1px solid blue;')

        return super(Omal, self).eventFilter(o, e)


class History(QtWidgets.QWidget):
    def __init__(self, h=True):
        super(History, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'history.ui'), self)
        self.move(300, 200)
        self.h = h
        self.back_btn.clicked.connect(self.back)
        self.title = ''
        if not h:#todo for change the title if not history window
            self.title = ''

    def back(self):
        if self.h:
            self.main = Main()
        else:
            self.main = Omal()
        self.close()
        self.main.show()

class Add(QtWidgets.QWidget):
    def __init__(self):
        super(Add, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'add.ui'), self)
        self.move(300, 200)

        self.back_btn.clicked.connect(self.back)


    def back(self):
        self.main = Omal()
        self.close()
        self.main.show()


class Pay(QtWidgets.QWidget):
    def __init__(self):
        super(Pay, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'pay.ui'), self)
        self.move(300, 200)

        self.back_btn.clicked.connect(self.back)


    def back(self):
        self.main = Omal()
        self.close()
        self.main.show()

class Omal_list(QtWidgets.QWidget):
    def __init__(self):
        super(Omal_list, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'omal_list.ui'), self)
        self.move(300, 200)

        self.back_btn.clicked.connect(self.back)


    def back(self):
        self.main = Omal()
        self.close()
        self.main.show()


class Checkin(QtWidgets.QWidget):
    def __init__(self):
        super(Checkin, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'checkin.ui'), self)

        self.move(300, 200)
        self.cancel.clicked.connect(self.back)

    def back(self):
        self.main = Omal()
        self.close()
        self.main.show()


class Logs():
    def __init__(self, user, operation_id ):
        pass




if __name__ == '__main__':
    # print(f'from firebase : {ADMIN_ALLOWED}')
    # print(f'Current User before : {CURRENT_USER}')
    app = QtWidgets.QApplication(sys.argv)
    login = Login()

    print(f'Current User after : {CURRENT_USER}')
    login.show()
    # err = Err(err='test')
    # err.show()
    app.exec_()
