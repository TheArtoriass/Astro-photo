#-------------------------------- Importations neccessaire --------------------------------#
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt

#-------------------------------- Classe ClicLineEdit --------------------------------#
class ClicLineEdit(QLineEdit):
    """
    Classe qui permet de changer la couleur du texte et de l'aligner à gauche lorsqu'on clique dessus

    Méthodes:
    - __init__(self, parent=None) : constructeur de la classe
    - mousePressEvent(self, event) : permet de changer la couleur du texte et de l'aligner à gauche

    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        """
        Cette méthode permet de changer la couleur du texte et de l'aligner à gauche
        """
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setStyleSheet("color: white;")
        super().mousePressEvent(event)