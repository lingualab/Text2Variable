import pandas as pd
from collections import Counter
import numpy as np

class LinguisticProcessor:
    def __init__(self, taggedCorpus):
        self.taggedCorpus = taggedCorpus

    def process_data(self):
        # Prepare the list to hold the processed data
        grammaList = []

        # Process each participant's data
        for participant, transcript in self.taggedCorpus.items():
            # Initialize counters and lists
            posCount = Counter()
            tagCount = Counter()
            depCount = Counter()
            lemmaList = []
            n_leftList = []
            n_rightList = []
            dep_list = []
            normList = []
            OOVList = []
            lemmaNouns = []
            lemmaVerbs = []
            allVerbs = []
            lemmaAdj = []
            verbLeftChild = []
            verbRightChild = []
            OOVWords = []
            lemmaVerbsSet = set()

            # Process each token in the transcript
            for token_data in transcript:
                token, lemma, pos, tag, dep, leftChildren, rightChildren, OOV, hasVector, L2norm = token_data
                # Count POS, TAG, and DEP
                posCount[pos] += 1
                tagCount[tag] += 1
                depCount[dep] += 1
                # Collect various data based on the token
                lemmaList.append(lemma)
                n_leftList.append(leftChildren)
                n_rightList.append(rightChildren)
                dep_list.append(len(dep))
                normList.append(L2norm)
                OOVList.append(OOV)
                if pos == 'NOUN':
                    lemmaNouns.append(lemma)
                if pos == 'VERB':
                    lemmaVerbs.append(lemma)
                    lemmaVerbsSet.add(lemma)
                    allVerbs.append(token)
                    verbLeftChild.append(leftChildren)
                    verbRightChild.append(rightChildren)
                if pos == 'ADJ':
                    lemmaAdj.append(lemma)
                if OOV:
                    OOVWords.append(token)

            # Calculate ratios and means
            pronounRatio = posCount.get('PRON', 0) / posCount.get('NOUN', 1)  # Avoid division by zero

            inflectedVerbs = len([x for x in allVerbs if x not in lemmaVerbsSet])

            # Compile the participant's data
            grammaSJ = {
                'lemmatized': lemmaList,
                'lemmaNouns': lemmaNouns,
                'lemmaVerbs': lemmaVerbs,
                'lemmaAdj': lemmaAdj,
                'pronounRatio': pronounRatio,
                'pronouns': posCount.get('PRON', 0),
                'verbs': posCount.get('VERB', 0),
                'adverbs': posCount.get('ADV', 0),
                'nouns': posCount.get('NOUN', 0),
                'adjectives': posCount.get('ADJ', 0),
                'interjections': posCount.get('INTJ', 0),
                'prepositions': posCount.get('ADP', 0),
                'determiners': posCount.get('DET', 0),
                'conjunctions': posCount.get('CCONJ', 0) + posCount.get('SCONJ', 0),
                'closedclass': sum(posCount.get(key, 0) for key in ['CCONJ', 'SCONJ', 'PRON', 'DET', 'ADP']),
                'openclass': sum(posCount.get(key, 0) for key in ['NOUN', 'VERB', 'ADJ', 'ADV']),
                'leftChildren': np.mean(n_leftList) if n_leftList else np.nan,
                'rightChildren': np.mean(n_rightList) if n_rightList else np.nan,
                'dep_length': np.mean(dep_list) if dep_list else np.nan,
                'dep_max': np.max(dep_list) if dep_list else np.nan,
                'L2norm': np.mean(normList) if normList else np.nan,
                'outOfVocabulary': np.mean(OOVList) if OOVList else np.nan,
                'inflectedVerbs': inflectedVerbs,
                'gerunds': tagCount.get('VBG', 0),
                'presenttense': tagCount.get('VBP', 0) + tagCount.get('VBZ', 0),
                'pasttense': tagCount.get('VBD', 0),
                'verbLeftChild': np.mean(verbLeftChild) if verbLeftChild else np.nan,
                'verbRightChild': np.mean(verbRightChild) if verbRightChild else np.nan,
                'OOV_words': OOVWords
            }
            # Add the participant's data to the list
            grammaList.append(grammaSJ)

        # Convert the processed data into a DataFrame
        grammaDF = pd.DataFrame(grammaList)

        return grammaDF
