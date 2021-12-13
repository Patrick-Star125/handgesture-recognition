# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication
from Connect.states_html import states_html
from Connect.sanUI import *


class SecondUI(QWidget):
    def __init__(self):
        self.count = 0
        self.san_UI = sanUI()
        self.button = []
        self.button_states = []
        self.person_number = 0
        self.choose_number = "0"
        self.is_open = 0

        self.c_state = states_html()
        super(SecondUI, self).__init__()
        self.resize(300, 400)
        self.setWindowTitle("选择主讲人")
        self.high = 20
        # self.set_person_number(5)

    def change_number(self, text):
        for i in range(0, self.person_number):
            if self.button_states[i] == text:
                self.person_number = i
                print(i)
        self.san_UI.show()

    def set_person_number(self, person_number):
        # QApplication.processEvents()
        self.count = self.person_number
        self.person_number = person_number
        if self.is_open == 1:
            self.show_controller()
            self.is_open = 0

    def clear(self):
        self.button = []

    def show_controller(self):
        self.clear()

        for i in range(0, self.person_number):
            print("i=", i)
            self.button_states.append("参讲人" + str(i))

            self.button.append(QtWidgets.QPushButton(self))
            print("----------------------------", self.button)
            # self.button[i]=QtWidgets.QPushButton(self)
            self.button[i].setGeometry(QtCore.QRect(50, self.high, 200, 50))
            self.button[i].setText(self.button_states[i])
            self.button[i].setStyleSheet("border:2px solid #717171;\n"
                                         "border-radius:10px;\n"
                                         "background:#F1E3FA;\n"
                                         "font-size:15px")
            self.button[i].clicked.connect(lambda: self.change_number(self.sender().text()))
            # self.button[i].show()
            self.high += 70
        self.high = 20

    def get_choose_person(self):
        return self.choose_number


