"""
В нескольких функциях реализован английский стеммер по алгоритму Porter2.
:param word: Слово в низком регистре на английском языке без лишних знаков.
:return: Обрезанное строчное слово на английском языке.
"""
import re

class Stemmer:
    def __init__(self):
        # Define vowels, english_doubles, valid li-endings and exceptions
        self.english_vowels = 'aeiouy'
        self.english_doubles = ['bb', 'dd', 'ff', 'gg', 'mm', 'nn', 'pp', 'rr', 'tt']
        self.english_valid_li_endings = 'cdeghkmnrt'
        self.english_exceptions1 = {'skis':'ski',
                                   'skies':'sky',
                                   'dying':'die',
                                   'lying':'lie',
                                   'tying':'tie',
                                   'idly':'idl',
                                   'gently':'gentl',
                                   'ugly':'ugli',
                                   'early':'earli',
                                   'only':'onli',
                                   'singly':'singl',
                                   'sky':'sky',
                                   'news':'news',
                                   'howe':'howe',
                                   'atlas':'atlas',
                                   'cosmos':'cosmos',
                                   'bias':'bias',
                                   'andes':'andes'}
        self.english_exceptions2 = ['inning',
                                    'outing',
                                    'herring',
                                    'canning',
                                    'earring',
                                    'proceed',
                                    'exceed',
                                    'succeed']


    def english_set_regions(self, word):
        R1 = ''
        R2 = ''
        for i in range(1, len(word)):
            if word[i] not in self.english_vowels and word[i-1] in self.english_vowels:
                R1 = word[i+1:]
                break
        if word.startswith('commun'):
            R1 = word[6:]
        if word.startswith('arsen') or word.startswith('gener'):
            R1 = word[5:]
        if R1:
            for i in range(1, len(R1)):
                if R1[i] not in self.english_vowels and R1[i-1] in self.english_vowels:
                    R2 = R1[i+1:]
                    break
        return R1, R2
    
    def english_replace_suffixes(self, word, R1):
        word = re.sub(r"('s|'s')$", '', word)  # Step 0
        R1, R2 = self.english_set_regions(word)
        word = re.sub(r"sses$", 'ss', word)  # Step 1a
        R1, R2 = self.english_set_regions(word)
        word = re.sub(r"ied$|ies$", lambda m: 'i' if len(word[:-3]) > 1 else 'ie', word)  # Step 1a
        R1, R2 = self.english_set_regions(word)
        if word.endswith('s') and not (word.endswith('us') or word.endswith('ss')):
            preceding = word[:-1]
            if any(vowel in preceding[:-1] for vowel in self.english_vowels):
                word = word[:-1]
                R1, R2 = self.english_set_regions(word)

        # Second exceptions after step 1a
        if word in self.english_exceptions2:
            return word
        
        suffixes = ['eedly','eed']
        for suffix in suffixes:
            if word.endswith(suffix):
                if suffix in R1:
                    word = re.sub(r"(eedly|eed)$", 'ee', word)
                    R1, R2 = self.english_set_regions(word)
                if len(word) > 2 and word[-1] in ['y', 'Y'] and word[-2] not in self.english_vowels: # Step 1c required here since it is unreachable otherwise
                    word = word[:-1] + 'i'
                return word
        suffixes = ['edly', 'ingly', 'ing', 'ed']
        for suffix in suffixes:
            if word.endswith(suffix):
                if any(vowel in word[:-len(suffix)] for vowel in self.english_vowels):
                    word = re.sub(r"(ed|edly|ing|ingly)$", '', word)
                    R1, R2 = self.english_set_regions(word)
                    # Post-processing after deletion
                    if len(word) < 3:
                        syllable = word
                    else:
                        syllable = word[-3:]
                    if word.endswith(('at', 'bl', 'iz')):
                        word += 'e'  
                    elif len(word) > 2 and word[-2:] in self.english_doubles:
                        if word[:-2] not in "aeo":
                            word = word[:-1]
                    elif len(word) > 1 and word[-2:] not in self.english_doubles and self.english_is_short(syllable, R1):
                        word += 'e'
                    break
        if len(word) > 2 and word[-1] in ['y', 'Y'] and word[-2] not in self.english_vowels:
            word = word[:-1] + 'i'
        
        return word

    def english_is_short(self, word, R1):
        return self.english_is_short_syllable(word) is not False and R1 == ''

    def english_is_short_syllable(self, word):
        if len(word) == 2 and word[0] in self.english_vowels and word[1] not in self.english_vowels:
            return True
        if len(word) < 3:
            return False
        if (
            word[-3] not in self.english_vowels and  # Non-vowel before
            word[-2] in self.english_vowels and  # Vowel
            word[-1] not in self.english_vowels and word[-1] not in ['w', 'x', 'Y']  # Non-vowel, not 'w', 'x', or 'Y'
        ):
            return True
        return False
    
    def step2(self, word, R1):
        if R1:
            suffixes = [
            ("ational", "ate"),
            ("tional", "tion"),
            ("enci", "ence"),
            ("anci", "ance"),
            ("abli", "able"),
            ("entli", "ent"),
            ("izer", "ize"),
            ("ization", "ize"),
            ("ation", "ate"),
            ("ator", "ate"),
            ("alism", "al"),
            ("aliti", "al"),
            ("alli", "al"),
            ("fulness", "ful"),
            ("ousli", "ous"),
            ("ousness", "ous"),
            ("iveness", "ive"),
            ("iviti", "ive"),
            ("biliti", "ble"),
            ("bli", "ble"),
            ("ogi", "og"),
            ("fulli", "ful"),
            ("lessli", "less"),
            ("li", "")  # Delete if preceded by a valid li-ending
            ]
            for suffix, replacement in suffixes:
                if word.endswith(suffix):
                    if word[len(word) - len(suffix):] in R1:
                        if suffix == "ogi" and len(word) > 3 and word[-4] == 'l':
                            word = word[:-len(suffix)] + replacement
                        elif suffix == "li" and len(word) > 2 and word[-3] not in self.english_valid_li_endings:
                            break
                        else:
                            word = word[:-len(suffix)] + replacement
                        break  # Stop after the first valid suffix replacement
                    break
        return word

    def step3(self, word, R1, R2):
        if R1:
            suffixes = [
                ("ational", "ate"),
                ("tional", "tion"),
                ("alize", "al"),
                ("icate", "ic"),
                ("iciti", "ic"),
                ("ical", "ic"),
                ("ful", ""),
                ("ness", ""),
                ("ative", ""),
            ]
            for suffix, replacement in suffixes:
                if word.endswith(suffix):
                    if word[len(word) - len(suffix):] in R1:
                        if word.endswith("ative"):
                            if suffix in R2:
                                word = word[:-len(suffix)] + replacement
                            break
                        word = word[:-len(suffix)] + replacement
                        break
                    break
        return word

    def step4(self, word, R2):
        suffixes = [
            "al", "ance", "ence", "er", "ic", "able", "ible", "ant", 
            "ement", "ment", "ent", "ism", "ate", "iti", "ous", "ive", "ize", "ion"
        ]
        for suffix in suffixes:
            if word.endswith(suffix):
                if suffix in R2:
                    if word.endswith("ion") and len(word) > 3 and word[-4] in ('s', 't'):
                        word = word[:-3]
                    elif not word.endswith("ion"):
                        word = word[:-len(suffix)]
                    break
                break
        return word

    def step5(self, word, R1, R2):
        # Flags so there's no accidental trimming (ex. versaille => versaill => versail shouldn't happen)
        e_flag = False
        l_flag = False
        if word.endswith("e"):
            e_flag = True
        elif word.endswith("l"):
            l_flag = True
            
        if e_flag:
            if word[-1] in R2: 
                word = word[:-1]
                R1, R2 = self.english_set_regions(word)
            elif word[-1] in R1 and not self.english_is_short_syllable(word[:-1]):  
                word = word[:-1]
                R1, R2 = self.english_set_regions(word)
        if l_flag and len(word) > 1 and word[-2] == 'l': 
            if word[-1] in R2:
                word = word[:-1]        
        return word

    def english_stemmer(self, word: str) -> str:
        # Follows the Porter2 algorithm with all provided exceptions
        if word in self.english_exceptions1:
            return self.english_exceptions1[word]

        if word and word[0] == 'y':
            word = 'Y' + word[1:]
    
        word = ''.join('Y' if i > 0 and word[i] == 'y' and word[i-1] in self.english_vowels else c
                       for i, c in enumerate(word))
        
        
        R1, R2 = self.english_set_regions(word)
        
        word = self.english_replace_suffixes(word, R1)
        R1, R2 = self.english_set_regions(word)
        word = self.step2(word, R1)
        R1, R2 = self.english_set_regions(word)
        word = self.step3(word, R1, R2)
        R1, R2 = self.english_set_regions(word)
        word = self.step4(word, R2)
        R1, R2 = self.english_set_regions(word)
        word = self.step5(word, R1, R2)
        return word.lower()