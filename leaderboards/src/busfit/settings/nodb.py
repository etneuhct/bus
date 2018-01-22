# -*-coding:utf8-*-
"""
Fichier de configuration à utiliser pour les tests ne nécessitant pas la présence d'une base de donnée.
"""
from settings.development import *


TEST_RUNNER = 'busfit.runners.NoDBTestRunner'
