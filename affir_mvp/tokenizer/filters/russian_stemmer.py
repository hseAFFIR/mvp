import re


class RussianPorterStemmer:
    def __init__(self):
        self.vowels = "аеиоуыэюя"
        self.stop_words = set(
            [
                "и",
                "в",
                "во",
                "не",
                "что",
                "он",
                "на",
                "я",
                "с",
                "со",
                "как",
                "а",
                "то",
                "все",
                "она",
                "так",
                "его",
                "но",
                "да",
                "ты",
                "к",
                "у",
                "же",
                "вы",
                "за",
                "бы",
                "по",
                "только",
                "ее",
                "мне",
                "было",
                "вот",
                "от",
                "меня",
                "еще",
                "нет",
                "о",
                "из",
                "ему",
                "теперь",
                "когда",
                "даже",
                "ну",
                "вдруг",
                "ли",
                "если",
                "уже",
                "или",
                "ни",
                "быть",
                "был",
                "него",
                "до",
                "вас",
                "нибудь",
                "опять",
                "уж",
                "вам",
                "сказал",
                "ведь",
                "там",
                "потом",
                "себя",
                "ничего",
                "ей",
                "может",
                "они",
                "тут",
                "где",
                "есть",
                "надо",
                "ней",
                "для",
                "мы",
                "тебя",
                "их",
                "чем",
                "была",
                "сам",
                "чтоб",
                "без",
                "будто",
                "человек",
                "чего",
                "раз",
                "тоже",
                "себе",
                "под",
                "жизнь",
                "будет",
                "ж",
                "тогда",
                "кто",
                "этот",
                "говорил",
                "того",
                "потому",
                "этого",
                "какой",
                "совсем",
                "ним",
                "здесь",
                "этом",
                "один",
                "почти",
                "мой",
                "тем",
                "чтобы",
                "нее",
                "кажется",
                "сейчас",
                "были",
                "куда",
                "зачем",
                "сказать",
                "всех",
                "никогда",
                "сегодня",
                "можно",
                "при",
                "наконец",
                "два",
                "об",
                "другой",
                "хоть",
                "после",
                "над",
                "больше",
                "тот",
                "через",
                "эти",
                "нас",
                "про",
                "всего",
                "них",
                "какая",
                "много",
                "разве",
                "сказала",
                "три",
                "эту",
                "моя",
                "впрочем",
                "хорошо",
                "свою",
                "этой",
                "перед",
                "иногда",
                "лучше",
                "чуть",
                "том",
                "нельзя",
                "такой",
                "им",
                "более",
                "всегда",
                "конечно",
                "всю",
                "между",
            ]
        )

        # Endings
        self.perfective_gerund_1 = ["в", "вши", "вшись"]
        self.perfective_gerund_2 = ["ив", "ивши", "ившись", "ыв", "ывши", "ывшись"]
        self.perfective_gerund = self.perfective_gerund_1 + self.perfective_gerund_2

        self.adjective = [
            "ее",
            "ие",
            "ые",
            "ое",
            "ими",
            "ыми",
            "ей",
            "ий",
            "ый",
            "ой",
            "ем",
            "им",
            "ым",
            "ом",
            "его",
            "ого",
            "ему",
            "ому",
            "их",
            "ых",
            "ую",
            "юю",
            "ая",
            "яя",
            "ою",
            "ею",
        ]

        self.participle_1 = ["ем", "нн", "вш", "ющ", "щ"]
        self.participle_2 = ["ивш", "ывш", "ующ"]
        self.participle = self.participle_1 + self.participle_2

        self.reflexive = ["ся", "сь"]

        self.verb_1 = [
            "ла",
            "на",
            "ете",
            "йте",
            "ли",
            "й",
            "л",
            "ем",
            "н",
            "ло",
            "но",
            "ет",
            "ют",
            "ны",
            "ть",
            "ешь",
            "нно",
        ]
        self.verb_2 = [
            "ила",
            "ыла",
            "ена",
            "ейте",
            "уйте",
            "ите",
            "или",
            "ыли",
            "ей",
            "уй",
            "ил",
            "ыл",
            "им",
            "ым",
            "ен",
            "ило",
            "ыло",
            "ено",
            "ят",
            "ует",
            "уют",
            "ит",
            "ыт",
            "ены",
            "ить",
            "ыть",
            "ишь",
            "ую",
            "ю",
        ]
        self.verb = self.verb_1 + self.verb_2

        self.noun = [
            "а",
            "ев",
            "ов",
            "ие",
            "ье",
            "е",
            "иями",
            "ями",
            "ами",
            "еи",
            "ии",
            "и",
            "ией",
            "ей",
            "ой",
            "ий",
            "й",
            "иям",
            "ям",
            "ием",
            "ем",
            "ам",
            "ом",
            "о",
            "у",
            "ах",
            "иях",
            "ях",
            "ы",
            "ь",
            "ию",
            "ью",
            "ю",
            "ия",
            "ья",
            "я",
        ]

        self.superlative = ["ейш", "ейше"]
        self.derivational = ["ост", "ость"]

    def russian_set_regions(self, word):
        rv, r1, r2 = "", "", ""
        for i in range(len(word)):
            if word[i] in self.vowels:
                rv = word[i + 1 :]
                break
        for i in range(len(word) - 1):
            if word[i] in self.vowels and word[i + 1] not in self.vowels:
                r1 = word[i + 2 :]
                break
        for i in range(len(r1) - 1):
            if r1[i] in self.vowels and r1[i + 1] not in self.vowels:
                r2 = r1[i + 2 :]
                break
        return rv, r1, r2

    def russian_stemmer(self, word):
        word = word.lower().replace("ё", "е")
        rv, r1, r2 = self.russian_set_regions(word)

        # Step 1
        word = self.step_1(rv, word)
        rv, r1, r2 = self.russian_set_regions(word)

        # Step 2
        if rv.endswith("и"):
            word = word[:-1]
            rv, r1, r2 = self.russian_set_regions(word)

        # Step 3
        for ending in sorted(self.derivational, key=len, reverse=True):
            if r2.endswith(ending):
                word = word[: -len(ending)]
                rv, r1, r2 = self.russian_set_regions(word)
                break

        # Step 4
        for ending in sorted(self.superlative, key=len, reverse=True):
            if rv.endswith(ending):
                word = word[: -len(ending)]
                rv, r1, r2 = self.russian_set_regions(word)
                break
        if rv.endswith("нн"):
            word = word[:-1]
        elif rv.endswith("ь"):
            word = word[:-1]

        return word

    def step_1(self, rv, word):
        ends_with_p_gerund = False
        for ending in sorted(self.perfective_gerund, key=len, reverse=True):
            if rv.endswith(ending):
                if ending in self.perfective_gerund_1:
                    pattern = rf"(а|я){ending}$"
                    if re.search(pattern, rv):
                        word = word[: -len(ending)]
                        rv, r1, r2 = self.russian_set_regions(word)
                        ends_with_p_gerund = True
                if ending in self.perfective_gerund_2:
                    word = word[: -len(ending)]
                    rv, r1, r2 = self.russian_set_regions(word)
                    ends_with_p_gerund = True
                break
        if not ends_with_p_gerund:
            word = self.step_1_if(word, rv)
        return word

    def step_1_if(self, word, rv):
        rv, r1, r2 = self.russian_set_regions(word)
        for ending in sorted(self.reflexive, key=len, reverse=True):
            if rv.endswith(ending):
                word = word[: -len(ending)]
                rv, r1, r2 = self.russian_set_regions(word)
                break
        for ending in sorted(self.adjective, key=len, reverse=True):
            if rv.endswith(ending):
                word = word[: -len(ending)]
                rv, r1, r2 = self.russian_set_regions(word)
                for participle_ending in sorted(self.participle, key=len, reverse=True):
                    if rv.endswith(participle_ending):
                        if participle_ending in self.participle_1:
                            pattern = rf"(а|я){participle_ending}$"
                            if re.search(pattern, rv):
                                word = word[: -len(participle_ending)]
                                rv, r1, r2 = self.russian_set_regions(word)
                                return word
                        if participle_ending in self.participle_2:
                            word = word[: -len(participle_ending)]
                            rv, r1, r2 = self.russian_set_regions(word)
                            return word
                return word
        for ending in self.verb:
            if rv.endswith(ending):
                if ending in self.verb_1:
                    pattern = rf"(а|я){ending}$"
                    if re.search(pattern, rv):
                        word = word[: -len(ending)]
                        rv, r1, r2 = self.russian_set_regions(word)
                        return word
                if ending in self.verb_2:
                    word = word[: -len(ending)]
                    rv, r1, r2 = self.russian_set_regions(word)
                    return word
        for ending in self.noun:
            if rv.endswith(ending):
                word = word[: -len(ending)]
                return word
        return word

    # для проверки с оригинальным портером с сайта (https://snowballstem.org/demo.html#Russian)
    def russian_compare_files(self, voc_file, output_file):
        with open(voc_file, "r", encoding="utf-8") as voc:
            voc_words = [line.strip() for line in voc]
        print(f"Number of words: {len(voc_words)}")
        with open(output_file, "r", encoding="utf-8") as out:
            output_words = [line.strip() for line in out]

        mismatched_count = 0
        for voc_word, output_word in zip(voc_words, output_words):
            voc_word = voc_word.replace("ё", "е")
            output_word = output_word.replace("ё", "е")

            if voc_word in self.stop_words:
                continue
            stemmed_word = self.russian_stemmer(voc_word)
            if stemmed_word != output_word:
                print(f"{voc_word} -> {stemmed_word} does not match {output_word}")
                mismatched_count += 1

        return mismatched_count


# Example usage
# if __name__ == "__main__":
#     stemmer = RussianPorterStemmer()
#     voc_file = "voc.txt"
#     output_file = "output.txt"
#     mismatched_count = stemmer.russian_compare_files(voc_file, output_file)
#     print(f"Number of mismatched words: {mismatched_count}")
#     print(stemmer.russian_stemmer("сказанный"))
