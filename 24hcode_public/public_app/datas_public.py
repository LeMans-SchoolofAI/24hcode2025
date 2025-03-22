from langchain_core.tools import tool

@tool
def dict_sujets() -> dict:
    """
    Retourne le dictionnaire des sujets des 24h du code 2025 avec le nom des porteurs en clé et le sujet en valeur
    """
    print("DEBUG: dict_sujets")
    x = {
        "HAUM":"Le sujet du HAUM cette année porte sur la fabrication d'un robot autonome et de la résolution d'un labyrinthe",
        "Sopra Steria":"Sopra Steria propose un sujet sur la création du ville numérique avec gestion des ressources et de la pollution",
        "Le Mans School of AI":"Le Mans School of AI propose un sujet sur l'IA, avec la création d'un agent conversationnel jouant le rôle d'un majordome d'hôtel",
        "ST Microelectronics":"ST Microelectronics propose un sujet sur l'innovation avec leur matériel électronique, sur le thème de qui veut être mon associé"
    }
    return x


@tool
def dict_orgas_sujets() -> dict:
    """
    Retourne le dictionnaire des organisateurs des sujets des "24h du code" en clé ainsi qu'une description de chaque organisateur en valeur
    """
    print("DEBUG: dict_orgas_sujets")
    x = {
        "HAUM":"""Le HAUM est un hackerspace situé au Mans, fondé en 2011, qui promeut la culture du Do It Yourself et du libre.
            Il propose à ses membres un accès à divers outils et machines pour réaliser des projets collaboratifs
            et participe à des événements comme les Repair Cafés et les "24 Heures du code".""",
        "Sopra Steria":"""Sopra Steria est un entreprise de services numériques internationale, qui propose des services de conseil,
            de développement et de maintenance de logiciels. Elle participe aux "24 Heures du code" en tant que partenaire
            et sponsor de l'événement.""",
        "Le Mans School of AI":"""Le Mans School of AI est une auto-organisation de partage de connaissances en intelligence artificielle.
            Ouverte à tous, mais principalement aux développeur ou étudiants en informatique, elle propose des ateliers et des
            conférences sur des sujets variés en IA. Après avoir remporté de nombreuses éditions des "24 Heures du code", elle a basculé dans
            l'organisation de l'événement en 2023.""",
        "ST Microelectronics":"""ST Microelectronics est un fabricant de semi-conducteurs et de composants électroniques. Spécialisé dans l'informatique
            embarqué, l'entreprise propose chaque année des sujets autour de robots ou de composants électroniques pour les "24 Heures du code"."""
    }
    return x

@tool
def dict_lieu() -> dict:
    """
    Retourne le dictionnaire des lieux des "24h du code" en clé ainsi que l'emplacement de chaque lieu en valeur
    """
    print("DEBUG: dict_lieu")
    x = {
        "Le Mans School of AI":"Situé à gauche de l'escalier principal quand on est en face",
        "Sopra Steria":"Situé à droite de l'escalier principal quand on est en face",
        "HAUM":"Situé sur la mezzanine, directement à droite de l'entrée principale",
        "ST Microelectronics":"Situé au fond à gauche par rapport à l'entrée principale",
        "Toilettes du rez-de-chaussée":"Situées à droite de l'escalier principal",
        "Toilettes du deuxième étage":"Situées à gauche en montant l'escalier principal",
        "Toilettes du quatrième étage":"Situées à gauche en montant l'escalier principal",
        "Salle de conférence":"Située au sixième étage, prendre l'ascenseur situé au bout du couloir à droite",
        "Salon Vielle":"Situé au deuxième étage, à droite en montant l'escalier principal",
    }
    return x


@tool
def dict_programme_public() -> dict :
    """
    Retourne le dictionnaire des activités du programme public des 24h du code 2025, les horaires, les lieux et diverses informations
    """
    print("DEBUG: dict_programme_public")
    x = {
        "Atelier à destination des enfants #BOT | Proposé par le Conseil départemental de la Sarthe | A la CCI Le Mans Sarthe":
            """Initiation à la programmation avec les robots Mbots ! - dès 12 ans
            Séance de 1h15 minutes
            2 séances disponibles : 15h ou 16h30""",
        "Atelier à destination des enfants #DRONE | Proposé par Eurientis | A la CCI Le Mans Sarthe":
            """Programme ton drone en t'amusant ! - dès 12 ans
            Séance de 45 minutes
            3 séances disponibles : 14h30 - 15h30 - 16h30""",
        "Atelier #VOITURE 3D | Proposée par l'association Filamans du lab' Campus CESI LE MANS | A la CCI Le Mans Sarthe":
            """Les étudiants de l’association FILAMANS, du lab’ campus CESI LE MANS, vous ferons découvrir la construction d’une voiture télécommandée via des imprimantes 3D
            Accessible à tout âge
            Durée : aléatoire
            Les plus petits pourront repartir avec des portes clés dinosaures articulés, imprimés
            sur place en 3D.
            Horaires : de 14h à 18h30 en accès libre""",
        "Animation #ROBOTS | Proposée par le HAUM | A la CCI Le Mans Sarthe":
            """Plongez dans l’univers des robots avec le HAUM !
            Dès 5 ans
            Durée : aléatoire
            Horaires : de 14h à 18h en accès libre""",
        "Conférence #IA | Animée par Pierre CARTIER - Fondateur de Plaïades | A la CCI Le Mans Sarthe":
            """L’Intelligence Artificielle : vers une utilisation intelligente et responsable !
            Durée : 1h
            Horaires : de 15h à 16h""",
        "REPAIR CAFÉ | Animé par le groupe repair café du centre social de Montfort le Gesnois | A la CCI Le Mans Sarthe":
            """Venez réparer et donner une seconde vie à vos appareils électriques, ordinateurs, …
            Durée : 1h environ
            Horaires : de 14h à 17h""",
        "Conférence | Animée par Sopra Steria | A la CCI Le Mans Sarthe":
            """Développeur, comment agir pour un numérique plus responsable ?
            Durée : 1h
            Horaires : de 16h à 17h""",
        "Animation #Battle de Just Dance sur #WiiU | A la CCI Le Mans Sarthe":
            """Bougez aux rythmes de chansons endiablées et affrontez vos amis dans des Battles de Danse
            Horaires : de 17h30 à 18h30""",
        "Tournoi avec le célèbre Babyfoot de la #JENSIM | A la CCI Le Mans Sarthe":
            """Venez partager un moment de convivialité, de fun et de compétition !
            Accessible en équipe de 2 personnes (8 équipes possibles)
            Horaires : de 14h30 à 16h""",
        "Des visites guidées grâce aux lycéens du lycée Touchard Washington | A la CCI Le Mans Sarthe":
            """Découvrez les métiers de la programmation informatique !
            En famille
            Environ 30 minutes
            Horaires : de 14h à 18h30""",
        "Une dégustation de thés par Le Palais des Thés | A la CCI Le Mans Sarthe":
            """Découvrez les différentes propositions de la boutique du centre-ville, spécialement sélectionnées pour l'événement !
            Horaires : de 15h à 17h""",
        "Une dégustation de gourmandises par Le Comptoir de Mathilde | A la CCI Le Mans Sarthe":
            """Découvrez les différents produits de la boutique du centre-ville !
            Horaires : de 15h à 17h""",
        "Une crêpes party avec des confitures de La Fée Confiture | A la CCI Le Mans Sarthe":
            """
            Dégustez une délicieuse crêpes avec de délicieuses confitures ou
            l'accompagnement de votre choix !
            Horaires : de 15h à 17h""",
        "Des jeux vidéo et consoles rétro avec l’association #RETROTAKU | A la CCI Le Mans Sarthe":
            """Faites une pause ludique en famille et affrontez-vous le temps d'une partie !
            En famille
            En libre service
            Horaires : de 14h à 18h30""",
        "Un Puissance 4 Géant sera proposé par #SII | A la CCI Le Mans Sarthe":
            """Faites une pause ludique à deux le temps d'une partie !
            En duo
            En libre service
            Horaires : de 14h à 18h30""",
        "Un bar à bonbons | A la CCI Le Mans Sarthe":
            """Rechargez les batteries avec une pause sucrée !
            En famille
            A la demande
            Horaires : de 15h à 17h""",
        "Un bar à jus de fruits | A la CCI Le Mans Sarthe":
            """Rechargez les batteries en faisant une pause vitaminée !
            En famille
            A la demande
            Horaires : de 15h à 17h"""
    }
    return x
    
    
@tool
def str_histoire() -> str:
    """
    Retourne une chaine de caractère contenant l'histoire des 24h du code
    """
    print("DEBUG: str_histoire")
    x = """Les 24h du code sont un événement annuel organisé par la chambre de commerce et d'industrie du Mans et de la Sarthe ainsi 
    que l'ENSIM, l'école d'ingénieurs du Mans et différents porteurs de sujets. Cet événement a pour but de promouvoir la programmation
    informatique et les métiers du numérique en général. Les participants ont 24 heures pour réaliser un projet en équipe, en utilisant
    les outils et les technologies de leur choix sur des sujets imposés au choix. Les projets sont ensuite présentés devant un jury de professionnels 
    qui décerne des prix. Cet événement est ouvert à tous les développeurs, en deux catégories, les étudiants et les professionnels.
    Les 24h du code sont également l'occasion de participer à des ateliers, des conférences et des animations pour le public autour de la programmation
    informatique et des nouvelles technologies.
    
    Les premières éditions sont nées il y a plus de 13 ans, organisées par l'ENSIM, avec un problème d'organisation des cours d'informatique à l'école.
    Un enseignant s'est alors dit, comment faire tenir 24 heures de cours et de travaux pratiques en si peu de temps. C'est ainsi que l'idée des 24h du code
    est née. Les premières éditions étaient réservées aux étudiants de l'école, puis l'événement s'est ouvert à d'autres écoles et aux professionnels.
    """
    return x

