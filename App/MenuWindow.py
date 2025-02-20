#-------------------------------- Importations neccessaire --------------------------------#
import sys
import os
import subprocess
import cv2
import numpy as np

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox, QScrollArea, QMainWindow, QDockWidget, QSplitter
from PyQt6.QtGui import QPixmap, QImage, QFontDatabase, QFont
from PyQt6.QtCore import Qt

from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilenames

# Importation de la classe ClicLineEdit et de la classe ModificationsImageWindow
from ClicLineEdit import ClicLineEdit
from ModificationsImageWindow import ModificationsImageWindow


#----------------------------------Classe MenuWindow----------------------------------#
class MenuWindow(QMainWindow):
    """
    Classe qui permet de créer la fenêtre principale de ll'application

    Méthodes:
    - __init__(self, app: QApplication): Constructeur de la classe
    - modifier_valeur_flou(self) -> None: Cette méthode permet de modifier la valeur de flou dans le QLineEdit
    - afficher_parametre(self) -> None: Cette méthode permet d'afficher ou de cacher la fenêtre paramètre
    - retour_menu(self) -> None: Cette méthode permet de retourner au menu principal
    - supprimer_element(self, widget: QWidget) -> bool: Cette méthode permet de supprimer un widget
    - afficher_image_en_grand(self, image_info: tuple) -> None: Cette méthode permet d'afficher une image dans une fenêtre avec possibilité de la modifier avec des outils (luminosité, contraste, etc.)
    - ajouter_images(self) -> None: Cette méthode permet d'ajouter des images
    - enregistrer_images(self) -> None: Cette méthode permet d'enregistrer les images cochées dans un dossier spécifié par l'utilisateur
    """

    def __init__(self, app):
        super().__init__()

        # Charger la police 
        font_id = QFontDatabase.addApplicationFont("font/megatrans.otf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.setFont(QFont(font_family))

        # Recuperer les dimensions de l'écran
        self.screen = app.primaryScreen()
        self.screen_size = self.screen.size()
        self.screen_width = self.screen_size.width()
        self.screen_height = self.screen_size.height() 

        # Empêcher le redimensionnement de la fenêtre
        self.setFixedSize(int(self.screen_width / 1.2) , int(self.screen_height / 1.2))

        # Charger le style CSS
        repertoire_courant = os.path.dirname(os.path.realpath(__file__))
        style_path = os.path.join(repertoire_courant, 'style.css')
        with open(style_path, 'r') as f:
            style = f.read()

        # Appliquer le style à l'ensemble de l'application
        self.setStyleSheet(style)

        # Créer une mise en page verticale pour le widget principal
        central_widget = QWidget()

        # Créer un widget pour l'en-tête
        widget_entete = QWidget()
        widget_entete.setObjectName("entete")
        layout_horizontal_entete = QHBoxLayout()

        # Ajouter un QLabel avec le texte "Gradient Remover" à gauche de l'en-tête
        entete_nom_app = QLabel("Gradient\nRemover")
        entete_nom_app.setObjectName("entete_nom_app")

        # Cree un QSplitter pour afficher le bouton parametre dans la zone sous l'en-tête
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Créer un bouton pour afficher la fenetre parametre
        self.bouton_parametre = QPushButton("Parametres")
        self.bouton_parametre.setObjectName("bouton_parametre")
        self.bouton_parametre.clicked.connect(self.afficher_parametre)

        # Créer un QDockWidget pour afficher les parametres
        self.parametre_dock = QDockWidget(self)
        self.parametre_dock.setObjectName("parametre_dock")
        self.parametre_dock.setWidget(QWidget())
        self.parametre_dock.setStyleSheet("background-color: black;")
        self.parametre_dock.hide()
        self.parametre_dock.setTitleBarWidget(QWidget())

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.parametre_dock)
        self.parametre_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable | QDockWidget.DockWidgetFeature.DockWidgetMovable)

        self.valeur_flou: int = 100

        # Créer un widget pour les parametres
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Valeur Flou")
        label.setObjectName("texte_parametre")
        layout.addWidget(label)

        entree_layout = QHBoxLayout()

        # Créer un QLineEdit pour modifier la valeur de flou
        self.line_edit = ClicLineEdit()
        self.line_edit.setObjectName("line_edit_valeur_flou")
        self.line_edit.setText(str(self.valeur_flou))
        self.line_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.line_edit.returnPressed.connect(self.modifier_valeur_flou)
        entree_layout.addWidget(self.line_edit)

        # Créer un bouton pour valider la valeur de flou
        entree_button = QPushButton("->")
        entree_button.setObjectName("bouton_entree_valeur_flou")
        entree_button.clicked.connect(self.modifier_valeur_flou)
        entree_layout.addWidget(entree_button)

        layout.addLayout(entree_layout)
        layout.addStretch(1)
        widget.setLayout(layout)
        self.parametre_dock.setWidget(widget)

        widget_entete.setMinimumHeight(80)
        widget_entete.setMaximumHeight(80)

        # Ajouter le label et le bouton à la mise en page horizontale
        layout_horizontal_entete.addWidget(entete_nom_app)
        layout_horizontal_entete.addStretch()
        layout_horizontal_entete.addWidget(self.bouton_parametre)

        widget_entete.setLayout(layout_horizontal_entete)

        # Créer un layout vertical pour le widget principal
        layout_vertical = QVBoxLayout()
        layout_vertical.setSpacing(0)
        layout_vertical.addWidget(widget_entete)

        # Créer un widget pour la zone sous l'en-tête
        widget_contenu = QWidget()
        self.layout_vertical_contenu = QVBoxLayout()
        self.layout_vertical_contenu.addStretch()  

        # Créer un bouton pour ajouter des images
        self.bouton_milieu = QPushButton("Ajouter des images")
        self.bouton_milieu.setObjectName("bouton_ajouter_image")

        style = f"""
            #bouton_ajouter_image {{
                background-color: black;
                color: white;
                font-family: "megatrans demo";
                font-size: 35px;
                max-width: {self.screen_width/4}px;
                margin-left: {self.screen_width/3.5}px;
            }}
          """

        # Appliquer le style au widget
        self.bouton_milieu.setStyleSheet(style)
        self.bouton_milieu.setMinimumHeight(100)
        self.bouton_milieu.clicked.connect(self.ajouter_images)

        # Ajouter le bouton à la zone sous l'en-tête
        self.layout_vertical_contenu.addWidget(self.bouton_milieu)
        self.layout_vertical_contenu.addStretch()
        widget_contenu.setLayout(self.layout_vertical_contenu)
        widget_contenu.setObjectName("zone_sous_entete")

        # Appliquer la mise en page verticale au widget principal
        central_widget.setLayout(layout_vertical)

        # Ajouter le widget de la zone sous l'en-tête à la mise en page verticale
        layout_vertical.addWidget(widget_contenu)

        # Ajouter le widget de la zone sous l'en-tête et le QDockWidget au QSplitter
        self.splitter.addWidget(widget_contenu)
        self.splitter.addWidget(self.parametre_dock)

        # Ajouter le QSplitter à la mise en page verticale
        layout_vertical.addWidget(self.splitter)

        # Ajouter le widget principal à la fenêtre
        self.setCentralWidget(central_widget)


    def modifier_valeur_flou(self) -> None:
        """
        Cette méthode permet de modifier la valeur de flou dans le QLineEdit
        """
        try:
            # On récupère la valeur entrée par l'utilisateur
            self.valeur_flou: int = int(self.line_edit.text())
        except ValueError:
            # Si l'utilisateur entre autre chose que des chiffres, on affiche un message d'erreur et on remet la valeur à 50
            self.valeur_flou: int = 100
            print("Veuillez entrer des chiffres.")

        # On affiche la valeur de flou dans le QLineEdit
        self.line_edit.setText(str(self.valeur_flou))
        self.line_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.line_edit.clearFocus() 
        self.line_edit.setStyleSheet("color: grey;")

    def afficher_parametre(self) -> None:
        """
        Cette méthode permet d'afficher ou de cacher la fenêtre paramètre
        """
        self.splitter.setSizes([int(self.height() * 0.7), int(self.height() * 0.2)])
        if self.parametre_dock.isHidden():
            self.parametre_dock.show()
        else:
            self.parametre_dock.hide()

    def retour_menu(self) -> None:
        """
        Cette méthode permet de retourner au menu principal
        """
        # Si on clique sur retour menu alors on quitte et on relance le programme
        self.close()
        subprocess.Popen([sys.executable] + sys.argv)

    def supprimer_element(self, widget: QWidget) -> bool:
        """
        Cette méthode permet de supprimer un widget

        Args:
        - widget (QWidget): Le widget à supprimer

        Returns:
        - bool: True si le widget a été supprimé, False sinon
        """

        self.layout_vertical_contenu.removeWidget(widget)
        widget.deleteLater()
        return True

    def afficher_image_en_grand(self, image_info: tuple) -> None:        
        """
        Cette méthode permet d'afficher une image dans une fenêtre avec possibilité de la modifier avec des outils (luminosité, contraste, etc.)
        
        Args:
        - image_info (tuple): Un tuple contenant l'image, le nom de l'image et la checkbox de l'image

        Returns:
        - None

        Comportement:
        - Appelle la classe ModificationsImageWindow pour afficher l'image en grand avec des outils pour modifier l'image
        """

        # Créer une fenêtre à l'aide de la classe ModificationsImageWindow
        self.fenetre_image = ModificationsImageWindow(image_info)

        # Afficher la fenetre en plein ecran
        self.fenetre_image.showMaximized()
        self.fenetre_image.show()


    def ajouter_images(self) -> None:
        """
        Cette méthode permet d'ajouter des images
        """

        # Créer une liste pour stocker les images
        self.liste_image: list[tuple[str, np.ndarray]] = []
       
        #----------------------------------Demander à l'utilisateur de choisir les images à nettoyer----------------------------------#
        # Créer une fenêtre Tkinter pour la sélection de fichier
        Tk().withdraw() 
        root = Tk()
        root.withdraw()

        types_fichiers: tuple[str, ...] = [
        ("Image files", "*.png;*.jpg;*.jpeg"),
        ("All files", "*.*")
        ]   

        # Demander à l'utilisateur de choisir l'image à nettoyer
        chemins_images: tuple[str, ...] = askopenfilenames(filetypes=types_fichiers)

        # Si l'utilisateur n'a pas sélectionné d'image, on quitte la fonction
        if not chemins_images:
            print("Aucune image sélectionnée.")
            return

        # Extraire le chemin du dossier à partir du premier chemin d'image sélectionné
        self.chemin_dossier: str = os.path.dirname(chemins_images[0])
        #----------------------------------------------------------------------------------------------------------------------------#
        
        # Changer le texte du bouton parametre en "Retour menu" et changer la fonction du bouton
        self.bouton_parametre.setText("Retour menu")
        self.bouton_parametre.clicked.disconnect()  
        self.bouton_parametre.clicked.connect(self.retour_menu) 

        # Supprimer le bouton ajouter image et le parametre dock
        self.supprimer_element(self.bouton_milieu)
        self.supprimer_element(self.parametre_dock)
        
        for chemin_image in chemins_images:
            # Ouvrir l'image d'astrophotographie
            image_ressource: np.ndarray = cv2.imread(chemin_image)
            
            # Récupérer le nom du fichier sans le chemin ni l'extension
            nom_fichier_ressource: str = os.path.splitext(os.path.basename(chemin_image))[0]
            
            # Reperer les étoiles et cree un masque noit dessus pour les exclure
            image_gris = cv2.cvtColor(image_ressource, cv2.COLOR_BGR2GRAY)

            # Appliquer un seuillage pour détecter les étoiles
            _, masque_binaire = cv2.threshold(image_gris, 200, 255, cv2.THRESH_BINARY)

            # Inverser le masque binaire
            masque_binaire = cv2.bitwise_not(masque_binaire)

            # Copier l'image
            image = image_ressource.copy()

            # Créer une copie floue de l'image
            flou = cv2.GaussianBlur(image, (0, 0), self.valeur_flou)

            # Créer une image vide pour la pollution lumineuse
            pollution = np.zeros_like(image)

            # Appliquer le masque binaire à l'image floue
            pollution = cv2.bitwise_and(flou, flou, mask=masque_binaire)

            # Soustraire la pollution lumineuse de l'image d'astrophotographie
            image_sans_pollution = cv2.subtract(image, pollution)

            # Enregistrer l'image sans pollution dans la liste d'images
            self.liste_image.append((nom_fichier_ressource, image_sans_pollution))

        # Creer une liste pour stocker les miniatures des images
        self.liste_image_miniature: list[tuple[str, np.ndarray]] = []
        
        # Taille de la miniature
        taille_miniature: tuple[int, int] = (400, 200)

        # Dictionnaire pour stocker les labels des images
        self.image_labels = {}


        # Transformer les images en miniature
        for image in self.liste_image:

            # Extraire le nom du fichier et l'image
            nom_fichier_ressource: str = image[0]
            image_sans_pollution: np.ndarray = image[1]

            # Convertir l'image de BGR à RGB
            image_sans_pollution: np.ndarray = cv2.cvtColor(image_sans_pollution, cv2.COLOR_BGR2RGB)

            # Créer une miniature de l'image
            image_miniature: np.ndarray = cv2.resize(image_sans_pollution, taille_miniature)

            # Ajouter la miniature à la liste
            self.liste_image_miniature.append((nom_fichier_ressource, image_miniature))

        # Ajouter un rectangle noir pour afficher les images dedans dans la zone sous l'en-tête
        self.rectangle_noir = QScrollArea()
        self.rectangle_noir.setObjectName("rectangle_noir")

        # Créer un widget pour contenir les miniatures
        sidebar_widget = QWidget()

        # Créer un layout pour organiser les miniatures
        sidebar_layout = QVBoxLayout()

        # Créer un layout horizontal initial pour afficher les miniatures
        layout_horizontal = QHBoxLayout()

        # Compteur pour compter le nombre d'images par ligne
        compteur: int = 0

        # Nombre d'images par ligne
        images_par_ligne: int = 3

        # Ajouter chaque image à la fenêtre, 3 par ligne
        for image in self.liste_image_miniature:

            # Extraire le nom du fichier et la miniature
            nom_fichier_ressource: str = image[0]
            image_miniature: np.ndarray = image[1]

            image_widget = QWidget()
            image_layout = QVBoxLayout(image_widget)

            # Créer un label pour afficher la miniature
            label = QLabel()

            # Convertir l'image en miniature en QPixmap et l'afficher dans le label
            miniature = QPixmap.fromImage(QImage(image_miniature.data, image_miniature.shape[1], image_miniature.shape[0], QImage.Format.Format_RGB888))
            label.setPixmap(miniature)

            # Ajouter le label au dictionnaire image_labels
            self.image_labels[label] = (image_miniature, nom_fichier_ressource)

            # Checkbox pour sélectionner l'image
            self.checkbox = QCheckBox()
            self.checkbox.setObjectName("checkbox")
            self.checkbox.setChecked(True)

            # Ajouter le label et la checkbox au layout
            image_layout.addWidget(label)
            image_layout.addWidget(self.checkbox)

            layout_horizontal.addWidget(image_widget)
            layout_horizontal.setObjectName("layout_horizontal")

            nom_image: str = image[0]

            # Chercher dans liste_image l'image correspondant à la miniature
            for image in self.liste_image:
                if image[0] == nom_image:
                    self.image_labels[label] = (image[1], nom_image, self.checkbox)

            # Quand on clique sur une miniature, afficher l'image en grand
            label.mousePressEvent: callable = lambda event, label=label: self.afficher_image_en_grand(self.image_labels[label])

            # Augmenter le compteur de 1
            compteur += 1

            # Ajouter une nouvelle ligne de miniatures tous les 3 widgets
            if compteur == images_par_ligne:
                compteur = 0
                sidebar_layout.addLayout(layout_horizontal)
                layout_horizontal = QHBoxLayout()

        # Si le compteur supérieur, ajoutez la dernière ligne d'images
        if compteur > 0:
            sidebar_layout.addLayout(layout_horizontal)

        # Ajouter le layout de la barre latérale au widget et l'ajouter au rectangle noir
        sidebar_widget.setLayout(sidebar_layout)
        self.rectangle_noir.setWidget(sidebar_widget)

        # Ajouter la zone de défilement à la zone sous l'en-tête
        self.layout_vertical_contenu.addWidget(self.rectangle_noir)

        # Créer un bouton pour enregistrer les images et l'ajouter à la zone sous l'en-tête
        self.bouton_enregistrer = QPushButton("Enregistrer les images")
        self.bouton_enregistrer.setObjectName("bouton_enregistrer")
        self.layout_vertical_contenu.addWidget(self.bouton_enregistrer)

        # Quand on clique sur le bouton "Enregistrer les images, exécuter la fonction enregistrer_images
        self.bouton_enregistrer.clicked.connect(self.enregistrer_images)


    def enregistrer_images(self) -> None:
        """
        Cette méthode permet d'enregistrer les images cochées dans un dossier spécifié par l'utilisateur

        Args:
        - None

        Returns:
        - None

        Comportement:
        - Demande à l'utilisateur de choisir le dossier de sortie
        - Créer le dossier de sortie s'il n'existe pas déjà
        - Enregistrer les images nettoyées dans le dossier de sortie
        """

        # Créer une liste pour stocker les images cochées
        images_coches = []

        # Parcourir le dictionnaire image_labels et ajouter les images cochées à la liste images_coches
        for label, (image, image_nom, checkbox) in self.image_labels.items():
            if checkbox.isChecked():
                images_coches.append((image_nom))

        # Créer une liste pour stocker les images à conserver
        image_conservees = [] 

        # Parcourir la liste des images et ne conserver que celles qui sont dans images_coches
        for image in self.liste_image:
            if image[0] in images_coches:
                image_conservees.append(image)
        
        # Remplacer la liste d'images par la liste d'images à conserver
        self.liste_image = image_conservees

        # On demande à l'utilisateur de choisir le dossier de sortie
        dossier_sortie: str = asksaveasfilename(defaultextension="", filetypes=[("Dossiers", "")], initialdir=self.chemin_dossier)

        # Créer le dossier de sortie s'il n'existe pas déjà
        if dossier_sortie and not os.path.exists(dossier_sortie):
            os.makedirs(dossier_sortie)
        else:
            print("Le chemin spécifié est invalide ou n'existe pas.")
            

        # Enregistrer les images nettoyées dans le dossier de sortie
        if dossier_sortie:
            for image in self.liste_image:
                # Récupérer le nom du fichier sans le chemin ni l'extension
                nom_fichier_ressource: str = image[0]

                # Récupérer l'image sans pollution
                image_sans_pollution: np.ndarray = image[1]            

                # Enregistrer l'image sans pollution en PNG
                cv2.imwrite(f"{dossier_sortie}/{nom_fichier_ressource}_nettoyee.png", image_sans_pollution)
        else:
            print("Aucun dossier de sortie sélectionné.")
        


app = QApplication(sys.argv)
mon_menu = MenuWindow(app)
mon_menu.show()
sys.exit(app.exec())