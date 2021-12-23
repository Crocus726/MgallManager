import sys
from PyQt5.QtWidgets import QApplication

from gui import MgallManager


def main():
    app = QApplication(sys.argv)
    ex = MgallManager()
    app.aboutToQuit.connect(ex.ExitHandler)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
