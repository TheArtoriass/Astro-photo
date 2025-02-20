# ASTRO-PHOTO

## Sommaire 
1. [Objectif de la SAE](#objectif-de-la-sae) 
2. [Réalisation](#Réalisation) 
3. [Utilisation de l'interface Python](#utilisation-de-linterface-python) 

	
## Objectif de la SAE

*Développer une application capable de traiter les images astronomiques en éliminant la pollution lumineuse.*

# Réalisation

Le dossier **App** qui contient l'ensemble des programmes pour faire fonctionner l'interface principale  **App**
>Permet de traiter les images astronomiques et d’en soustraire la pollution lumineuse.
Avec une méthode de détection de gradient, on peut modifier la valeur du flou dans paramètre puis on peut sélectionner une image ou un lot d’images qu'on souhaite pour cliquer dessus pour modifier certains éléments (saturation,contraste,flou...) de la photo l'enregistrer ou retourner au menu pour recommencer.


# Utilisation de l'interface Python  
### Prérequis :
Assurez-vous d'avoir Python et les bibliothèques Python nécessaires installéss sur votre ordinateur.

```bash
pip install PyQt6
pip install opencv-python
pip install numpy
pip install pillow
pip install tk
```


### Téléchargement du ZIP :
- Téléchargez le ZIP.

### Extraction des Fichiers :
- Extrayez le contenu de l'archive dans un dossier de votre choix.

### Exécution du Programme:

- Ouvrez un **Terminal ou un Invite de commandes**.
- Naviguez jusqu'au dossier App²
- Exécutez le Programme en utilisant la commande suivante : 
`python App.py`

### OU

### Exécution depuis un IDE :
- Rendez-vous sur votre IDE.
- Ouvrez le dossier du projet.
- Accédez au programme `App.py`.
- Exécutez le programme à l'aide de la flèche en haut à droite.

### Après l'exécution de la fenêtre  :
- Cliquez sur Paramètre pour changer le flou de suppression de pollution au besoin. Nous vous conseillons un flou entre 50 et 300 avec 300 représentant un meilleur rendu, mais plus long (ATTENTION: Au-delà de 300, cela devient très long).
- Cliquez sur le "Ajouter des images" pour sélectionner une ou plusieurs images de votre choix.
- Cliquez sur les images pour les afficher en grand dans une fenetre de modification avec la possibilité de changer la luminosité, la chaleur, le flou... de l'image.
- Appliquez les modifications en appuyant sur "Appliquer" ou appuyez sur Reset pour remettre l'image par défaut.
- Quittez la fenêtre de modification d'image, et cochez ou non les checkboxs en dessous des miniatures pour conserver les images correspondantes.
- Appuyez sur "Enregistrer les Images" pour enregistrer les images dans un dossier, ou sur "Retour menu" pour revenir au menu principal
