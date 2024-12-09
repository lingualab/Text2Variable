# Database Mecaniques de production de la parole

## Liste fragments
liste_fragments = {
    "Francais": ["NA"],
    "English": ['f', 'n', 'N', 'di', 'wa', 'dr', 'clo', 'di', 'lo', 'b', 'mo', 'wat', 'gon', 'tw', 'wha', 'st', 'rec', 'fff', 'ha', 'i',
                                'hap', 'gir', 'mirr', 'gra', 'ba', 'sh', 'r', 'fa', 'ben', 'ch', 'ru', 'chil', 'd', 'ap', 's', 'laun'],
}

## Liste fragments en contexte
words_targets = {
    "Francais": [('mot1_fr', 'mot2_fr'), ('mot3_fr', 'mot4_fr')],
    "English": [('the', 'there'), ('dry', 'or'), ('out', 'outside'), ('wash', 'drying'), ('curt', 'the'), ('is', 'spill'), ('wash', 'is'), ('bow', 'Cup'), ('tap', 'taps'),
           ('spill', 'is'), ('kit', 'the'), ('stand', 'standing'), ('go', 'reaching'), ('dish', 'The'), ('look', 'uh'), ('dry', 'or'), ('watch', 'washing'), ('sleeve', 'sleeveless'),
           ('cook', 'cookie'), ('a', 'an'), ('day', 'daytime'), ('curt', 'the'), ('look', 'reaching'), ('sister', 'reach'), ('cab', 'the'), ('cook', 'the'), ('stand', 'climbing'), ('her','ask'),
           ('ask', 'asking'), ('up', 'upper')],
}

# Database Fluence

## Liste des mots cibles pour identifier des pauses
dictPauses = {
    'English': {'filled': ['uhm', 'uh', 'uhummm', 'hum', 'hummmm', 'humm', 'mm', 'mmm', 'Mm', 'um', 'hmmm', 'hmm', 'hm', 'eh', 'err']},
    'Francais': {'filled': ['euh', 'hum', 'heu', 'hm', 'öhm', 'uhm', 'mmh', 'mh']},
    'UCSF': {'filled': ["um", "er", "uh", "ah", "hmm", "erm", "like", "so", "well"]}
}

# Database caractéristiques linguistiques

## Nom des étiquettes POS (parties du discours) de l'anglais vers le français
# Correspondance des étiquettes POS entre l'anglais et le français
pos_mapping = {
    'ADJ': 'Adjectif', 'ADP': 'Preposition', 'ADV': 'Adverbe',
    'AUX': 'Auxiliaire', 'CONJ': 'Conjonction', 'CCONJ': 'Conjonction_de_coordination',
    'DET': 'Determinant', 'INTJ': 'Interjection', 'NOUN': 'Nom',
    'NUM': 'Numeral', 'PART': 'Particule', 'PRON': 'Pronom',
    'PROPN': 'Nom propre', 'PUNCT': 'Ponctuation', 'SCONJ': 'Conjonction_de_subordination',
    'SYM': 'Symbole', 'VERB': 'Verbe', 'X': 'Autre'
}

# Dictionnaire des pronoms déictiques pour chaque langue
deictic_pronouns = {
    "English": {
        "spatial": {"here", "there", "this", "these", "that", "those"},
        "personal": {"i", "you", "he", "she", "it", "we", "they"},
        "temporal": {"now", "then", "soon", "tomorrow"}
    },
    "Francais": {
        "spatial": {"ce", "cet", "cette", "ces", "celui-ci", "celle-ci", "ceux-ci", "celles-ci", "celui-là", "celle-là", "ceux-là", "celles-là", "y", "en"},
        "personal": {"je", "tu", "il", "elle", "nous", "vous", "ils", "elles"},
        "temporal": {"y", "en"}
    }
}

# Liste des termes indéfinis en anglais et en français
termes_indefinis = {
    "Francais": ["truc", "chose", "peu", "beaucoup", "quelques", "plusieurs", "quelqu'un", "tout le monde", 
           "personne", "chacun", "n'importe qui", "autre", "l'autre", "chaque", "ni l'un ni l'autre", 
           "les deux", "d'autres"],
    "English": ["thing", "stuff", "anything", "nothing", "anyone", "one", "either", "neither", "everyone", 
                "no one", "someone", "anybody", "everybody", "nobody", "somebody", "another", "the other", 
                "each", "little", "less", "much", "both", "few", "fewer", "many", "other", "others", "several"]
}

# Database Caractéristiques sémantiques

# Dictionnaires ICU pour les deux langues
dictICU_cookie_fr = {
    'mère': ['mère', 'maman', 'mamie', 'mam', 'mamma', 'momma', 'ma', 'mama', 'femme'],
    'garçon': ['garçon', 'gamin', 'mec', 'gosse', 'fils', 'écolier', 'jeune homme', 'jeune garçon', 'enfant mâle'],
    'fille': ['fille', 'fille', 'jeune fille', 'écolière', 'jeune dame', 'jeune fille', 'enfant femelle'],
    'cuisine': ['cuisine'],
    'extérieur': ['extérieur', 'dehors', "à l'air libre", 'en plein air'],
    'robinet': ['robinet', 'évacuation', 'mitigeur'],
    'eau': ['eau'],
    'évier': ['évier'],
    'sol': ['sol', 'terre', 'plancher'],
    'assiette': ['assiette', 'plat', 'plateau', 'soucoupe'],
    'vaisselle sur comptoir': ['posée sur', 'placée sur', 'étalée sur'],
    'comptoir': ['comptoir', 'plan de travail'],
    'cookies': ['cookies', 'biscuit', 'biscuits'],
    'bocal': ['bocal', 'pot', 'boîte'],
    'placard': ['placard', 'armoire', 'placards', 'armoires'],
    'tabouret': ['tabouret', 'escabeau'],
    'fenêtre': ['fenêtre'],
    'rideau': ['rideau', 'store', 'écran', 'volet'],
    'garçon prenant cookie': ['prenant', 'saisissant', 'atteignant', 'prendre', 'saisir', 'atteindre', 'se saisir'],
    'garçon/tabouret tombant': ['tombant', 'basculant', 'tomber', 'basculer'],
    'mère séchant/lavant vaisselle': ['sécher', 'séchant', 'laver', 'lavant', 'nettoyer', 'nettoyant', 'frotter', 'frottant', 'essuyant', 'faire la vaisselle'],
    'eau débordant': ['déborder', 'débordant', 'renverser', 'renversant', 'cascader', 'évier débordant', 'débordement'],
    'fille demandant cookie': ['demander', 'demandant', 'vouloir', 'veut', 'solliciter', 'sollicite'],
    'mère indifférente au débordement': ['indifférente', 'pas dérangée', 'se soucier', 'pas dérangé', 'remarqué', 'déranger'],
    'mère ne remarquant pas les enfants': ['inconsciente', 'remarqué', 'pas remarqué', 'pas prendre garde', 'pas dérangée', 'pas dérangé'],
}

dictICU_cookie_en = {'mother': ['mother', 'mom', 'mum', 'mommy', 'mummy', 'mamma', 'momma', 'ma', 'mama', 'woman'], 
        'boy': ['boy', 'guy', 'dude', 'lad', 'son', 'schoolboy', 'young man', 'son', 'young boy', 'male child'], 
        'girl': ['girl', 'daughter', 'lass', 'schoolgirl', 'young lady', 'young girl', 'female child'],
        'kitchen': ['kitchen'], 
        'exterior': ['exterior', 'outside', 'outdoor', 'outdoors'],
        'faucet': ['faucet', 'drain', 'tap'],
        'water': ['water'], 
        'sink': ['sink'],            
        'floor': ['floor', 'ground', 'flooring'],
        'plate': ['plate', 'dish', 'platter', 'saucer'], 
        'dishes on counter': ['laying on', 'placed on', 'spread on'], 
        'counter' : ['counter', 'worktop', 'counter top', 'countertop'],
        'cookies': ['cookies', 'cookie', 'biscuits', 'biscuit'],
        'jar': ['jar', 'pot', 'tin'], 
        'cabinet': ['cabinet', 'cupboard', 'cabinets', 'cupboards'], 
        'stool': ['stool', 'footstool'], 
        'window': ['window'], 
        'curtain': ['curtain', 'blind', 'screen', 'shutter'], 
        'boy taking cookie': ['taking', 'grabbing', 'reaching', 'take', 'grab', 'reach', 'get hold'], 
        'boy/stool falling': ['falling', 'tipping', 'fall', 'tip'], 
        'mother drying/washing dishes': ['dry', 'drying', 'wash', 'washing', 'clean', 'cleaning', 'scrub', 'scrubbing', 'wiping', 'doing dishes', 'doing the dishes'],
        'water overflowing': ['overflow', 'overflowing', 'spill', 'spilling', 'cascading', 'sink running over', 'overrunning'], 
        'girl asking for cookie': ['ask', 'asking', 'want', 'wants', 'requesting', 'requests'],
        'mother unconcerned about overflowing': ['unconcerned', 'unbothered', 'care', 'not bothered', 'noticed', 'bother'],
        'mother not noticing children': ['unnoticing', 'noticed', 'not noticed', 'not take notice', 'unbothered', 'not bothered'],
}

# define Information Content Units (ICU) with the grid from Jensen, Chenery, Copland (2006) J Comm Dis
dictICU_picnic_en = {'father': ['father', 'husband', 'daddy', 'Dad', 'dad'], 
           'mother': ['mother', 'wife', 'mom', 'mommy', 'girl'], 
           'couple': ['couple', 'parents', 'owners'],
            'child': ['child'], 
           'boy': ['boy', 'brother'],
           'fisherman': ['fisherman', 'fisher', 'rod'],
           'sailors': ['sailors', 'people', 'people sailing'], 
           'dog': ['dog', 'doggy', 'animal'], 
           
           'garage': ['garage'],
           'water': ['water', 'lake', 'river', 'sea', 'ocean',
                    'bank', 'edge', 'shore', 'riverside'], 
           'beach': ['beach', 'sand'], 
           #'pail': ['pail', 'blanket'], this one is not in Jensen
           'jetty' : ['jetty', 'wharf', 'dock'],
           'kite': ['kite'],
           'book': ['book', 'novel'], 
            'bucket': ['bucket'], 
           'spade': ['spade', 'shovel'], 
           'car': ['car', 'vehicle', 'automobile', 'sedan', 'wagon'], 
           'boat': ['boat', 'sailboat', 'yacht', 'vessel', 'slinghy', 'sloop'], 
           'flag': ['flag', 'pole'], 
           'radio': ['radio', 'transistor'], 
           'sandals': ['sandals', 'shoes', 'shoe', 'flip', 'flops'],
           'tree': ['tree' 'oak'], 
           'basket': ['basket'],
           'drink': ['drink', 'bottle', 'wine', 'soda', 'beer', 'liquor', 
                       'coffee', 'tea'],
            'house': ['house', 'cottage', 'shack', 'cottage'],
           'reading': ['reading', 'read'], 
           'fishing': ['fishing', 'fish', 'catch'], 
           'pouring': ['pouring', 'pour', 'serve'], 
           'flying': ['flying', 'fly'], #flag
           'flying' : ['flying', 'fly'], #kite
           'playing': ['playing', 'play', 'build', 'building'], # child on the beach
           'playing': ['playing', 'blasting'], # radio
           'picnicking': ['picnic', 'picnicking'], 
           'sailing': ['sailing', 'sail', 'boating'], 
           'parking': ['parking', 'parked', 'park']
          }

# Database Caractéristiques syntaxiques

## Traductions des étiquettes de dépendance en français
dep_labels_fr = {
    'nsubj': 'Sujet_nominal',
    'ROOT': 'Racine',
    'det': 'Determinant',
    'amod': 'Modificateur_adjectival',
    'compound': 'Compose',
    'dobj': 'Objet_direct',
    'prep': 'Preposition',
    'pobj': 'Objet_de_preposition',
    'punct': 'Ponctuation',
    'expl': 'Element_expletif',
    'attr': 'Attribut',
    'acl': 'Clause_adjectivale',
    'advcl': 'Clause_adverbiale',
    'aux': 'Auxiliaire',
    'xcomp': 'Complement_ouvert',
    'conj': 'Conjonction',
    'cc': 'Conjonction_de_coordination',
    'neg': 'Negation',
    'dative': 'Datif'
}

translation_dict = {
    'csubj': 'Sujets_Clausaux',
    'xcomp': 'Complements_Clausaux_Controles',
    'ccomp': 'Complements_Clausaux_Non_Controles',
    'advcl': 'Modificateurs_Clauses_Adverbiaux',
    'acl': 'Modificateurs_Clauses_Adnominaux'
}

## Dictionnaire des conjonctions de coordination par langue
coordination_conjunctions = {
    'English': {"and", "but", "for", "nor", "or", "yet", "so"},
    'Francais': {"et", "mais", "ou", "donc", "or", "ni", "car"}
}

# Database Caractéristiques pragmatiques

## Mots d'incertitude en anglais et en français
uncertainty_words = {
    'English': {"think", "look", "like", "kind", "seem", "maybe", "can", "something"},
    'Francais': {"penser", "sembler", "comme", "genre", "peut-être", "peut", "quelque", "chose"}  
}

## Expressions formulaiques en anglais et en français
formulaic_expressions = {
    'English': {"well", "so", "I guess", "you know", "as it is", "as it were"},
    'Francais': {"bien", "alors", "je suppose", "tu sais", "comme il est", "comme il serait"}
}
## Expressions de modalisation en anglais et en français
expressions = {
    'English': {"I think", "In my opinion", "of course", "naturally", "unsure", "likely", "could be that", "unfortunately", "surely"},
    'Francais': {"je pense", "à mon avis", "bien sûr", "naturellement", "incertain", "probablement", "ça pourrait être que", "malheureusement", "sûrement"}
}

## Dictionnaires des expressions de remplissage pour l'anglais et le français
filler_expressions_dict = {
    'English': {"you know", "I mean"},
    'Francais': {"tu sais", "je veux dire"}  
}