#-------------------------------- Importations neccessaire --------------------------------#
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox, QScrollArea, QDockWidget, QSlider, QMainWindow
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtCore import QSize


#-------------------------------- Classe ModificationsImageWindow --------------------------------#
class ModificationsImageWindow(QMainWindow):
    """
    Classe pour la fenêtre de modifications d'image

    Méthodes:
    - __init__(self, image_info: tuple[np.ndarray, str]): Constructeur de la classe
    - zoom(self, event): Cette méthode permet de gérer le zoom dans la vue graphique
    - afficher_image(self): Cette méthode permet d'afficher l'image originale dans la vue graphique
    - convertir_et_afficher_image(self, copie_image: np.ndarray): Cette méthode permet de convertir l'image et de l'afficher dans le QGraphicsView
    - appliquer_effets_cumules(self): Cette méthode permet d'appliquer les effets cumulés sur l'image
    - appliquer_modifications(self): Cette méthode permet d'appliquer les modifications sur l'image
    - appliquer_luminosite(self, img: np.ndarray, valeur_luminosite: int): Cette méthode permet d'appliquer l'ajustement de luminosité sur l'image
    - appliquer_contraste(self, img: np.ndarray, valeur_contraste: int): Cette méthode permet d'appliquer l'ajustement de contraste sur l'image
    - appliquer_saturation(self, img: np.ndarray, valeur_saturation: int): Cette méthode permet d'appliquer l'ajustement de saturation sur l'image
    - appliquer_nettete(self, img: np.ndarray, valeur_nettete: int): Cette méthode permet d'appliquer l'ajustement de netteté sur l'image
    - appliquer_chaleur(self, valeur_chaleur: int, img: np.ndarray): Cette méthode permet d'appliquer l'ajustement de chaleur sur l'image
    - appliquer_flou(self, img: np.ndarray, valeur_flou: int): Cette méthode permet d'appliquer l'ajustement de flou sur l'image
    """
    
    def __init__(self, image_info: tuple[np.ndarray, str]):
        super().__init__()
        
        self.setWindowTitle("Modifications image")

        self.image_originale: np.ndarray = image_info[0]
        self.image_originale_nom: str = image_info[1]

        # cree une copie de l'image
        self.copie_image: np.ndarray = self.image_originale.copy()

        # Creation d"un QLabel pour afficher l'image
        self.label_image = QLabel()
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Créer une QDockWidget pour les outils
        self.dock_widget = QDockWidget("Ajustements", self)
        
        self.dock_widget.setStyleSheet("color: white; background-color: black;")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_widget)

        # faire en sorte que le QDockWidget ne puisse etre deplace que sur les cotes
        self.dock_widget.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)

        # Modifier la largeur du QDockWidget
        self.dock_widget.setMinimumWidth(200)
        self.dock_widget.setMaximumWidth(400)

        outilsLayout = QVBoxLayout()

        #-------------------------------------------------Luminosite-------------------------------------------------#
        self.BoxLuminosite = QVBoxLayout()

        self.labelLuminosite = QLabel("Luminosite")
        self.labelLuminosite.setStyleSheet("color: white;")

        self.slider_luminosite = QSlider(Qt.Orientation.Horizontal, self)
                
        self.slider_luminosite.setMinimum(-100)
        self.slider_luminosite.setMaximum(100)
        self.slider_luminosite.setValue(0)
        self.slider_luminosite.valueChanged.connect(self.appliquer_effets_cumules)
                
        self.BoxLuminosite.addWidget(self.labelLuminosite)
        self.BoxLuminosite.addWidget(self.slider_luminosite)

        self.BoxLuminosite.addStretch(1)

        widgetLuminosite = QWidget()
        widgetLuminosite.setLayout(self.BoxLuminosite)
        outilsLayout.addWidget(widgetLuminosite)

        #-------------------------------------------------Contraste-------------------------------------------------#

        self.BoxContraste = QVBoxLayout()

        self.labelContraste = QLabel("Contraste")
        self.labelContraste.setStyleSheet("color: white;")

        self.slider_contraste = QSlider(Qt.Orientation.Horizontal, self)
                
        self.slider_contraste.setMinimum(-100)
        self.slider_contraste.setMaximum(100)
        self.slider_contraste.setValue(0)
        self.slider_contraste.valueChanged.connect(self.appliquer_effets_cumules)

        self.BoxContraste.addWidget(self.labelContraste)
        self.BoxContraste.addWidget(self.slider_contraste)

        self.BoxContraste.addStretch(1)

        widgetContraste = QWidget()
        widgetContraste.setLayout(self.BoxContraste)
        outilsLayout.addWidget(widgetContraste)

        #-------------------------------------------------Saturation-------------------------------------------------#

        self.BoxSaturation = QVBoxLayout()

        self.labelSaturation = QLabel("Saturation")
        self.labelSaturation.setStyleSheet("color: white;")

        self.slider_saturation = QSlider(Qt.Orientation.Horizontal, self)
                
        self.slider_saturation.setMinimum(-100)
        self.slider_saturation.setMaximum(100)
        self.slider_saturation.setValue(0)
        self.slider_saturation.valueChanged.connect(self.appliquer_effets_cumules)

        self.BoxSaturation.addWidget(self.labelSaturation)
        self.BoxSaturation.addWidget(self.slider_saturation)

        self.BoxSaturation.addStretch(1)

        widgetSaturation = QWidget()
        widgetSaturation.setLayout(self.BoxSaturation)
        outilsLayout.addWidget(widgetSaturation)


        #-------------------------------------------------Nettete-------------------------------------------------#

        self.BoxNettete = QVBoxLayout()

        self.labelNettete = QLabel("Nettete")
        self.labelNettete.setStyleSheet("color: white;")
        
        self.slider_nettete = QSlider(Qt.Orientation.Horizontal, self)
                
        self.slider_nettete.setMinimum(0)
        self.slider_nettete.setMaximum(200)
        self.slider_nettete.setValue(0)
        self.slider_nettete.valueChanged.connect(self.appliquer_effets_cumules)

        self.BoxNettete.addWidget(self.labelNettete)
        self.BoxNettete.addWidget(self.slider_nettete)

        self.BoxNettete.addStretch(1)

        widgetNettete = QWidget()
        widgetNettete.setLayout(self.BoxNettete)
        outilsLayout.addWidget(widgetNettete)

        
        #-------------------------------------------------Chaleur d'image-------------------------------------------------#

        self.BoxChaleur = QVBoxLayout()

        self.labelChaleur = QLabel("Chaleur")
        self.labelChaleur.setStyleSheet("color: white;")
        
        self.slider_chaleur = QSlider(Qt.Orientation.Horizontal, self)
                
        self.slider_chaleur.setMinimum(-40)
        self.slider_chaleur.setMaximum(40)
        self.slider_chaleur.setValue(0)
        self.slider_chaleur.valueChanged.connect(self.appliquer_effets_cumules)

        self.BoxChaleur.addWidget(self.labelChaleur)
        self.BoxChaleur.addWidget(self.slider_chaleur)

        self.BoxChaleur.addStretch(1)

        widgetChaleur = QWidget()
        widgetChaleur.setLayout(self.BoxChaleur)
        outilsLayout.addWidget(widgetChaleur)

        #-------------------------------------------------Flou-------------------------------------------------#


        self.BoxFlou = QVBoxLayout()

        self.labelFlou = QLabel("Flou")
        self.labelFlou.setStyleSheet("color: white;")
        
        self.slider_flou = QSlider(Qt.Orientation.Horizontal, self)
                
        self.slider_flou.setMinimum(0)
        self.slider_flou.setMaximum(20)
        self.slider_flou.setValue(0)
        self.slider_flou.valueChanged.connect(self.appliquer_effets_cumules)

        self.BoxFlou.addWidget(self.labelFlou)
        self.BoxFlou.addWidget(self.slider_flou)

        self.BoxFlou.addStretch(1)

        widgetFlou = QWidget()
        widgetFlou.setLayout(self.BoxFlou)
        outilsLayout.addWidget(widgetFlou)

        #-------------------------------------------------Reset-------------------------------------------------#
        
        self.bouton_reset = QPushButton("Reset")
        self.bouton_reset.setObjectName("bouton_reset")
    
        self.bouton_reset.clicked.connect(self.afficher_image)
        
        self.bouton_reset.clicked.connect(lambda: self.slider_luminosite.setValue(0))
        self.bouton_reset.clicked.connect(lambda: self.slider_contraste.setValue(0))
        self.bouton_reset.clicked.connect(lambda: self.slider_saturation.setValue(0))
        self.bouton_reset.clicked.connect(lambda: self.slider_nettete.setValue(0))
        self.bouton_reset.clicked.connect(lambda: self.slider_chaleur.setValue(0))
        self.bouton_reset.clicked.connect(lambda: self.slider_flou.setValue(0))
        
        outilsLayout.addWidget(self.bouton_reset)

        #-------------------------------------------------Appliquer les modifications-------------------------------------------------#

        self.BoxAppliquer = QVBoxLayout()
        self.bouton_appliquer = QPushButton("Appliquer")
        self.bouton_appliquer.clicked.connect(self.appliquer_modifications)
        self.BoxAppliquer.addWidget(self.bouton_appliquer)
        self.BoxAppliquer.addStretch(1)
        widgetAppliquer = QWidget()
        widgetAppliquer.setLayout(self.BoxAppliquer)
        outilsLayout.addWidget(widgetAppliquer)

        outilsWidget = QWidget()
        outilsWidget.setLayout(outilsLayout)
        self.dock_widget.setWidget(outilsWidget)


        #-------------------------------------------------Afficher l'image-------------------------------------------------#

        # Initialiser le niveau de zoom, le zoom minimum et le zoom maximum
        self.zoom_level: float = 1
        self.min_zoom: float = 0.1
        self.max_zoom: float = 10

        # Creation d'un QGraphicsView pour afficher l'image dans une zone de défilement
        self.graphics_view = QGraphicsView()
        self.graphics_scene = QGraphicsScene()
        self.graphics_view.setScene(self.graphics_scene)
        self.graphics_view.wheelEvent = self.zoom

        self.setCentralWidget(self.graphics_view)

        # Afficher l'image initiale
        self.afficher_image()

    def zoom(self, event) -> None:
        """
        Cette méthode permet de gérer le zoom dans la vue graphique.

        Parameters :
        - event : l'action de la molette de la souris.

        Returns :
        - None

        Comportement :
        - Définit le facteur de zoom et de dézoom.
        - Calcule le nouveau niveau de zoom en fonction de la direction de la molette de la souris.
        - Si le nouveau niveau de zoom est compris entre le zoom minimum et le zoom maximum, applique le zoom ou le dézoom sur la vue graphique.
        """

        # Définir le facteur de zoom et de dézoom
        facteur_zoom: float = 1.25
        facteur_dezoom: float = 1 / facteur_zoom

        # Calculer le nouveau zoom
        if event.angleDelta().y() > 0:  
            nouveau_zoom: float = self.zoom_level * facteur_zoom 
        else: 
            nouveau_zoom: float = self.zoom_level * facteur_dezoom 

        # Si le nouveau zoom est compris entre le zoom minimum et le zoom maximum, appliquer le zoom
        if self.min_zoom <= nouveau_zoom <= self.max_zoom:
            facteur_taille: float = facteur_zoom if nouveau_zoom > self.zoom_level else facteur_dezoom
            self.graphics_view.scale(facteur_taille, facteur_taille)            
            self.zoom_level = nouveau_zoom


    def afficher_image(self):
        """
        Cette méthode permet d'afficher l'image originale dans la vue graphique.
        
        Parameters :
        - None
        
        Returns :
        - None
        
        Comportement :
        - Convertit l'image originale en pixmap.
        - Redimensionne le QLabel pour qu'il corresponde à la taille de l'image.
        - Affiche l'image dans le QGraphicsView.
        """

        # Charger l'image
        image = cv2.cvtColor(self.image_originale, cv2.COLOR_BGR2RGB)

        # Redimensionner l'image pour qu'elle ne dépasse pas une certaine taille
        max_width = 1600 
        max_height = 900
        facteur_taille = min(max_width / image.shape[1], max_height / image.shape[0])


        resized_image = cv2.resize(image, (0, 0), fx=facteur_taille, fy=facteur_taille)

        # Convertir l'image redimensionnée en pixmap
        height, width, channel = resized_image.shape
        bytes_per_line = 3 * width
        qimage = QImage(resized_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        qpixmap = QPixmap.fromImage(qimage)

        # Redimensionner le QLabel pour qu'il corresponde à la taille de l'image
        self.label_image.setFixedSize(QSize(max_width, max_height))

        # Afficher l'image redimensionnée dans le QGraphicsView
        self.graphics_scene.clear()
        self.graphics_scene.addPixmap(qpixmap)



    def convertir_et_afficher_image(self, copie_image: np.ndarray) -> None:
        """
        Cette méthode permet de convertir l'image et de l'afficher dans le QGraphicsView.
        
        Parameters :
        - copie_image : l'image à convertir et à afficher.
        
        Returns :
        - None
        
        Comportement :
        - Convertit l'image de BGR à RGB.
        - Redimensionne l'image pour qu'elle ne dépasse pas une certaine taille.
        - Convertit l'image redimensionnée en pixmap.
        - Redimensionne le QLabel pour qu'il corresponde à la taille de l'image.
        - Affiche l'image redimensionnée dans le QGraphicsView.
        """

        # Convertir l'image de BGR à RGB
        copie_image = cv2.cvtColor(copie_image, cv2.COLOR_BGR2RGB)

        # Redimensionner l'image pour qu'elle ne dépasse pas une certaine taille
        max_width: int = 1600 
        max_height: int = 900 
        facteur_taille: float = min(max_width / copie_image.shape[1], max_height / copie_image.shape[0])

        resized_image: np.ndarray  = cv2.resize(copie_image, (0, 0), fx=facteur_taille, fy=facteur_taille)

        # Convertir l'image redimensionnée en pixmap
        height, width, channel = resized_image.shape
        bytes_per_line: int = 3 * width
        qimage: QImage = QImage(resized_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        qpixmap: QPixmap = QPixmap.fromImage(qimage)

        # Redimensionner le QLabel pour qu'il corresponde à la taille de l'image
        self.label_image.setFixedSize(QSize(max_width, max_height))

        # Afficher l'image redimensionnée dans le QGraphicsView
        self.graphics_scene.clear()
        self.graphics_scene.addPixmap(qpixmap)
        

    
    def appliquer_effets_cumules(self) -> None:
        """
        Cette méthode permet d'appliquer les effets cumulés sur l'image.
        
        Parameters :
        - None
        
        Returns :
        - None
        
        Comportement :
        - Récupère les valeurs des curseurs pour chaque effet.
        - Copie l'image originale.
        - Applique les effets individuellement.
        """

        # Récupérer les valeurs des curseurs pour chaque effet
        valeur_luminosite: int = self.slider_luminosite.value()
        valeur_contraste: int = self.slider_contraste.value()
        valeur_saturation: int = self.slider_saturation.value()
        valeur_netete: int = self.slider_nettete.value()
        valeur_chaleur: int = self.slider_chaleur.value()
        valeur_flou: int = self.slider_flou.value()

        # Copier l'image originale
        img: np.ndarray = self.image_originale.copy()
        
        # Appliquer les effets individuellement
        img = self.appliquer_luminosite(img, valeur_luminosite)
        img = self.appliquer_contraste(img, valeur_contraste)
        img = self.appliquer_saturation(img, valeur_saturation)
        img = self.appliquer_nettete(img, valeur_netete)
        img = self.appliquer_chaleur(valeur_chaleur, img)
        img = self.appliquer_flou(img, valeur_flou)

    def appliquer_modifications(self) -> None:
        """
        Cette méthode permet d'appliquer les modifications sur l'image.
        
        Parameters :
        - None
        
        Returns :
        - None
        
        Comportement :
        - Récupère les valeurs des curseurs pour chaque effet.
        - Applique les effets individuellement sur une copie de l'image originale.
        - Met à jour l'image originale avec l'image modifiée.
        - Remplace l'image originale par l'image modifiée dans la liste d'images.
        - Remplace l'image originale par l'image modifiée dans la liste d'images miniatures.
        - Recrée le dictionnaire pour stocker les labels des images.
        - Recrée tout les widgets pour afficher les miniatures.
        """

        # Importation de MenuWindow
        from MenuWindow import mon_menu

        # Récupération des valeurs des curseurs pour chaque effet
        valeur_luminosite: int = self.slider_luminosite.value()
        valeur_contraste: int = self.slider_contraste.value()
        valeur_saturation: int = self.slider_saturation.value()
        valeur_netete: int = self.slider_nettete.value()
        valeur_chaleur: int = self.slider_chaleur.value()
        valeur_flou: int = self.slider_flou.value()

        # Copier l'image originale
        img = self.image_originale.copy()

        # Appliquer les effets individuels
        img = self.appliquer_luminosite(img, valeur_luminosite)
        img = self.appliquer_contraste(img, valeur_contraste)
        img = self.appliquer_saturation(img, valeur_saturation)
        img = self.appliquer_nettete(img, valeur_netete)
        img = self.appliquer_chaleur(valeur_chaleur, img)
        img = self.appliquer_flou(img, valeur_flou)

        # Remplacer l'image originale par l'image modifiée
        self.image_originale = img

        # Remplacer l'image originale par l'image modifiée dans la liste d'images
        for i, image in enumerate(mon_menu.liste_image):
            if image[0] == self.image_originale_nom:
                mon_menu.liste_image[i] = (self.image_originale_nom, self.image_originale)

        # Remplacer l'image originale par l'image modifiée dans la liste d'images miniatures
        for i, image_miniature in enumerate(mon_menu.liste_image_miniature):
            if image_miniature[0] == self.image_originale_nom:
                image_rgb = cv2.cvtColor(self.image_originale, cv2.COLOR_BGR2RGB)
                mon_menu.liste_image_miniature[i] = (self.image_originale_nom, cv2.resize(image_rgb, (400, 200)))

        # Supprimer tout le rectangle noir et le bouton enregistrer
        mon_menu.supprimer_element(mon_menu.rectangle_noir)
        mon_menu.supprimer_element(mon_menu.bouton_enregistrer)

         # Recréer le Dictionnaire pour stocker les labels des images
        mon_menu.image_labels = {}

        # Créer un nouveau rectangle noir
        mon_menu.rectangle_noir = QScrollArea()
        mon_menu.rectangle_noir.setObjectName("rectangle_noir")

        # Créer un widget pour contenir les miniatures
        sidebar_widget = QWidget()

        # Créer un layout pour organiser les miniatures
        sidebar_layout = QVBoxLayout()

        # Créer un layout horizontal initial pour afficher les miniatures
        layout_horizontal = QHBoxLayout()

        compteur: int = 0
        images_par_ligne: int = 3

        # Ajouter chaque image à la fenêtre, 3 par ligne
        for image in mon_menu.liste_image_miniature:
            image_miniature: np.ndarray = image[1]

            # Créer un widget pour contenir l'image
            image_widget = QWidget()
            image_layout = QVBoxLayout(image_widget)

            # Créer un label pour afficher l'image
            label = QLabel()
            miniature = QPixmap.fromImage(QImage(image_miniature.data, image_miniature.shape[1], image_miniature.shape[0], QImage.Format.Format_RGB888))
            label.setPixmap(miniature)

            # Checkbox pour sélectionner l'image
            checkbox = QCheckBox()
            checkbox.setObjectName("checkbox")
            checkbox.setChecked(True)

            # Ajouter le label et la checkbox au layout
            image_layout.addWidget(label)
            image_layout.addWidget(checkbox)

            # Ajouter le layout au widget
            layout_horizontal.addWidget(image_widget)
            layout_horizontal.setObjectName("layout_horizontal")

            # Récupérer le nom de l'image
            nom_image: str = image[0]
            
            # Chercher dans liste_image l'image correspondant à la miniature
            for image in mon_menu.liste_image:
                if image[0] == nom_image:
                    mon_menu.image_labels[label] = (image[1], nom_image, checkbox)

            # Quand on clique sur une miniature, afficher l'image en grand
            label.mousePressEvent = lambda event, label=label: mon_menu.afficher_image_en_grand(mon_menu.image_labels[label])

            # Augmenter le compteur de 1
            compteur += 1

            # Ajouter une nouvelle ligne de miniatures tous les 3 widgets
            if compteur == images_par_ligne:
                compteur = 0
                sidebar_layout.addLayout(layout_horizontal)
                layout_horizontal = QHBoxLayout()

        # Si le compteur est différent de zéro, ajoutez la dernière ligne d'images
        if compteur > 0:
            sidebar_layout.addLayout(layout_horizontal)

        sidebar_widget.setLayout(sidebar_layout)
        mon_menu.rectangle_noir.setWidget(sidebar_widget)
        mon_menu.layout_vertical_contenu.addWidget(mon_menu.rectangle_noir)

        # Créer un bouton pour enregistrer les images
        mon_menu.bouton_enregistrer = QPushButton("Enregistrer les images")
        mon_menu.bouton_enregistrer.setObjectName("bouton_enregistrer")
        mon_menu.layout_vertical_contenu.addWidget(mon_menu.bouton_enregistrer)

        # Quand on clique sur le bouton "Enregistrer les images" exécuter la fonction enregistrer_images
        mon_menu.bouton_enregistrer.clicked.connect(mon_menu.enregistrer_images)

        # Fermer la fenêtre de modifications d'image
        self.close()
        

    def appliquer_luminosite(self, img: np.ndarray, valeur_luminosite: int) -> np.ndarray:
        """
        Cette méthode permet d'appliquer l'ajustement de luminosité sur l'image.

        Args :
        - img : l'image à modifier.
        - valeur_luminosite : la valeur de luminosité à appliquer.

        Returns :
        - img : l'image modifiée.

        Comportement :
        - Calcule les valeurs alpha et gamma pour ajuster la luminosité.
        - Applique l'effet de luminosité à l'image.
        - Convertit l'image et l'affiche.
        """

        # highlight: valeur la plus élevée dans l'image 
        highlight: int = 255

        # Calculer les valeurs alpha et gamma pour ajuster la luminosité
        if valeur_luminosite > 0:
            ombre: int = valeur_luminosite
        else:
            ombre: int = 0
            highlight: int = 255 + valeur_luminosite
        alpha_b: float = (highlight - ombre) / 255
        gamma_b: int = ombre

        # Appliquer l'ajustement de luminosité à l'image
        img = cv2.convertScaleAbs(img, alpha=alpha_b, beta=gamma_b)

        # Convertir l'image et l'afficher
        self.convertir_et_afficher_image(img)

        return img


    def appliquer_contraste(self, img: np.ndarray, valeur_contraste: int) -> np.ndarray:
        """
        Cette méthode permet d'appliquer l'ajustement de contraste sur l'image.

        Args :
        - img : l'image à modifier.
        - valeur_contraste : la valeur de contraste à appliquer.

        Returns :
        - img : l'image modifiée.

        Comportement :
        - Convertit l'image en image PIL.
        - Augmente le contraste à l'aide de la méthode enhance de la bibliothèque PIL.
        - Convertit l'image PIL en numpy array.
        - Convertit l'image et l'affiche.
        """

        # Convertir le numpy array en image PIL
        img_pil = Image.fromarray(img)
        enhancer = ImageEnhance.Contrast(img_pil)

        # Augmenter le contraste
        facteur: float = 1 + valeur_contraste / 100

        # Convertir l'image PIL en numpy array et appliquer le contraste
        img: np.ndarray = np.array(enhancer.enhance(facteur))

        # Convertir l'image et l'afficher
        self.convertir_et_afficher_image(img)

        return img
    
    def appliquer_saturation(self, img: np.ndarray, valeur_saturation: int) -> np.ndarray:
        """
        Cette méthode permet d'appliquer l'ajustement de saturation sur l'image.

        Args :
        - img : l'image à modifier.
        - valeur_saturation : la valeur de saturation à appliquer.

        Returns :
        - img : l'image modifiée.

        Comportement :
        - Convertit l'image de BGR à HSV.
        - Ajuste la saturation.
        - Convertit l'image de HSV à BGR.
        - Convertit l'image et l'affiche.
        """

        # Convertir l'image de BGR à HSV
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Ajuster la saturation
        img[:, :, 1] = np.clip(img[:, :, 1] * (1 + valeur_saturation / 100), 0, 255)

        # Convertir l'image de HSV à BGR
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)

        # Convertir l'image et l'afficher
        self.convertir_et_afficher_image(img)

        return img


    def appliquer_nettete(self, img: np.ndarray, valeur_nettete: int) -> np.ndarray:
        """
        Cette méthode permet d'appliquer l'ajustement de netteté sur l'image.

        Args :
        - img : l'image à modifier.
        - valeur_nettete : la valeur de netteté à appliquer.

        Returns :
        - img : l'image modifiée.

        Comportement :
        - Convertit l'image en image PIL.
        - Augmente la netteté à l'aide de la méthode enhance de la bibliothèque PIL.
        - Convertit l'image PIL en numpy array.
        - Convertit l'image et l'affiche.
        """

        # Convertir le numpy array en image PIL
        img_pil = Image.fromarray(img)

        # Appliquer un filtre de netteté
        enhancer = ImageEnhance.Sharpness(img_pil)

        # Augmenter la netteté
        facteur: float = 1 + valeur_nettete / 100
        img = enhancer.enhance(facteur)

        # Convertir l'image PIL en numpy array
        img: np.ndarray = np.array(img)

        # Convertir l'image et l'afficher
        self.convertir_et_afficher_image(img)

        return img


    def appliquer_chaleur(self, valeur_chaleur: int, img: np.ndarray) -> np.ndarray:
        """
        Cette méthode permet d'appliquer l'ajustement de chaleur sur l'image.
        
        Args :
        - valeur_chaleur : la valeur de chaleur à appliquer.
        - img : l'image à modifier.
        
        Returns :
        - img : l'image modifiée.
        
        Comportement :
        - Convertit l'image en image PIL.
        - Augmente la valeur de la couleur rouge et diminue la valeur de la couleur bleue.
        - Convertit l'image et l'affiche.
        """

        # Convertir le numpy array en image PIL
        img_pil = Image.fromarray(img)

        # Convertir l'image en mode RGB
        r, g, b = img_pil.split()

        # Augmenter la valeur de la couleur rouge et diminuer la valeur de la couleur bleue
        r = r.point(lambda i: i - valeur_chaleur)
        b = b.point(lambda i: i + valeur_chaleur)

        # Fusionner les canaux RGB
        img = Image.merge('RGB', (r, g, b))

        # Convertir l'image PIL en numpy array
        img: np.ndarray = np.array(img)

        # Convertir l'image et l'afficher
        self.convertir_et_afficher_image(img)

        return img



    def appliquer_flou(self, img: np.ndarray, valeur_flou: int) -> np.ndarray:
        """
        Cette méthode permet d'appliquer l'ajustement de flou sur l'image.
        
        Args :
        - img : l'image à modifier.
        - valeur_flou : la valeur de flou à appliquer.
        
        Returns :
        - img : l'image modifiée.
        
        Comportement :
        - Convertir l'image en image PIL.
        - Appliquer un flou à l'aide de la méthode filter de la bibliothèque PIL.
        - Convertir l'image PIL en numpy array.
        - Convertir l'image et l'afficher.
        """

        # Convertir le numpy array en image PIL
        img_pil = Image.fromarray(img)

        # Appliquer un flou
        img = img_pil.filter(ImageFilter.GaussianBlur(radius=valeur_flou))

        # Convertir l'image PIL en numpy array
        img: np.ndarray = np.array(img)

        # Convertir l'image et l'afficher
        self.convertir_et_afficher_image(img)

        return img
