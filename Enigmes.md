Ce fichier est dédié à la description des énigmes unitaires et composites présentes dans le jeu final  

  
Détail général : Chaque bandeau est composé de 32 leds. On considérera les leds par groupe de 4 pour les énigmes, ce qui laissera la possibilité d'avoir 8 sections indépendantes sur le bandeau


# Enigme bouton SWAG

## Description  

Visuel : Un bandeau de led complétement ou partiellement coloré en rouge.  
Résolution : Appuyer sur le bouton swag correspondant au bandeau.  

## Fichier config

Exemple :  
swag 3 xxx..x..  
Explication : Énigme swag sur le bandeau 3. Les parties 1,2,3,6 du bandeau sont allumées en rouge (les x de la gauche vers la droite).




# Enigme petits boutons

## Description

Visuel : Un bandeau est composé de x/8 (1<=x<=8) de leds de couleur bleu.
Résolution : Appuyer sur les petits boutons colorés en rouge et correpondants au bon bandeau.

## Fichier config

Exemple :  
buttons 5 xx..xx.x xxxx...x  
Explication : Énigme petits boutons. Les parties 1,2,5,6,8 du bandeau 5 sont allumées en bleu (les premiers x). Les boutons n°5 des panneaux 1,2,3,4,8 sont allumés en bleu. Les autres NE doivent PAS être allumés en bleu.





# Séquence de couleurs

Visuel : Un morceau de bandeau est divisé en sections de 2 leds de mêmes couleurs.
Résolution : Aller sur la console correspondant au bandeau puis appuyer sur les boutons correspondant aux couleurs en allant du haut vers le bas.

# Masques de bandeau

Visuel : Un bandeau est éteint complétement. Le bouton swag correspondant clignote
Résolution : Appuyer sur le bouton permet d'afficher.
