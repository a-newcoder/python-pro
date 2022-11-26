import json
from os import system
from socket import gethostname, gethostbyname

from PyQt5.QtGui import QPixmap
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication,QWidget, QPushButton, QLabel, QTextBrowser, QVBoxLayout, QMessageBox, \
    QInputDialog, QComboBox, QTextEdit, QHBoxLayout


class Server(QWidget):
    try:
        with open("people.json", "r+", encoding="utf-8") as file:  # 这里曾经出现问题：把打开模式设置为了a+，导致文件从最后面读取，以至于无法读取到任何数据
            lis = json.load(file)
    except json.decoder.JSONDecodeError or IOError:
        with open("people.json", "w", encoding="utf-8") as file:
            lis = {}
            json.dump({}, file)

    def __init__(self):
        super(Server, self).__init__()

        self.lis = None
        self.setGeometry(550, 340, 400, 400)

        self.lab = QLabel(self)
        self.lab.setPixmap(QPixmap("onefile.jpg"))
        self.lab.setScaledContents(True)

        self.lab.lower()

        self.sock = QUdpSocket(self)
        self.sock.bind(QHostAddress.Any, 6666)
        self.sock.readyRead.connect(self.read_data_slot)

        self.Chat_record = QPushButton()
        self.Chat_record.setText("打开聊天记录")
        self.Chat_record.clicked.connect(self.open_chat_record)

        self.browser = QTextBrowser(self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.browser)
        self.layout.addWidget(self.Chat_record)
        self.setLayout(self.layout)

    @staticmethod
    def open_chat_record():
        system("\"E:\\python Project\\contest\\Chat_record.txt\"")

    def read_data_slot(self):
        while self.sock.hasPendingDatagrams():
            datagram, host, port = self.sock.readDatagram(self.sock.pendingDatagramSize())
            if self.is_not(host.toString()):
                messgae = 'message: {}\nHost: {}\n'.format(datagram.decode(), self.lis[host.toString()],
                                                           port)
                with open("Chat_record.txt", "a", encoding="utf-8") as file:
                    file.write("{}:{}\n".format(self.lis[host.toString()], datagram.decode()))
                self.browser.append(messgae)

    def is_not(self, host):
        if host in self.lis:
            return True
        else:
            confirm = QMessageBox.question(self, "安全验证", "有一个陌生信息,是否通过？",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                name = QInputDialog.getText(self, "询问", "请输入他的名或者填写‘陌生’")
                with open("people.json", "r", encoding="utf-8") as file:
                    self.lis = json.load(file)
                self.lis[host] = name[0]
                with open("people.json", "w", encoding="utf-8") as file:
                    json.dump(self.lis, file)
                return True
            if confirm == QMessageBox.No:
                return False

    def resizeEvent(self, *args, **kwargs) -> None:
        x = self.width()
        y = self.height()
        self.lab.resize(x, y)


class Client(QWidget):
    def __init__(self):
        super(Client, self).__init__()
        try:

            with open("contacts.json", "r+", encoding="utf-8") as file:  # 这里曾经出现问题：把打开模式设置为了a+，导致文件从最后面读取，以至于无法读取到任何数据
                self.lis = json.load(file)

        except json.decoder.JSONDecodeError or IOError:
            with open("contacts.json", "w", encoding="utf-8") as file:
                self.lis = {}
                json.dump({}, file)

        self.setGeometry(970, 340, 400, 400)

        self.sock = QUdpSocket(self)

        self.lab = QLabel(self)
        self.lab.setPixmap(QPixmap("onefile.jpg"))
        self.lab.setScaledContents(True)
        self.lab.lower()

        self.my_IP = QLabel()
        self.my_IP.setStyleSheet("color:blue")
        self.my_IP.setStyleSheet("background-color:grey")
        self.my_IP.setText("你的IP地址" + gethostbyname(gethostname()))

        self.choce = QComboBox()

        self.name = QTextEdit()

        self.IP = QTextEdit()
        self.add = QPushButton("添加")
        self.del_ = QPushButton("删除")
        self.name.setPlaceholderText("请输入联系人名字")
        self.IP.setPlaceholderText("请输入联系人ID地址")
        self.add.released.connect(self.add_people)
        self.del_.released.connect(self.del_people)
        self.choce.addItems(self.lis)

        self.btn = QPushButton('Start Server', self)
        self.btn.clicked.connect(self.send_data_slot)
        self.mes = QTextEdit()
        self.mes.setPlaceholderText("输入你要发送的消息")

        self.bottom = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        self.left = QVBoxLayout()
        self.h_layout = QHBoxLayout()

        self.bottom.addWidget(self.add)
        self.bottom.addWidget(self.del_)
        self.v_layout.addWidget(self.my_IP)
        self.v_layout.addWidget(self.mes)
        self.v_layout.addWidget(self.btn)
        self.left.addWidget(self.choce)
        self.left.addWidget(self.name)
        self.left.addWidget(self.IP)
        self.left.addLayout(self.bottom)
        self.h_layout.addLayout(self.left)
        self.h_layout.addLayout(self.v_layout)

        self.setLayout(self.h_layout)

    def send_data_slot(self):
        message = self.mes.toPlainText()

        datagram = message.encode()
        self.sock.writeDatagram(datagram, QHostAddress(self.lis[self.choce.currentText()]), 6666)

    def add_people(self):
        self.lis[self.name.toPlainText()] = self.IP.toPlainText()
        self.choce.clear()
        self.choce.addItems(self.lis)

        with open("contacts.json", "w", encoding="utf-8") as file:
            print(self.lis)
            json.dump(self.lis, file)

        self.IP.clear()
        self.name.clear()

    def del_people(self):
        del self.lis[self.name.toPlainText()]
        self.choce.clear()
        self.choce.addItems(self.lis)

        with open("contacts.json", "w", encoding="utf-8") as file:
            json.dump(self.lis, file)
        self.IP.clear()

    def resizeEvent(self, *args, **kwargs) -> None:
        x = self.width()
        y = self.height()
        self.lab.resize(x, y)


if __name__ == "__main__":
    from sys import argv
    app = QApplication(argv)
    window = Server()
    window2=Client()
    window.show()
    window2.show()
    app.exec_()
