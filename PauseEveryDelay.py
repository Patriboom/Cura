# Par Patrick ALLAIRE
# Version 1.1  ---   2023/06/14

# Description:  This plugin insets a pause every x minutes of printing
#               *** Assumptions ****
#               *** 1) Assumes "remaining time" is activated, at least on gcode's third line  as "M117 Time Left 4h36m12s"  ***
#               --- Example (1) of a propoer gcode's third line ---
#               M117 Time Left 4h36m12s
#               --- End of Example (1)  ---
#               *** End of assumptions ****

from ..Script import Script
# import re

class PauseEveryDelay(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name":"Pause à fréquence déterminée",
            "key": "PauseEveryDelay",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "val_Frequence":
                {
                    "label": "Fréquence des pauses (min.)",
                    "description": "Espace de temps (en minutes) entre les pauses.Minimum: 1; Maximum: 100",
                    "type": "int",
                    "default_value": 10,
                    "minimum_value": 1,
                    "maximum_value": 100
                 },
                "val_duree":
                {
                    "label": "Durée (sec.)",
                    "description": "Durée (en secondes) d`arrêt de l`impression (0 : aussi longtemps que vous ne redémarrerez pas l`impression)",
                    "type": "int",
                    "default_value": 55,
                    "minimum_value": 0,
                    "maximum_value": 300
                 },
                "val_posiX":
                {
                    "label": "Parquer la tête (X)",
                    "description": "Coordonnée X de la buse au moment d`amorcer la pause.",
                    "unit": "mm",
                    "type": "int",
                    "default_value": 0,
                    "minimum_value": 0,
                    "maximum_value": 220
                },
                "val_posiY":
                {
                    "label": "Parquer la tête (Y)",
                    "description": "Coordonnée Y de la buse au moment d`amorcer la pause.",
                    "unit": "mm",
                    "type": "int",
                    "default_value": 0,
                    "minimum_value": 0,
                    "maximum_value": 220
                },
                "val_posiZ":
                {
                    "label": "Parquer la tête (Z)",
                    "description": "Coordonnée Z de la buse au moment d`amorcer la pause.",
                    "unit": "mm",
                    "type": "int",
                    "default_value": 0,
                    "minimum_value": 0,
                    "maximum_value": 220
                },
                "val_vitesse":
                {
                    "label": "Vitesse",
                    "description": "Vitesse de déplacement vers le point de repos.",
                    "unit": "mm/s",
                    "type": "int",
                    "default_value": 20,
                    "minimum_value": 10,
                    "maximum_value": 100
                 },
                 "val_msg":
                 {
                    "label": "Message",
                    "description": "Message affiché sur l`écran ACL de votre imprimante durant la pause",
                    "type": "str",
                    "default_value": "Veuillez appuyer pour reprendre"
                 }
            }
        }"""

    def execute(self, data):
        # Récupération des valeurs de l'usager
        duree = self.getSettingValueByKey("val_duree")
        Freq = self.getSettingValueByKey("val_Frequence")
        msg = self.getSettingValueByKey("val_msg")
        posiX = str(self.getSettingValueByKey("val_posiX"))
        posiY = str(self.getSettingValueByKey("val_posiY"))
        posiZ = str(self.getSettingValueByKey("val_posiZ"))
        vitesse = str(self.getSettingValueByKey("val_vitesse"))

        # Définition des variables de travail
        line_set = {}
        rendu = 0
        last_z = 0
        nbLignes = 0
        tempsPrevu = ""

        # Calcul des valeurs de travail
        for layer in data:
            lines = layer.split("\n")
            for line in lines:
                if line.startswith("M117 Time Left ") and tempsPrevu == "":
                    tempsPrevu = line[15:]
                nbLignes = nbLignes + 1

        tempsPrevu = str(tempsPrevu)
        pointA = tempsPrevu.index("h", 0)
        pointB = tempsPrevu.index("m", 0)
        hres = tempsPrevu[:pointA]
        mins = tempsPrevu[(pointA+1):pointB]
        dureePrevue = int(hres) * 60 + int(mins)
        dureePrevue = int(hres) * 60 + int(mins)
        tempsTrav = dureePrevue / Freq
        lignesTra = round(nbLignes / round(tempsTrav))

        # Contenu à insérer aux fréquences définies
        contenuAjoutA = ";Pause demandée par PauseEveryDelay\n"
        contenuAjoutA += "G60\n"
        contenuAjoutA += "G90\n"
        contenuAjoutA += ";;Positionnement de la tête au lieu demandé"
        contenuAjoutB = ";;Alerte sonore et mise en pause de la machine\n"
        contenuAjoutB += "M300 P5 S261\n"
        contenuAjoutB += "M300 P5 S329\n"
        contenuAjoutB += "M300 P5 S415\n"
        contenuAjoutB += "M300 P15 S523\n"
        contenuAjoutB += "M76\n"
        contenuAjoutB += "M25\n"
        contenuAjoutB += "G92 Z" + str((last_z + 4)) + "\n"
        contenuAjoutB += ";FIN DE ----Pause demandée par PauseEveryDelay ----\n"
        if duree == 0:
            contenuAjoutB += "M0 " + msg + "\n"
        else:
            contenuAjoutB += "G4 S" + str(duree) + "\n"
        contenuAjoutB += "G61\n"

        # Travail du fichier et insértion des pauses
        for layer in data:
            layer_index = data.index(layer)
            lines = layer.split("\n")
            for line in lines:
                contenu = ""
                # Si la ligne a déjà été traitée, nous passons
                if line in line_set:
                    continue
                line_set[line] = True

                last_z = self.getValue(layer, "Z", posiZ)
                last_e = self.getValue(layer, "E", -1)

                if rendu >= lignesTra:
                    lines.insert(lines.index(line), contenuAjoutA)
                    contenu += "G0 E0 F" + vitesse + " X" + posiX + " Y" + posiY + " Z" + str(last_z) + "\n"
                    contenu += "G92 E" + str(last_e) + " F" + vitesse + "  X" + posiX + " Y" + posiY + " Z" + posiZ
                    lines.insert(lines.index(line), contenu)
                    lines.insert(lines.index(line), contenuAjoutB)
                    rendu = 0
                rendu = rendu + 1
            data[layer_index] = "\n".join(lines)

        return data

