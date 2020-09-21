# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'KaHaShEr.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os, hashlib, string
from PyQt5 import QtCore, QtGui, QtWidgets
from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property


class AppContext(ApplicationContext):
    @cached_property
    def swap_icon(self):
        return QtGui.QPixmap(self.get_resource('icons/swap.svg'))

    @cached_property
    def checked_icon(self):
        return QtGui.QPixmap(self.get_resource('icons/checked.svg'))

    @cached_property
    def x_mark_icon(self):
        return QtGui.QPixmap(self.get_resource('icons/x-mark.svg'))

    @cached_property
    def bulb_icon(self):
        return QtGui.QPixmap(self.get_resource('icons/bulb.svg'))

    @cached_property
    def people_icon(self):
        return QtGui.QPixmap(self.get_resource('icons/people.png'))

    @cached_property
    def import_icon(self):
        return QtGui.QPixmap(self.get_resource('icons/import.svg'))

    @cached_property
    def reset_icon(self):
        return QtGui.QPixmap(self.get_resource('icons/reset.svg'))


''' Global variables '''
last_open_directory = None
selected_file_path = None
current_clipboard_txt_val = None
hash_type_all = ["MD5", "SHA1", "SHA256", "SHA512"]
current_hash_type_index = 0
clipboard_changed_from_app = False

''' Util functions '''


def get_hash_type():
    global hash_type_all, current_hash_type_index
    return hash_type_all[current_hash_type_index]


def is_hex(s):
    return all(char in string.hexdigits for char in s)


def get_file_checksum(fp, hash_func):
    with open(fp, mode='rb') as f:
        for chunk in iter(lambda: f.read(1024), b''):
            hash_func.update(bytes(chunk))
        checksum = hash_func.hexdigest()
    return checksum


def calculate_file_checksum(fp):
    if get_hash_type().lower() == "md5":
        md5 = hashlib.md5()
        return get_file_checksum(fp, hash_func=md5)
    if get_hash_type().lower() == "sha1":
        sha1 = hashlib.sha1()
        return get_file_checksum(fp, hash_func=sha1)
    elif get_hash_type().lower() == "sha256":
        sha256 = hashlib.sha256()
        return get_file_checksum(fp, hash_func=sha256)
    elif get_hash_type().lower() == "sha512":
        sha512 = hashlib.sha512()
        return get_file_checksum(fp, hash_func=sha512)
    else:
        raise ValueError('Choose a valid hash type [md5, sha1, sha256, sha512 ]')


def get_file_name(fp):
    return fp.split(os.sep)[-1]


def format_hash_result(txt, block_n=64):
    if block_n >= len(txt):
        return txt
    fmt_txt, txt_length = '', len(txt)
    for x in range(txt_length // block_n):
        fmt_txt += txt[:block_n] + ' '
        txt = txt[block_n:txt_length]
    return fmt_txt


def undo_format_hash_result(txt):
    return ''.join([char for char in txt if char != ' '])


class Ui_MainWindow(object):

    def __init__(self):
        self.app_context = AppContext()

    def ui_set_success_compare(self):
        _translate = QtCore.QCoreApplication.translate
        self.compare_result_label.setText(_translate("MainWindow", 'Perfect match'))
        self.compare_result_label.setVisible(True)
        self.compare_result_icon.setVisible(True)
        self.compare_result_icon.setPixmap(self.app_context.checked_icon)
        self.compare_result_label.setStyleSheet("font-weight: bold; font-size: 12pt; color: rgb(95, 211, 141)")

    def ui_set_error_compare(self):
        _translate = QtCore.QCoreApplication.translate
        self.compare_result_label.setText(_translate("MainWindow", 'Do not match'))
        self.compare_result_label.setVisible(True)
        self.compare_result_icon.setVisible(True)
        self.compare_result_icon.setPixmap(self.app_context.x_mark_icon)
        self.compare_result_label.setStyleSheet("font-weight: bold;font-size: 12pt; color: rgb(198, 54, 54)")

    def ui_hide_compare_result(self):
        self.compare_result_label.setVisible(False)
        self.compare_result_icon.setVisible(False)

    def ui_set_compare_tip_visibility(self, show):
        _translate = QtCore.QCoreApplication.translate
        self.compare_tips_label.setText(_translate("MainWindow", "Copy the hash value in the clipboard to compare"))
        self.compare_tip_icon_label.setVisible(show)
        self.compare_tips_label.setVisible(show)

    def ui_set_hash_copy_info_visibility(self, show):
        _translate = QtCore.QCoreApplication.translate
        self.hash_copy_info.setText(_translate("MainWindow", "Successfully copied!"))
        self.hash_copy_info.setVisible(show)
        self.hash_copy_info.setStyleSheet("font-weight: bold; font-size: 12pt; color: rgb(95, 211, 141)")

    def next_hash_type(self):
        global hash_type_all, current_hash_type_index
        current_hash_type_index = (current_hash_type_index + 1) % len(hash_type_all)
        global selected_file_path
        if selected_file_path:
            self.hash_result_label.setText(calculate_file_checksum(selected_file_path))
        self.next_hash_button.setText(hash_type_all[current_hash_type_index])

    def on_push_import_button(self):
        global selected_file_path, last_open_directory, current_clipboard_txt_val
        user_download_path = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.DownloadLocation)[0]

        fp = QtWidgets.QFileDialog(directory=user_download_path).getOpenFileName()[0]

        if fp:
            self.on_push_reset_button()
            selected_file_path = fp

            f_name = get_file_name(fp)
            self.filename_label.setText(f_name)
            self.file_extension_label.setText(f_name.split('.')[-1])
            self.hash_result_label.setText(format_hash_result(calculate_file_checksum(fp)))
            self.ui_set_compare_tip_visibility(True)

    def on_push_next_hash_button(self):
        global selected_file_path, hash_type_all, current_hash_type_index
        current_hash_type_index = (current_hash_type_index + 1) % len(hash_type_all)
        next_hash_type_index = (current_hash_type_index + 1) % len(hash_type_all)

        if selected_file_path:
            self.hash_result_label.setText(
                format_hash_result(calculate_file_checksum(selected_file_path)))
        self.current_hash_label.setText(hash_type_all[current_hash_type_index])
        self.next_hash_label.setText(hash_type_all[next_hash_type_index])

        self.ui_set_hash_copy_info_visibility(False)
        self.ui_hide_compare_result()

    def on_clipboard_change(self):
        global current_clipboard_txt_val, clipboard_changed_from_app
        current_clipboard_txt_val = QtWidgets.QApplication.clipboard().text()

        if clipboard_changed_from_app:
            self.ui_hide_compare_result()
            self.ui_set_hash_copy_info_visibility(True)
            clipboard_changed_from_app = False
        else:
            if is_hex(current_clipboard_txt_val) and self.hash_result_label.text():
                if current_clipboard_txt_val == undo_format_hash_result(self.hash_result_label.text()):
                    self.ui_set_success_compare()
                else:
                    self.ui_set_error_compare()
                self.ui_set_compare_tip_visibility(False)
                self.ui_set_hash_copy_info_visibility(False)

    def on_push_reset_button(self):
        global selected_file_path
        selected_file_path = None
        _translate = QtCore.QCoreApplication.translate

        self.file_extension_label.setText(":)")
        self.filename_label.setText(_translate("MainWindow", "The most minimalist and smart checksum verifier ever !"))
        self.hash_result_label.setText("")

        self.ui_hide_compare_result()
        self.ui_set_hash_copy_info_visibility(False)
        self.ui_set_compare_tip_visibility(False)

    def on_push_result_label(self, ev):
        global clipboard_changed_from_app

        hash_result_val = undo_format_hash_result(self.hash_result_label.text())
        if hash_result_val:
            QtWidgets.QApplication.clipboard().setText(hash_result_val)
            clipboard_changed_from_app = True

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        ''' Center app on screen fuck the traditional technics '''
        app_width, app_height = 801, 600
        qr = QtWidgets.QDesktopWidget().screenGeometry()
        left = (qr.width() // 2) - (app_width // 2)
        top = (qr.height() // 2) - (app_height // 2)
        MainWindow.setGeometry(left, top, app_width, app_height)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(-1, 0, 811, 601))
        self.frame.setStyleSheet("font-family: Roboto, sans-serif, sans, Arial, Helvetica;\n"
                                 "background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.illustration_img_label = QtWidgets.QLabel(self.frame)
        self.illustration_img_label.setGeometry(QtCore.QRect(130, 160, 591, 111))
        self.illustration_img_label.setText("")
        self.illustration_img_label.setPixmap(self.app_context.people_icon)
        self.illustration_img_label.setObjectName("illustration_img_label")
        self.hash_result_label = QtWidgets.QLabel(self.frame)
        self.hash_result_label.setGeometry(QtCore.QRect(90, 340, 641, 61))
        self.hash_result_label.setStyleSheet("border-radius: 6px;\n"
                                             "border: 2px solid rgb(0, 0, 0);\n"
                                             "padding-left: 6px;\n"
                                             "padding-right: 6px;\n"
                                             "font-size: 13pt;\n"
                                             "color: rgb(0, 0, 0);\n"
                                             "font-weight: bold;")
        self.hash_result_label.setWordWrap(True)
        self.hash_result_label.setAlignment(QtCore.Qt.AlignVCenter)
        self.hash_result_label.setObjectName("hash_result_label")
        self.file_extension_label = QtWidgets.QLabel(self.frame)
        self.file_extension_label.setGeometry(QtCore.QRect(354, 10, 100, 100))
        self.file_extension_label.setStyleSheet("font-size: 15pt;\n"
                                                "background-color: rgb(0, 0, 0);\n"
                                                "color: #fff;\n"
                                                "border-radius: 50%;\n"
                                                "")
        self.file_extension_label.setAlignment(QtCore.Qt.AlignCenter)
        self.file_extension_label.setObjectName("file_extension_label")
        self.reset_button = QtWidgets.QPushButton(self.frame)
        self.reset_button.setGeometry(QtCore.QRect(100, 500, 111, 41))
        self.reset_button.setStyleSheet("\n"
                                        "QPushButton {\n"
                                        "    background-color: rgb(6, 6, 6);\n"
                                        "    color: #fff;\n"
                                        "    border-radius: 8px;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover {\n"
                                        "    background-color: rgb(89, 89, 89);\n"
                                        "}")
        icon = QtGui.QIcon()
        icon.addPixmap(self.app_context.reset_icon, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reset_button.setIcon(icon)
        self.reset_button.setObjectName("reset_button")
        self.compare_tips_label = QtWidgets.QLabel(self.frame)
        self.compare_tips_label.setGeometry(QtCore.QRect(410, 510, 400, 31))
        self.compare_tips_label.setStyleSheet("font-size: 11pt;\n"
                                              "color: rgb(0, 0, 0);")
        self.compare_tips_label.setObjectName("compare_tips_label")
        self.compare_tip_icon_label = QtWidgets.QLabel(self.frame)
        self.compare_tip_icon_label.setGeometry(QtCore.QRect(380, 500, 31, 51))
        self.compare_tip_icon_label.setText("")
        self.compare_tip_icon_label.setPixmap(self.app_context.bulb_icon)
        self.compare_tip_icon_label.setObjectName("compare_tip_icon_label")
        self.compare_result_label = QtWidgets.QLabel(self.frame)
        self.compare_result_label.setGeometry(QtCore.QRect(90, 30, 111, 41))
        self.compare_result_label.setStyleSheet("font-size: 12pt;\n"
                                                "color: rgb(95, 211, 141);\n"
                                                "font-weight: bold;\n"
                                                "")
        self.compare_result_label.setObjectName("compare_result_label")
        self.import_button = QtWidgets.QPushButton(self.frame)
        self.import_button.setGeometry(QtCore.QRect(350, 430, 111, 41))
        self.import_button.setStyleSheet("\n"
                                         "QPushButton {\n"
                                         "    background-color: rgb(6, 6, 6);\n"
                                         "    color: #fff;\n"
                                         "    border-radius: 8px;\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:hover {\n"
                                         "    background-color: rgb(89, 89, 89);\n"
                                         "}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(self.app_context.import_icon, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.import_button.setIcon(icon1)
        self.import_button.setObjectName("import_button")
        self.compare_result_icon = QtWidgets.QLabel(self.frame)
        self.compare_result_icon.setGeometry(QtCore.QRect(200, 30, 41, 31))
        self.compare_result_icon.setText("")
        self.compare_result_icon.setPixmap(self.app_context.checked_icon)
        self.compare_result_icon.setObjectName("compare_result_icon")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(570, 570, 231, 21))
        self.label.setStyleSheet("font-size: 12px;")
        self.label.setObjectName("label")
        self.current_hash_label = QtWidgets.QLabel(self.frame)
        self.current_hash_label.setGeometry(QtCore.QRect(90, 290, 71, 31))
        self.current_hash_label.setStyleSheet("font-size: 13pt;\n"
                                              "color: rgb(0, 0, 0);\n"
                                              "font-weight: bold;")
        self.current_hash_label.setObjectName("current_hash_label")
        self.next_hash_label = QtWidgets.QLabel(self.frame)
        self.next_hash_label.setGeometry(QtCore.QRect(658, 290, 71, 41))
        self.next_hash_label.setStyleSheet("font-size: 13pt;\n"
                                           "color: rgb(0, 0, 0);\n"
                                           "font-weight: bold;")
        self.next_hash_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.next_hash_label.setObjectName("next_hash_label")
        self.next_hash_button = QtWidgets.QPushButton(self.frame)
        self.next_hash_button.setGeometry(QtCore.QRect(370, 290, 61, 36))
        self.next_hash_button.setStyleSheet("\n"
                                            "QPushButton {\n"
                                            "    background-color: rgb(255, 255, 255);\n"
                                            "    border: 0 solid none;\n"
                                            "}\n"
                                            "\n"
                                            "\n"
                                            "QPushButton:hover {\n"
                                            "    background-color: rgb(237, 237, 237);\n"
                                            "}")
        self.next_hash_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(self.app_context.swap_icon, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next_hash_button.setIcon(icon2)
        self.next_hash_button.setObjectName("next_hash_button")
        self.filename_label = QtWidgets.QLabel(self.frame)
        self.filename_label.setGeometry(QtCore.QRect(64, 130, 681, 20))
        self.filename_label.setStyleSheet("font-weight: bold;\n"
                                          "color: rgb(138, 146, 167);")
        self.filename_label.setAlignment(QtCore.Qt.AlignCenter)
        self.filename_label.setObjectName("filename_label")
        self.hash_copy_info = QtWidgets.QLabel(self.frame)
        self.hash_copy_info.setGeometry(QtCore.QRect(540, 40, 201, 31))
        self.hash_copy_info.setStyleSheet("font-weight: bold;\n"
                                          "color: rgb(138, 146, 167);")
        self.hash_copy_info.setAlignment(QtCore.Qt.AlignCenter)
        self.hash_copy_info.setObjectName("hash_copy_info")

        ''' Connected slots to buttons  '''
        self.reset_button.clicked.connect(self.on_push_reset_button)
        self.import_button.clicked.connect(self.on_push_import_button)
        self.next_hash_button.clicked.connect(self.on_push_next_hash_button)
        self.hash_result_label.mouseReleaseEvent = self.on_push_result_label
        QtWidgets.QApplication.clipboard().dataChanged.connect(self.on_clipboard_change)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "KaHaShEr"))
        self.hash_result_label.setText(
            _translate("MainWindow", ""))
        self.file_extension_label.setText(_translate("MainWindow", ":)"))
        self.reset_button.setText(_translate("MainWindow", "Reset"))
        self.compare_tips_label.setText(
            _translate("MainWindow", "Copy the hash value in the clipboard to compare"))
        self.compare_result_label.setText(_translate("MainWindow", ""))
        self.import_button.setText(_translate("MainWindow", "Import"))
        self.label.setText(_translate("MainWindow", "© 2020 Copyright | Abdoulaye Koumare"))
        self.current_hash_label.setText(_translate("MainWindow", "MD5"))
        self.next_hash_label.setText(_translate("MainWindow", "SHA1"))
        self.filename_label.setText(
            _translate("MainWindow", "The most minimalist and smartest checksum verifier ever !"))
        self.hash_copy_info.setText(_translate("MainWindow", "Successfully copied!"))
        self.hash_copy_info.setVisible(False)
        self.compare_result_icon.setVisible(False)

        self.ui_set_compare_tip_visibility(False)
        self.hash_result_label.setToolTip("Click to copy the content")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
