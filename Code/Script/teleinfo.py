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