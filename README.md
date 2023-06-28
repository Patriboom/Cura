Voici une brève description des scripts disponibles

# Degrade
Permet de faire des dégradés de couleur avec une ou plusieurs buses en désignant les couches où sera appliqué le dégradé.

### Variables: 
- Couleur initiale (composée de trois filaments)
- Couleur finale (composée de trois filaments)
- Couche initiale
- Couche finale

### Exemple de code généré:
```
M163 S0 P0.00
M163 S1 P1.00
M163 S2 P0.00
```



# PauseEveryDelay
Met l'appareil en pause à fréquence déterminée (en minute), pendant un temps déterminé (en secondes).

### Variables: 
- Fréquence des pauses (en minutes)
- Durée des pauses (en secondes) ... une durée de 0 (zéro) seconde équivaut à une durée indéterminée, donc interrompue par l'action de l'usager
- Position de la buse durant les pauses (chacun des axes, X, Y et Z)
- Vitesse de déplacement de la buse en début et fin de pause
- Message affiché sur l'écran LCD durant les pauses

### Exemple de code généré:
```
;Pause demandée par PauseEveryDelay
G60
G90
;;Positionnement de la tête au lieu demandé
G0 E0 F20 X0 Y0 Z0
G92 E-1 F20  X0 Y0 Z0
;;Alerte sonore et mise en pause de la machine
M300 P5 S261
M300 P5 S329
M300 P5 S415
M300 P15 S523
M76
M25
G92 Z4
;FIN DE ----Pause demandée par PauseEveryDelay ----G4 S55
```



