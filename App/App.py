#-------------------------------- Importations neccessaire --------------------------------#
import sys
from PyQt6.QtWidgets import QApplication
from MenuWindow import MenuWindow


#-------------------------------- Main -------------------------------- #
def main():
    app = QApplication(sys.argv)
    main_window = MenuWindow(app)
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()