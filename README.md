# Linky-Collector 

This project is about collecting and displaying informations from French power distributions units. 
All the project will be written in French. 

Ce projet a pour but de récupérer et d'afficher les information du compteur électrique. 

## Avertissement 

Si vous êtes amenés à réaliser ce projet, nous ne sommes pas responsable des conséquences de vos actions. La mise à disposition de ce projet n'a que pour but d'information. 
La réalisation de ce projet implique de travailler proche de sources de tensions mortelles. Faites uniquement ce que vous êtes sûr de savoir faire. En cas de doute, demandez à un professionnel. 

## Préambule

Les compteurs compatibles sont ceux disposant de ports TIC (TéléInformation Client). 
A ce jour il en existe principalement deux sortes  : 
- Compteurs Classique 
- Compteurs "Linky"

On utilisera les sorties TIC de ces compteurs (sorties d'information), à ne pas confondre avec les sorties traditionnelles (généralement repérées C1 - C2 - ...). Ces sorties ont une tension de 230v quand actives ! (cf. Avertissement)

Les compteurs Linky sont par défaut en mode "Historique". Vous pouvez faire la demande auprès de votre gestionnaire de réseau pour basculer le compteur en mode "Standard" (cf. ci-dessous le comparatif des modes).

## Technologies

On distingue 2 technologies de transmission de données utilisées par les compteurs: 

|Tech. "Historique"|Tech. "Standard"  |
|--|--|
| Tous les compteurs avec TIC| Uniquement "Linky", paramétré dans ce mode |
|Porteuse de 50kHz|Porteuse de 50kHz|
|UART - Async Serial|UART - Async Serial|
|Async Serial Vitesse : 1200 Bauds|Vitesse : 9600 Bauds|
|Caractéristique de transmission : logique négative (0 = présence porteuse, 1 = absence porteuse), LSB First, "0" start bit, 7 bit ASCII (Donc 8 bit par transfert, "1" bit stop, bit parité paire (even)  |Caractéristique de transmission : logique négative (0 = présence porteuse, 1 = absence porteuse), LSB First, "0" start bit, 7 bit ASCII (Donc 8 bit par transfert, "1" bit stop, bit parité paire (even)|
|Trame : 7 éléments|Trame : 7 ou 9 éléments (Horodate en plus selon champ)|
|Début de transmission < STX > (0x02)|Début de transmission < STX > (0x02)|
|< LF > (0x0A) Label < SP > (0x20) Data < SP > Checksum < CR > (0x0D)|< LF > (0x0A) Label [< HT > (0x09) Heure] < HT > Data < HT > Checksum < CR > (0x0D)|
|Fin de transmission : < ETX > (0x03)|Fin de transmission : < ETX > (0x03)|

Le raccordement s'effectue aux bornes I1 I2 du compteur. 

## Structure du projet
- Doc : Documentation spécifique au projet
- Code : Toute la partie programmation 
- Elec : Toute la partie physique, schémas de montage ... 

## Références

Documentation ErDF / ENEDIS : 
 - TIC "Historique" : [ERDF-NOI-CPT_02E.pdf](https://git.bde-insa-lyon.fr/colloc/linky_collector/doc/ERDF-NOI-CPT_02E.pdf)
 - TIC "Standard" : [Enedis-NOI-CPT_54E.pdf](https://git.bde-insa-lyon.fr/colloc/linky_collector/doc/Enedis-NOI-CPT_54E.pdf)
 
## Auteurs

Alban PRATS
Hugo REYMOND