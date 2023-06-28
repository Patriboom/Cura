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
        
    def pourcentage(self, valeur, cumulons, coul):
        if valeur == 100:
            v = "1.00"
        elif cumulons == 0 and coul == "C":
            v = "1.00"
            cumulons = 100
        else:
            cumulons += valeur
            if coul == "C":
                while cumulons < 100:
                    valeur += 1
                    cumulons += 1
            v = str(valeur)
            if valeur < 10:
                v = "0" + v + "0"
            v = "0." + v + "000"
            v = v[0:4]
                
        return str(v), cumulons
       
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

        for index, layer in enumerate(data):
            rendu = index - 2
            if rendu >= zDebut and rendu <= zFin:
                cumul = 0
                cherche = ";LAYER:"
                remplace = cherche + str(rendu) + "\n"
                # Première valeur
                val = (coulFinA - coulInitA) * (compte/nombre)
                val = round(val)
                sval, cumul = self.pourcentage(val, cumul, "A")
                remplace += "M163 S0 P" + sval + "\n"
                # Deuxième valeur
                val = (coulFinB - coulInitB) * (compte/nombre)
                val = round(val)
                sval, cumul = self.pourcentage(val, cumul, "B")
                remplace += "M163 S1 P" + sval + "\n"
                # Troisième valeur
                val = (coulFinC - coulInitC) * (compte/nombre)
                val = round(val)
                sval, cumul = self.pourcentage(val, cumul, "C")
                remplace += "M163 S2 P" + sval + "\n;"

                data[index] = re.sub(cherche, remplace, layer)
                compte += 1

        return data

