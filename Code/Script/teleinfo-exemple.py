#!/usr/bin/env python
import configparser
import sys, serial, time, logging, logging.config, pprint, datetime, sqlite3, pymongo
from pymongo import MongoClient


# Port serie : /dev/ttyAMA0, 1200 Baud, 7E1

# Trame commence par STX et fini par ETX
# Exemple pour tarif HC WE

# MOTDETAT 000000 B
# ADCO 200000294579 P
# OPTARIF BASE 0
# ISOUSC 30 9
# BASE 002565285 ,
# PTEC TH.. $
# IINST 002 Y
# IMAX 030 B
# PAPP 00420 '

# Mode Standard HC WE
# ADSC 000000000000 6 - adresse sec compteur - serial no
# VTIC 02 J - Version TIC
# DATE H180128174015 G - Date et heure courante
# NGTF HC et Week-End U - Nom tarif
# LTARF HEURE WEEK-END 4 - Tarif actuel
# EAST 002050290 ! - Index Total
# EASF01 000784280 ? - Index 1 - HP
# EASF02 001154049 ; - index 2 - HC
# EASF03 000111961 7 - Index 3 - WE
# EASF04 000000000 % - Index 4
# EASF05 000000000 & - Index 5
# EASF06 000000000 ' - Index 6
# EASF07 000000000 ( - Index 7
# EASF08 000000000 ) - Index 8
# EASF09 000000000 * - Index 9
# EASF10 000000000 " - Index 10
# EASD01 001010341 * - Index Ditri 1
# EASD02 001039949 D - Index Distri 2
# EASD03 000000000 " - Index Distri 3
# EASD04 000000000 # - Index Distri 4
# IRMS1 007 5 - Courant Efficace
# URMS1 210 = - Tension efficace
# PREF 09 H - Puissance ref
# PCOUP 09 " - Puissance coupure
# SINSTS 01415 Q - Puissance instantane
# SMAXSN H180128132221 05374 ? - Pmax jour n
# SMAXSN-1 H180127195647 04715 / - Pmax jour n-1
# UMOY1 H180128174000 208 8 - Tension moyenne
# STGE 002A4800 D - Registre status
    # 0 Contact sec
    # 1 Organe de coupure
    # 2 Cache bornes
    # 3 N/A
    # 4 Surtension
    # 5 Depassement Pref
    # 6 prod/conso
    # 7
    # 8
# MSG1 PAS DE MESSAGE < - Message court
# PRM 00000000000000 : - Point de livraison
# RELAIS 001 C - Relais
# NTARF 03 P - Numero index en cours
# NJOURF 01 ' - Numero jour tarifaire en cours
# NJOURF+1 00 B - Numero prochain jour tarifaire


def lectureTrame(ser):
    """Lecture d'une trame sur le port serie specifie en entree.
    La trame debute par le caractere STX (002 h) et fini par ETX (003 h)"""
    # Lecture d'eventuel caractere avant le debut de trame
    # Jusqu'au caractere \x02 + \n (= \x0a)
    trame = list()
    while trame[-2:] != ['\x02', '\n']:
        trame.append(ser.read(1))
    print('Lecture de caracteres avant trame : \n' + pprint.pformat(trame))
    # Lecture de la trame jusqu'au caractere \x03
    trame = list()
    while trame[-1:] != ['\x03']:
        trame.append(ser.read(1))
    print('Lecture de caracteres trame (avant pop) : ' + pprint.pformat(trame))
    # Suppression des caracteres de fin '\x03' et '\r' de la liste
    trame.pop()
    trame.pop()
    return trame


def decodeTrame(trame):
    """Decode une trame complete et renvoie un dictionnaire des elements"""
    # Separation de la trame en groupe
    lignes = trame.split('\r\n')
    logger.debug('Groupes de la trame : \n' + pprint.pformat(lignes))
    result = {}
    for ligne in lignes:
        tuple = valideLigne(ligne)
        result[tuple[0]] = tuple[1]
    return result


def valideLigne(ligne):
    """Retourne les elements d'une ligne sous forme de tuple si le checksum est ok"""
    chk = checksumLigne(ligne)
    items = ligne.split(' ')
    if ligne[-1] == chk:
        return (items[0], items[1])
    else:
        logger.error("Pb de checksum : calcul = " + chk + " / chk dans trame = " + items[2])
        raise Exception("Checksum error")


def checksumLigne(ligne):
    """Verifie le checksum d'une ligne et retourne un tuple"""
    sum = 0
    for ch in ligne[:-2]:
        sum += ord(ch)
    sum = (sum & 63) + 32
    logger.debug("Checksum ligne : " + ligne + " ==> " + chr(sum))
    return chr(sum)


def ligneToCSV(lignes, cles):
    ligneCSV = list()
    ligneCSV.append(time.strftime("%Y-%m-%d", time.localtime()))
    ligneCSV.append(time.strftime("%H:%M:%S", time.localtime()))
    for cle in cles:
        # Attention, transformation de String en Int ... Toutes les cles ne fonctionnent pas !!!
        # Double conversion pour supprimer les 0 a gauche
        valeur = str(int(lignes[cle]))
        ligneCSV.append(valeur)
    return ";".join(ligneCSV)


def ligneToSQLite(lignes):
    db = sqlite3.connect('/home/pi/teleinfo/python/compteurElec.db', detect_types=sqlite3.PARSE_COLNAMES)
    c = db.cursor()
    c.execute('INSERT INTO teleinfo(date, indexconso, intensite, puissance) VALUES(?, ?, ?, ?)'
              , (datetime.datetime.now(), lignes['BASE'], lignes['IINST'], lignes['PAPP']))
    db.commit()


def ligneToMongo(lignes):
    client = MongoClient('moninstance.mongolab.com', 41758)
    db = client.home
    db.authenticate('monlogin', 'monpassword')
    collection = db['ConsoElec']
    docToInsert = {"datetime": datetime.datetime.now(),
                   "indexconso": int(lignes['BASE']),
                   "intensite": int(lignes['IINST']),
                   "puissance": int(lignes['PAPP'])}
    collection.insert(docToInsert)
    client.close


if __name__ == '__main__':
    # Initialisation Logger
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger(__name__)
    # loading config file
    config = configparser.ConfigParser()
    config.read('config.conf')
    perif = config['Compteur']['port']
    baudRate = config[config['Compteur']['Type']]['BaudRate']
    # Lecture du port serie
    ser = serial.Serial('/dev/'+perif, baudRate, 7, 'E', 1, timeout=1)
    ser.open()

    for i in range(2):
        logger.debug("tentative " + str(i))
        error = False
        ligneCSV = ''
        try:
            trame = lectureTrame(ser)
            # traitement de la trame
            lignes = decodeTrame("".join(trame))
            # export CSV
            ligneCSV = ligneToCSV(lignes, ['BASE', 'IINST', 'PAPP'])
            # Insertion en base
            # ligneToSQLite(lignes)
            ligneToMongo(lignes)
        except Exception as e:
            logger.error("Erreur : " + str(e))
            logger.error("Pb de lecture -> tentative complementaire " + str(i))
            error = True

        if not error:
            break;

    print
    ligneCSV

    ser.close()
