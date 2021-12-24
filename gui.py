import os
import logging

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, \
    QLineEdit, QCheckBox, QPushButton, QRadioButton, QComboBox, \
    QGroupBox, QGridLayout
from PyQt5.QtGui import QIcon

from crawler import Crawler
from blocker import Blocker
from deleter import Deleter
from thread import MgallThread
from utils import login, logout, checkauth, get_cur_date, get_cur_time
from icons import icon_path
from const import PROXY_TIME_DICT, MOBILE_TIME_DICT, \
    BLOCK_UPDATE_TIME_DICT, DELETE_UPDATE_TIME_DICT


class MgallManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.gall_id = None
        self.session = None

        self.crawler = None
        self.deleter = None
        self.blocker = None
        self.post_list = []

        self.logger = logging.getLogger()
        LOG_FILENAME = get_cur_date() + ".log"
        Log_Format = "%(levelname)s %(asctime)s %(message)s"
        logging.basicConfig(filename=LOG_FILENAME, format=Log_Format, level="INFO")

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

        self.setWindowTitle("MgallManager")
        self.setWindowIcon(QIcon(icon_path))
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
        self.delete_auto_button.setEnabled(False)
        self.delete_stop_button.setEnabled(False)
        self.delete_message_text.setText("")

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
            self.session = None
            self.crawler = None
            self.blocker = None
        self.initStatus()

    def get_gall_id(self):
        self.gall_id = self.gall_id_text.text()

    def update_blocktime(self):
        if self.crawler is not None and self.blocker is not None:
            texts = self.crawler.get_blocktime()
            try:
                proxy_text, mobile_text = texts
                self.block_proxy_status_text.setText("VPN : " + proxy_text)
                self.block_mobile_status_text.setText("통신사 IP : " + mobile_text)
            except Exception:
                self.manager_status_text.setText("갤러리 접속 불가")
                self.block_proxy_status_text.setText("갤러리 접속 불가")
                self.block_mobile_status_text.setText("갤러리 접속 불가")
                return False

            return True

    def tryCheckauth(self):
        if self.gall_id is None:
            self.get_gall_id()

        if self.session is not None:
            status = checkauth(self.session, self.gall_id)
            if status:
                self.manager_status_text.setText("관리자 권한 확인됨")
                self.crawler = Crawler(self.session, self.gall_id)
                self.crawler.logger = self.logger
                self.blocker = Blocker(self.session, self.gall_id)
                self.blocker.logger = self.logger
                self.deleter = Deleter(self.session, self.gall_id)
                self.deleter.logger = self.logger
                if self.update_blocktime():
                    self.setManagebuttons(True)

            else:
                self.manager_status_text.setText("관리자 권한 없음")
                self.setManagebuttons(False)

        else:
            self.manager_status_text.setText("로그인되지 않음")

    def tryBlock(self):
        proxy_time = self.block_proxy_box.currentText()
        proxy_time = PROXY_TIME_DICT[proxy_time]
        mobile_time = self.block_mobile_box.currentText()
        mobile_time = MOBILE_TIME_DICT[mobile_time]

        if self.blocker is not None:
            self.blocker.block(proxy_time, mobile_time)
            self.update_blocktime()

    def tryBlock_auto(self):
        self.block_auto_button.setEnabled(False)
        self.block_auto_button.setText("활성화됨")
        self.block_stop_button.setEnabled(True)

        proxy_time = self.block_proxy_box.currentText()
        proxy_time = BLOCK_UPDATE_TIME_DICT[proxy_time]
        mobile_time = self.block_mobile_box.currentText()
        mobile_time = BLOCK_UPDATE_TIME_DICT[mobile_time]

        if proxy_time and mobile_time:
            block_time = min(proxy_time, mobile_time)
        else:
            block_time = proxy_time or mobile_time

        if block_time:
            self.block_thread = MgallThread(self, block_time)
            self.block_thread.block()
        else:
            self.tryBlock_stop()

    def tryBlock_stop(self):
        self.block_auto_button.setEnabled(True)
        self.block_auto_button.setText("자동 차단")
        self.block_stop_button.setEnabled(False)
        self.block_thread.stop()

    def get_delete_list(self):
        user_list = self.delete_text.text().replace(" ", "").split(",")

        # 기본 유동닉은 삭제에서 배제
        for i in user_list:
            if "ㅇㅇ" in i:
                user_list.remove(i)

        try:
            self.post_list = self.crawler.get_post_nums(user_list)
        except Exception:
            pass

    def tryDelete(self):
        self.get_delete_list()
        try:
            response = self.deleter.delete(self.post_list)
            if response is None:
                message = "삭제할 글 없음 : "
            elif response is True:
                message = "삭제 완료 : " + str(len(self.post_list)) + "개 : "
            else:
                message = "삭제 불가 : "
            self.delete_message_text.setText(message + get_cur_time())
        except Exception:
            pass

    def tryDelete_auto(self):
        self.delete_auto_button.setEnabled(False)
        self.delete_auto_button.setText("활성화됨")
        self.delete_stop_button.setEnabled(True)

        delete_time = self.delete_box.currentText()
        delete_time = DELETE_UPDATE_TIME_DICT[delete_time]
        self.delete_thread = MgallThread(self, delete_time)
        self.delete_thread.delete()

    def tryDelete_stop(self):
        self.delete_auto_button.setEnabled(True)
        self.delete_auto_button.setText("자동 삭제")
        self.delete_stop_button.setEnabled(False)
        self.delete_thread.stop()
        self.delete_message_text.setText("삭제 중지")

    def ExitHandler(self):
        self.tryLogout()
        os._exit(1)
