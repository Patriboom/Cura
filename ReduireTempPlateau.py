# Copyright (c) 2017 Ghostkeeper
# The PostProcessingPlugin is released under the terms of the AGPLv3 or higher.

import re #Afin de réduire la température plateau après quelques couches d'impression. Ceci est fait dans le but d'éviter le séchage et la torsion des couches initiales.

from ..Script import Script


class ReduireTempPlateau(Script):
    """Réduction de la température du plateau

    Ce script modifiera la température du plateau à la hauteur de votre choix et à la température de votre choix

    Si vous désignez la couche 2 comme limite, la température commencera à descendre au début de l'impression de la couche 2.

    Bien entendu, le plateau ne perdra sa chaleur que progressivement et la température visée ne sera atteinte que vers la couche 4 ou 5.

    L'impression n'est pas interrompue, l'imprimante n'entendra pas l'atteinte de la température visée avant de remprendre l'impression.
    """

    def getSettingDataString(self):
        return """{
            "name": "Rafraichit plateau",
            "key": "ReduireTempPlateau",
            "metadata": {
                "name": "Rafraichit plateau",
                "author": "Patrick ALLAIRE, ptre",
                "version": "0.1",
                "description": "Réduire la température du plateau une fois que les couches initiales y sont bien adhérées.",
                "supported_sdk_versions": ["5.0.0"]
            },
            "version": 2,
            "settings":
            {
                "debut":
                {
                    "label": "Début",
                    "description": "Couche initiale du changement.  (valeur suggérée: 3)",
                    "type": "str",
                    "default_value": "3"
                },
                "temperature":
                {
                    "label": "Température",
                    "description": "Température du plateau visée pour la suite de l'impression. (valeur suggérée 35)",
                    "type": "str",
                    "default_value": 35
                }
            }
        }"""

    def execute(self, data):
        chercheTxt = "LAYER:{}".format(self.getSettingValueByKey("debut"))
        cherche = re.compile(chercheTxt)
        remplace = "LAYER:{}\nM140 S{}  ;Nouvelle température de plateau visée --- script ReduireTempPlateau.".format(self.getSettingValueByKey("debut"), self.getSettingValueByKey("temperature"), self.getSettingValueByKey("temperature"))
        for index, layer in enumerate(data):
            data[index] = re.sub(cherche, remplace, layer) #Replace all.


        return data
