import re


class RussianPorterStemmer:
    vowels = "\u0430\u0435\u0438\u043e\u0443\u044b\u044d\u044e\u044f"  # аеиоуыэюя
    perfective_gerund = re.compile(
        r"((ив|ивши|ившись|ыв|ывши|ывшись)|((?<=\u0430|\u044f)(в|вши|вшись)))$"
    )
    reflexive = re.compile(r"(с[яь])$")
    adjective = re.compile(
        r"(ее|ие|ые|ое|ими|ыми|ей|ий|ый|ой|ем|им|ым|ом|его|ого|ему|ому|их|ых|ую|юю|ая|яя|ою|ею)$"
    )
    participle = re.compile(r"((ивш|ывш|ующ)|((?<=\u0430|\u044f)(ем|нн|вш|ющ|щ)))$")
    verb = re.compile(
        r"((ила|ыла|ена|ейте|уйте|ите|или|ыли|ей|уй|ил|ыл|им|ым|ен|ило| \
        ыло|ено|ят|ует|уют|ит|ыт|ены|ить|ыть|ишь|ую|ю)|((?<=\u0430|\u044f) \
        (ла|на|ете|йте|ли|й|л|ем|н|ло|но|ет|ют|ны|ть|ешь|нно)))$"
    )
    noun = re.compile(
        r"(а|ев|ов|ие|ье|е|иями|ями|ами|еи|ии|и|ией|ей|ой|ий|й|иям|ям| \
        ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я)$"
    )
    superlative = re.compile(r"(ейш|ейше)$")
    derivational = re.compile(r"(ост|ость)$")
    soft_sign = re.compile(r"[ьъ]$")

    @staticmethod
    def russian_contains_vowel(word):
        return any(char in RussianPorterStemmer.vowels for char in word)

    @staticmethod
    def russian_stemmer(word):
        original_word = word
        word = word.lower()
        word = word.replace("ё", "е")  # хз, надо подумать.

        while True:
            # Step 1: Remove perfective gerund suffix
            m = re.search(RussianPorterStemmer.perfective_gerund, word)
            if m:
                word = word[: m.start()]
                continue

            # Step 2: Remove reflexive suffix
            new_word = re.sub(RussianPorterStemmer.reflexive, "", word)
            if new_word != word:
                word = new_word
                continue

            # Step 3: Remove adjectival, participial, or verbal suffix
            if re.search(RussianPorterStemmer.adjective, word):
                word = re.sub(RussianPorterStemmer.adjective, "", word)
                word = re.sub(RussianPorterStemmer.participle, "", word)
                continue
            elif re.search(RussianPorterStemmer.verb, word):
                word = re.sub(RussianPorterStemmer.verb, "", word)
                continue
            else:
                new_word = re.sub(RussianPorterStemmer.noun, "", word)
                if new_word != word:
                    word = new_word
                    continue

            # Step 4: Remove derivational suffix
            m = re.search(RussianPorterStemmer.derivational, word)
            if m:
                word = word[: m.start()]
                continue

            # Step 5: Remove superlative suffix and soft sign
            new_word = re.sub(RussianPorterStemmer.superlative, "", word)
            new_word = re.sub(RussianPorterStemmer.soft_sign, "", new_word)
            if new_word != word:
                word = new_word
                continue

            break

        # Ensure the result contains at least one vowel
        if not RussianPorterStemmer.russian_contains_vowel(word):
            return re.sub(
                RussianPorterStemmer.soft_sign, "", original_word
            )  # Return the original word without final 'ь' or 'ъ'

        return word
