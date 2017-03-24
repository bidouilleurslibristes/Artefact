Ce fichier est dédié à la description des énigmes unitaires et composites présentes dans le jeu final  

  
Détail général : Chaque bandeau est composé de 32 leds. On considérera les leds par groupe de 4 pour les énigmes, ce qui laissera la possibilité d'avoir 8 sections indépendantes sur le bandeau

Couleurs :
r : rouge
l : bleu
v : vert
j : jaune
t : turquoise
o : orange
b : blanc
m : mauve
n : noir


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
little 5 xx..xx.x xxxx...x  
Explication : Énigme petits boutons. Les parties 1,2,5,6,8 du bandeau 5 sont allumées en bleu (les premiers x). Les boutons n°5 des panneaux 1,2,3,4,8 sont allumés en bleu. Les autres NE doivent PAS être allumés en bleu.





# Séquence de couleurs

## Description  

Visuel : Un morceau de bandeau est divisé en sections de 2 leds de mêmes couleurs.
Résolution : Aller sur la console correspondant au bandeau puis appuyer sur les boutons correspondant aux couleurs en allant du haut vers le bas.

## Fichier config

sequence 3 brrjtn.....  
Explication : Séquence de couleurs sur le bandeau 3. Les couleurs vont toujours par deux. Ici on a donc deux leds bleus puis quatre leds rouges, deux jaunes, deux turquoises et deux noirs.




# Masques de bandeau

## Description

Visuel : Un bandeau est éteint complétement. Le bouton swag correspondant clignote
Résolution : Appuyer sur le bouton permet d'afficher le vrai contenu du bandeau.

## Fichier config

mask 4  
Explication : Éteint le bandeau 4 a moins de maintenir le bouton swag




# Allumage de boutons

## Description

Visuel : La liste des boutons d'un panneau est allumée
Résolution : Résolu

## Fichier config

buttons 1 bb.tv...rT
Explication : Allume sur le panneau 1 le bouton swag et les boutons 1,2,4,5,8 dans les couleurs correspondant aux initiales.


