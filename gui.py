import sys
import threading
import timer
import schedule
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from utils import login, logout, checkauth
from crawler import Crawler
from deleter import Deleter
from blocker import Blocker


class MgallManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = threading.Timer(60 * 59, self.tryBlock_auto_press)
        self.gall_id = None
        self.session = None
        self.crawler = None
        self.deleter = None
        self.blocker = None

    def initUI(self):
        layout = QVBoxLayout()

        self.id_text = QLineEdit(self)
        self.id_text.setPlaceholderText("ID")
        self.pw_text = QLineEdit(self)
        self.pw_text.setPlaceholderText("PW")
        self.pw_checkbox = QCheckBox("비밀번호 숨기기", self)
        self.pw_checkbox.stateChanged.connect(self.hidePassword)
        self.pw_checkbox.toggle()
        self.login_button = QPushButton("로그인", self)
        self.login_button.clicked.connect(self.tryLogin)
        self.logout_button = QPushButton("로그아웃", self)
        self.logout_button.setEnabled(False)
        self.logout_button.clicked.connect(self.tryLogout)
        self.login_status_text = QLabel("로그인되지 않음", self)

        self.gall_id_text = QLineEdit(self)
        self.gall_id_text.setPlaceholderText("Gallery ID")
        self.connect_button = QPushButton("권한 확인", self)
        self.connect_button.clicked.connect(self.tryCheckauth)
        self.connect_button.setEnabled(False)
        self.Mgall_rbutton = QRadioButton("마이너 갤러리", self)
        self.mgall_rbutton = QRadioButton("미니 갤러리", self)
        self.manager_status_text = QLabel("로그인되지 않음", self)

        self.block_vpn_text = QLabel("VPN 차단", self)
        self.block_vpn_box = QComboBox(self)
        self.block_vpn_box.addItems(["48시간", "24시간", "차단 해제"])
        self.block_mobile_text = QLabel("통신사 IP 차단", self)
        self.block_mobile_box = QComboBox(self)
        self.block_mobile_box.addItems(["60분", "30분", "차단 해제"])
        self.block_apply_button = QPushButton("적용", self)
        self.block_apply_button.clicked.connect(self.tryBlock)
        self.block_apply_button.setEnabled(False)
        self.block_auto_button = QPushButton("자동 차단", self)
        self.block_auto_button.pressed.connect(self.tryBlock_auto_press)
        self.block_auto_button.setEnabled(False)
        self.block_proxy_status_text = QLabel("VPN : ", self)
        self.block_mobile_status_text = QLabel("통신사 IP : ", self)

        self.delete_text = QLineEdit(self)
        self.delete_text.setPlaceholderText("사용자 ID 리스트 입력")
        self.delete_button = QPushButton("글 삭제", self)
        self.delete_button.setEnabled(False)
        self.delete_interval_text = QLabel("삭제 주기", self)
        self.delete_box = QComboBox(self)
        self.delete_box.addItems(["1분", "3분", "5분", "10분"])
        self.delete_auto_button = QPushButton("자동 삭제", self)
        self.delete_auto_button.setEnabled(False)

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
        managerLayout.addWidget(self.mgall_rbutton, 2, 3)
        managerLayout.addWidget(self.manager_status_text, 3, 2)
        layout.addWidget(managerbox)

        blockerbox = QGroupBox()
        blockerLayout = QGridLayout()
        blockerbox.setLayout(blockerLayout)
        blockerLayout.addWidget(self.block_vpn_text, 2, 2, 1, 2)
        blockerLayout.addWidget(self.block_vpn_box, 2, 4, 1, 1)
        blockerLayout.addWidget(self.block_mobile_text, 3, 2, 1, 2)
        blockerLayout.addWidget(self.block_mobile_box, 3, 4, 1, 1)
        blockerLayout.addWidget(self.block_apply_button, 2, 5, 1, 1)
        blockerLayout.addWidget(self.block_auto_button, 3, 5, 1, 1)
        blockerLayout.addWidget(self.block_proxy_status_text, 5, 2, 1, 3)
        blockerLayout.addWidget(self.block_mobile_status_text, 6, 2, 1, 3)
        layout.addWidget(blockerbox)

        deleterbox = QGroupBox()
        deleterLayout = QGridLayout()
        deleterbox.setLayout(deleterLayout)
        deleterLayout.addWidget(self.delete_text, 1, 2, 1, 3)
        deleterLayout.addWidget(self.delete_button, 1, 5)
        deleterLayout.addWidget(self.delete_interval_text, 2, 2, 1, 2)
        deleterLayout.addWidget(self.delete_box, 2, 4, 1, 1)
        deleterLayout.addWidget(self.delete_auto_button, 2, 5)
        layout.addWidget(deleterbox)

        self.setWindowTitle("MgallManager")
        self.setFixedSize(350, 425)
        self.setLayout(layout)
        self.show()

    def initStatus(self):
        self.login_status_text.setText("로그인되지 않음")
        self.manager_status_text.setText("로그인되지 않음")
        self.connect_button.setText("권한 확인")
        self.block_proxy_status_text.setText("VPN : ")
        self.block_mobile_status_text.setText("통신사 IP : ")
        self.setLoginbuttons(True)
        self.setManagebuttons(False)
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
        self.delete_button.setEnabled(state)
        self.delete_auto_button.setEnabled(state)

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

        return

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

    def tryBlock_auto_press(self):
        self.tryBlock()
        self.block_auto_button.setEnabled(False)
        self.block_auto_button.setText("활성화됨")
        self.timer.start()

    def tryBlock_stop(self):
        self.block_auto_button.setEnabled(True)
        self.block_auto_button.setText("자동 차단")
        self.timer.cancel()

    def ExitHandler(self):
        self.timer.cancel()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    schedule.run_pending()
    ex = MgallManager()
    app.aboutToQuit.connect(ex.ExitHandler)
    sys.exit(app.exec_())
