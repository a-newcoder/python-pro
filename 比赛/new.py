import json
from socket import gethostname,gethostbyname
from sys import argv
from os import system
import matplotlib.pyplot as py
import numpy as nu
import pandas
from PyQt5.QtGui import QPixmap
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, \
    QProgressBar, QFileDialog, QMessageBox, QInputDialog, QTextBrowser, QTextEdit, QComboBox, QLabel


class main(QWidget):
    def __init__(self):
        super(main, self).__init__()
        self.setGeometry(550, 340, 400, 400)
        self.lab = QLabel(self)
        self.lab.setScaledContents(True)
        self.sock = QUdpSocket(self)
        self.sock.bind(QHostAddress.Any, 6666)
        self.sock.readyRead.connect(self.read_data_slot)
        self.sock = QUdpSocket(self)
        self.lab = QLabel(self)
        self.my_IP = QLabel()
        self.choce = QComboBox()
        self.name = QTextEdit()
        self.btn = QPushButton('Start Server', self)
        self.btn.clicked.connect(self.send_data_slot)
        self.mes = QTextEdit()
        self.mes.setPlaceholderText("输入你要发送的消息")


    try:
        with open("people.json", "r+", encoding="utf-8") as file:  # 这里曾经出现问题：把打开模式设置为了a+，导致文件从最后面读取，以至于无法读取到任何数据
            lis = json.load(file)
    except json.decoder.JSONDecodeError or IOError:
        with open("people.json", "w", encoding="utf-8") as file:
            lis = {}
            json.dump({}, file)
    try:
        with open("contacts.json", "r+", encoding="utf-8") as file:  # 这里曾经出现问题：把打开模式设置为了a+，导致文件从最后面读取，以至于无法读取到任何数据
            self.lis = json.load(file)

    except json.decoder.JSONDecodeError or IOError:
        with open("contacts.json", "w", encoding="utf-8") as file:
            self.lis = {}
            json.dump({}, file)