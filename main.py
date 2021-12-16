from PyQt5.QtWidgets import QApplication
import sys
from gui import MgallManager

def main():
    app = QApplication(sys.argv)
    ex = MgallManager()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
