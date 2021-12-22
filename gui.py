import os
import time
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from utils import login, logout, checkauth
from crawler import Crawler
from blocker import Blocker
from deleter import Deleter
from const import BLOCK_TIME, DELETE_TIME


class MgallManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.block_timer = threading.Timer(BLOCK_TIME, self.tryBlock_auto)
        self.delete_timer = threading.Timer(DELETE_TIME, self.tryDelete_auto)
        self.gall_id = None
        self.session = None

        self.crawler = None
        self.deleter = None
        self.blocker = None
        self.post_list = []

    def initUI(self):
        layout = QVBoxLayout()

        self.id_text = QLineEdit(self)
        self.pw_text = QLineEdit(self)
        self.pw_checkbox = QCheckBox(self)
        self.login_button = QPushButton(self)
        self.logout_button = QPushButton(self)
        self.logout_button.setEnabled(False)
        self.login_status_text = QLabel(self)
        self.gall_id_text = QLineEdit(self)
        self.connect_button = QPushButton(self)
        self.connect_button.setEnabled(False)
        self.Mgall_rbutton = QRadioButton(self)
        self.Mgall_rbutton.toggle()
        # self.mgall_rbutton = QRadioButton(self)
        self.manager_status_text = QLabel(self)

        self.block_proxy_text = QLabel(self)
        self.block_proxy_box = QComboBox(self)
        self.block_mobile_text = QLabel(self)
        self.block_mobile_box = QComboBox(self)
        self.block_apply_button = QPushButton(self)
        self.block_apply_button.setEnabled(False)
        self.block_auto_button = QPushButton(self)
        self.block_auto_button.setEnabled(False)
        self.block_stop_button = QPushButton(self)
        self.block_stop_button.setEnabled(False)
        self.block_proxy_status_text = QLabel(self)
        self.block_mobile_status_text = QLabel(self)

        self.delete_text = QLineEdit(self)
        self.delete_button = QPushButton(self)
        self.delete_button.setEnabled(False)
        self.delete_interval_text = QLabel(self)
        self.delete_box = QComboBox(self)
        self.delete_auto_button = QPushButton(self)
        self.delete_auto_button.setEnabled(False)
        self.delete_message_text = QLabel(self)
        self.delete_stop_button = QPushButton(self)
        self.delete_stop_button.setEnabled(False)

        self.buttonConnect()
        self.initTexts()

        loginbox = QGroupBox()
        loginLayout = QGridLayout()
        loginbox.setLayout(loginLayout)
        loginLayout.addWidget(self.id_text, 1, 2)
        loginLayout.addWidget(self.pw_text, 2, 2)
        loginLayout.addWidget(self.pw_checkbox, 4, 2)
        loginLayout.addWidget(self.login_button, 1, 3, 1, 1)
        loginLayout.addWidget(self.logout_button, 2, 3, 1, 1)
        loginLayout.addWidget(self.login_status_text, 5, 2)
        layout.addWidget(loginbox)

        managerbox = QGroupBox()
        managerLayout = QGridLayout()
        managerbox.setLayout(managerLayout)
        managerLayout.addWidget(self.gall_id_text, 1, 2, 1, 3)
        managerLayout.addWidget(self.connect_button, 1, 5)
        managerLayout.addWidget(self.Mgall_rbutton, 2, 2)
        # managerLayout.addWidget(self.mgall_rbutton, 2, 3)
        managerLayout.addWidget(self.manager_status_text, 3, 2)
        layout.addWidget(managerbox)

        blockerbox = QGroupBox()
        blockerLayout = QGridLayout()
        blockerbox.setLayout(blockerLayout)
        blockerLayout.addWidget(self.block_proxy_text, 2, 2, 1, 2)
        blockerLayout.addWidget(self.block_proxy_box, 2, 4, 1, 1)
        blockerLayout.addWidget(self.block_mobile_text, 3, 2, 1, 2)
        blockerLayout.addWidget(self.block_mobile_box, 3, 4, 1, 1)
        blockerLayout.addWidget(self.block_apply_button, 2, 5, 1, 1)
        blockerLayout.addWidget(self.block_auto_button, 3, 5, 1, 1)
        blockerLayout.addWidget(self.block_proxy_status_text, 5, 2, 1, 3)
        blockerLayout.addWidget(self.block_mobile_status_text, 6, 2, 1, 3)
        blockerLayout.addWidget(self.block_stop_button, 5, 5, 1, 1)
        layout.addWidget(blockerbox)

        deleterbox = QGroupBox()
        deleterLayout = QGridLayout()
        deleterbox.setLayout(deleterLayout)
        deleterLayout.addWidget(self.delete_text, 1, 2, 1, 3)
        deleterLayout.addWidget(self.delete_button, 1, 5)
        deleterLayout.addWidget(self.delete_interval_text, 2, 2, 1, 2)
        deleterLayout.addWidget(self.delete_box, 2, 4, 1, 1)
        deleterLayout.addWidget(self.delete_auto_button, 2, 5)
        deleterLayout.addWidget(self.delete_message_text, 3, 2, 1, 3)
        deleterLayout.addWidget(self.delete_stop_button, 3, 5, 1, 1)
        layout.addWidget(deleterbox)

        ### 추후 업데이트 ###
        self.block_proxy_box.setEnabled(False)
        self.block_mobile_box.setEnabled(False)
        self.delete_box.setEnabled(False)

        self.setWindowTitle("MgallManager")
        self.setFixedSize(350, 450)
        self.setLayout(layout)
        self.show()

    def buttonConnect(self):
        self.login_button.clicked.connect(self.tryLogin)
        self.logout_button.clicked.connect(self.tryLogout)
        self.pw_checkbox.stateChanged.connect(self.hidePassword)
        self.pw_checkbox.toggle()
        self.connect_button.clicked.connect(self.tryCheckauth)
        self.block_apply_button.clicked.connect(self.tryBlock)
        self.block_auto_button.pressed.connect(self.tryBlock_auto)
        self.block_stop_button.pressed.connect(self.tryBlock_stop)
        self.delete_button.pressed.connect(self.tryDelete)
        self.delete_auto_button.pressed.connect(self.tryDelete_auto)
        self.delete_stop_button.pressed.connect(self.tryDelete_stop)

    def initTexts(self):
        self.id_text.setPlaceholderText("ID")
        self.pw_text.setPlaceholderText("PW")
        self.pw_checkbox.setText("비밀번호 숨기기")
        self.login_button.setText("로그인")
        self.logout_button.setText("로그아웃")
        self.login_status_text.setText("로그인되지 않음")

        self.gall_id_text.setPlaceholderText("Gallery ID")
        self.connect_button.setText("권한 확인")
        self.Mgall_rbutton.setText("마이너 갤러리")
        # self.mgall_rbutton.setText("미니 갤러리")
        self.manager_status_text.setText("로그인되지 않음")

        self.block_proxy_text.setText("VPN 차단")
        self.block_proxy_box.addItems(["48시간", "24시간", "차단 해제"])
        self.block_mobile_text.setText("통신사 IP 차단")
        self.block_mobile_box.addItems(["60분", "30분", "차단 해제"])
        self.block_apply_button.setText("적용")
        self.block_auto_button.setText("자동 차단")
        self.block_stop_button.setText("차단 중지")
        self.block_proxy_status_text.setText("VPN : ")
        self.block_mobile_status_text.setText("통신사 IP : ")

        self.delete_text.setPlaceholderText("사용자 ID 리스트 입력")
        self.delete_button.setText("글 삭제")
        self.delete_interval_text.setText("삭제 주기")
        self.delete_box.addItems(["1분", "3분", "5분", "10분"])
        self.delete_auto_button.setText("자동 삭제")
        self.delete_stop_button.setText("삭제 중지")

    def initStatus(self):
        self.login_status_text.setText("로그인되지 않음")
        self.manager_status_text.setText("로그인되지 않음")
        self.connect_button.setText("권한 확인")
        self.block_proxy_status_text.setText("VPN : ")
        self.block_mobile_status_text.setText("통신사 IP : ")
        self.setLoginbuttons(True)
        self.setManagebuttons(False)
        self.block_stop_button.setEnabled(False)
        self.block_auto_button.setEnabled(False)
        self.block_auto_button.setText("자동 차단")

    def setLoginbuttons(self, state: bool):
        self.id_text.setEnabled(state)
        self.pw_text.setEnabled(state)
        self.login_button.setEnabled(state)
        self.logout_button.setEnabled(not state)
        self.connect_button.setEnabled(not state)

    def setManagebuttons(self, state: bool):
        self.block_apply_button.setEnabled(state)
        self.block_auto_button.setEnabled(state)
        self.block_stop_button.setEnabled(not state)
        self.delete_button.setEnabled(state)
        self.delete_auto_button.setEnabled(state)
        self.delete_stop_button.setEnabled(not state)

    def hidePassword(self):
        if self.pw_checkbox.isChecked():
            self.pw_text.setEchoMode(QLineEdit.Password)

        else:
            self.pw_text.setEchoMode(QLineEdit.Normal)

    def tryLogin(self):
        user_id = self.id_text.text()
        user_pw = self.pw_text.text()

        self.session = login(user_id, user_pw)
        if self.session is None:
            self.login_status_text.setText("로그인 실패")
            return

        else:
            self.login_status_text.setText("로그인 완료")
            self.manager_status_text.setText("로그인 완료")
            self.setLoginbuttons(False)
            return

    def tryLogout(self):
        if self.session is not None:
            logout(self.session)
            self.block_timer.__init__(BLOCK_TIME, self.tryBlock_auto)
            self.delete_timer.__init__(DELETE_TIME, self.tryDelete_auto)
            self.session = None
            self.crawler = None
            self.blocker = None
        self.initStatus()

    def get_gall_id(self):
        self.gall_id = self.gall_id_text.text()

    def update_blocktime(self):
        if self.crawler is not None and self.blocker is not None:
            texts = self.crawler.get_blocktime()
            if texts is not None:
                proxy_text, mobile_text = texts
                self.block_proxy_status_text.setText("VPN : " + proxy_text)
                self.block_mobile_status_text.setText("통신사 IP : " + mobile_text)

    def tryCheckauth(self):
        if self.gall_id is None:
            self.get_gall_id()

        if self.session is not None:
            status = checkauth(self.session, self.gall_id)
            if status:
                self.manager_status_text.setText("관리자 권한 확인됨")
                self.crawler = Crawler(self.session, self.gall_id)
                self.blocker = Blocker(self.session, self.gall_id)
                self.deleter = Deleter(self.session, self.gall_id)
                self.update_blocktime()
                self.setManagebuttons(True)

            else:
                self.manager_status_text.setText("관리자 권한 없음")
                self.setManagebuttons(False)

        else:
            self.manager_status_text.setText("로그인되지 않음")

    def tryBlock(self):
        if self.blocker is not None:
            self.blocker.block()
            self.update_blocktime()

    def tryBlock_auto(self):
        self.tryBlock()
        self.block_auto_button.setEnabled(False)
        self.block_auto_button.setText("활성화됨")
        self.block_stop_button.setEnabled(True)
        if not self.block_timer.is_alive():
            self.block_timer.start()

    def tryBlock_stop(self):
        self.block_auto_button.setEnabled(True)
        self.block_auto_button.setText("자동 차단")
        self.block_stop_button.setEnabled(False)
        self.block_timer.__init__(BLOCK_TIME, self.tryBlock_auto)

    def get_delete_list(self):
        user_list = self.delete_text.text().replace(" ", "").split(",")

        for i in user_list:
            if "ㅇㅇ" in i:
                user_list.remove(i)

        if self.crawler is not None:
            self.post_list = self.crawler.get_post_nums(user_list)

    def tryDelete(self):
        self.get_delete_list()

        if self.deleter is not None:
            response = self.deleter.delete(self.post_list)

            if response is None:
                message = "삭제할 글 없음"
            elif response is True:
                message = "삭제 완료 : " + str(len(self.post_list)) + "개"
            else:
                message = "삭제 불가"

            now = time.localtime()
            current_time = " : %04d.%02d.%02d %02d:%02d:%02d" \
                % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
            self.delete_message_text.setText(message + current_time)

    def tryDelete_auto(self):
        self.tryDelete()
        self.delete_auto_button.setEnabled(False)
        self.delete_auto_button.setText("활성화됨")
        self.delete_stop_button.setEnabled(True)
        if not self.delete_timer.is_alive():
            self.delete_timer.start()

    def tryDelete_stop(self):
        self.delete_auto_button.setEnabled(True)
        self.delete_auto_button.setText("자동 차단")
        self.delete_stop_button.setEnabled(False)
        self.delete_timer.__init__(DELETE_TIME, self.tryDelete_auto)

    def ExitHandler(self):
        self.tryLogout()
        os._exit(1)
