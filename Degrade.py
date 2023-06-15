# Par Patrick ALLAIRE
# Version 1.1  ---   2023/06/14

from ..Script import Script
import re

class Degrade(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name":"Dégradé de couleurs",
            "key": "Degrade",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "debut":
                {
                    "label": "Première couche du dégradé",
                    "description": "Première couche du degradé (cette couche sera entièrement de la couleur initiale).",
                    "type": "int",
                    "default_value": 0,
                    "minimum_value": 0
                 },
                "inita":
                {
                    "label": "Buse 1",
                    "description": "Pourcentage (%) de la couleur 1 dans le mélange initial --- assurez-vous de totaliser 100% avec vos trois couleurs",
                    "type": "int",
                    "default_value": 100,
                    "minimum_value": 0,
                    "maximum_value": 100
                 },
                "initb":
                {
                    "label": "Buse 2",
                    "description": "Pourcentage (%) de la couleur 2 dans le mélange initial --- assurez-vous de totaliser 100% avec vos trois couleurs",
                    "type": "int",
                    "default_value": 0,
                    "minimum_value": 0,
                    "maximum_value": 100
                 },
                "initc":
                {
                    "label": "Buse 3",
                    "description": "Pourcentage (%) de la couleur 3 dans le mélange initial --- assurez-vous de totaliser 100% avec vos trois couleurs",
                    "type": "int",
                    "default_value": 0,
                    "minimum_value": 0,
                    "maximum_value": 100
                 },
                "fin":
                {
                    "label": "Dernière couche du processus",
                    "description": "Dernière couche du degradé (cette couche sera entièrement de la couleur finale).",
                    "type": "int",
                    "default_value": 10,
                    "minimum_value": 2
                },
                "fina":
                {
                    "label": "Buse 1",
                    "description": "Pourcentage (%) de la couleur 1 dans le mélange final --- assurez-vous de totaliser 100% avec vos trois couleurs",
                    "type": "int",
                    "default_value": 0,
                    "minimum_value": 0,
                    "maximum_value": 100
                 },
                "finb":
                {
                    "label": "Buse 2",
                    "description": "Pourcentage (%) de la couleur 2 dans le mélange final --- assurez-vous de totaliser 100% avec vos trois couleurs",
                    "type": "int",
                    "default_value": 0,
                    "minimum_value": 0,
                    "maximum_value": 100
                 },
                "finc":
                {
                    "label": "Buse 3",
                    "description": "Pourcentage (%) de la couleur 3 dans le mélange final --- assurez-vous de totaliser 100% avec vos trois couleurs",
                    "type": "int",
                    "default_value": 100,
                    "minimum_value": 0,
                    "maximum_value": 100
                 }
            }
        }"""
        
    def execute(self, data):
        zDebut = self.getSettingValueByKey("debut")
        zFin = int(self.getSettingValueByKey("fin"))
        if zFin < zDebut:
            passe = zDebut
            zDebut = zFin
            zFin = passe
        coulInitA = self.getSettingValueByKey("inita")
        coulInitB = self.getSettingValueByKey("initb")
        coulInitC = self.getSettingValueByKey("initc")
        coulFinA = self.getSettingValueByKey("fina")
        coulFinB = self.getSettingValueByKey("finb")
        coulFinC = self.getSettingValueByKey("finc")
        if (coulFinC + coulFinC + coulFinC) > 100:
            coulFinC = 100 - coulFinA - coulFinB
        compte = 0
        nombre = zFin - zDebut

        for layer_number, layer in enumerate(data):
            rendu = layer_number - 2
            if rendu >= zDebut and rendu <= zFin:
                cumul = 0
                cherche = ";LAYER:"
                remplace = cherche + str(rendu) + "\n"
                # Première valeur
                val = (coulFinA - coulInitA) * (compte/nombre)
                val = round(val)
                if val == 100:
                    sval = "1.00"
                else:
                    cumul += val
                    sval = str(val)
                    if val < 10:
                        sval = "0" + str(val)
                    sval = "0." + sval + "00"
                    sval = sval[0:4]
                remplace += "M163 S0 P" + sval + "\n"
                # Deuxième valeur
                val = (coulFinB - coulInitB) * (compte/nombre)
                val = round(val)
                if val == 100:
                    sval = "1.00"
                else:
                    cumul += val
                    sval = str(val)
                    if val < 10:
                        sval = "0" + str(val)
                    sval = "0." + sval + "00"
                    sval = sval[0:4]
                remplace += "M163 S1 P" + sval + "\n"
                # Troisième valeur
                val = (coulFinC - coulInitC) * (compte/nombre)
                val = round(val)
                if val == 100 or cumul == 0:
                    sval = "1.00"
                else:
                    cumul += val
                    while cumul < 100:
                        val += 1
                        cumul += 1
                    sval = str(val)
                    if val < 10:
                        sval = "0" + str(val)
                    sval = "0." + sval + "00"
                    sval = sval[0:4]
                remplace += "M163 S2 P" + sval + "\n;"

                data[layer_number] = re.sub(cherche, remplace, layer)
                compte += 1

        return data

