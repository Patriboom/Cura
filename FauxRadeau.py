# Copyright (c) 2017 Ghostkeeper
# The PostProcessingPlugin is released under the terms of the AGPLv3 or higher.

import re #Afin de remplacer un gros radeau par quelques couches (de votre modèle) un peu ralenties lors de l'impression

from ..Script import Script


class FauxRadeau(Script):
    """Ralentissons l`impression des premières couche afin d'éviter un gros radeau inutile.

    Ce script s'appliquera à la couche 0 est jusqu'avant la couche que vous désignerez.

    Si vous désignez la couche 2 comme limite, seules les couches 0 et 1 seront ralenties
    """

    def getSettingDataString(self):
        return """{
            "name": "Faux radeau",
            "key": "FauxRadeau",
            "metadata": {
                "name": "Faux radeau",
                "author": "Patrick ALLAIRE, ptre",
                "version": "0.1",
                "description": "Remplacer un gros radeau par quelques couches ralenties, c`est payant!",
                "supported_sdk_versions": ["5.0.0"]
            },
            "version": 2,
            "settings":
            {
                "debut":
                {
                    "label": "Début",
                    "description": "Couche initiale du ralentissement.  (valeur suggérée: 0)",
                    "type": "str",
                    "default_value": "0"
                },
                "finit":
                {
                    "label": "Fin",
                    "description": "Couche où la reprise de la vitesse normale s`applique.  (valeur suggérée: 2)",
                    "type": "str",
                    "default_value": "2"
                },
                "vitesse":
                {
                    "label": "% de la vitesse",
                    "description": "Pourcentage de la vitesse auquel doivent être imprimées le couches ralenties",
                    "type": "str",
                    "default_value": 50
                }
            }
        }"""

    def execute(self, data):
        cherch_debut = "LAYER:{}".format(self.getSettingValueByKey("debut"))
        cherch_debute = re.compile(cherch_debut)
        remplace_debut = "LAYER:{}\nM220 S{}  ;Vitesse ralentie à {}% de la vitesse normale --- script FauxRadeau.".format(self.getSettingValueByKey("debut"), self.getSettingValueByKey("vitesse"), self.getSettingValueByKey("vitesse"))
        for layer_number, layer in enumerate(data):
            data[layer_number] = re.sub(cherch_debute, remplace_debut, layer) #Replace all.

        cherch_finit = "LAYER:{}".format(self.getSettingValueByKey("finit"))
        cherch_finite = re.compile(cherch_finit)
        remplace_finit = "LAYER:{}\nM220 S100 ;Retour à la vitesse normale --- script FauxRadeau.".format(self.getSettingValueByKey("finit"))
        for layer_number, layer in enumerate(data):
            data[layer_number] = re.sub(cherch_finite, remplace_finit, layer) #Replace all.

        return data
