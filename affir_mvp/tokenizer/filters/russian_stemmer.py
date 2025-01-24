import re


def get_regions(word):
    vowels = "аеиоуыэюя"

    rv = ""
    r1 = ""
    r2 = ""

    # Find RV
    for i in range(len(word)):
        if word[i] in vowels:
            rv = word[i + 1 :]
            break

    # Find R1
    for i in range(len(word) - 1):
        if word[i] in vowels and word[i + 1] not in vowels:
            r1 = word[i + 2 :]
            break

    # Find R2
    for i in range(len(r1) - 1):
        if r1[i] in vowels and r1[i + 1] not in vowels:
            r2 = r1[i + 2 :]
            break

    return rv, r1, r2


def sort_by_length(arrays):
    # Сортируем каждый массив по длине строк по убыванию
    return [sorted(array, key=len, reverse=True) for array in arrays]


def porter_stem(word):
    word = word.lower()
    word = word.replace("ё", "е")

    # Define endings
    perfective_gerund_1 = ["в", "вши", "вшись"]  # а я
    perfective_gerund_2 = ["ив", "ивши", "ившись", "ыв", "ывши", "ывшись"]
    perfective_gerund = perfective_gerund_1 + perfective_gerund_2

    adjective = [
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

    participle_1 = ["ем", "нн", "вш", "ющ", "щ"]  # а я
    participle_2 = ["ивш", "ывш", "ующ"]
    participle = participle_1 + participle_2

    reflexive = ["ся", "сь"]

    verb_1 = [
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
    ]  # а я
    verb_2 = [
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
    verb = verb_1 + verb_2

    noun = [
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

    superlative = ["ейш", "ейше"]

    derivational = ["ост", "ость"]

    rv, r1, r2 = get_regions(word)

    # Step 1
    ends_with_p_gerund = False
    for ending in sorted(perfective_gerund, key=len, reverse=True):
        if rv.endswith(ending):
            if ending in perfective_gerund_1:
                pattern = rf"(а|я){ending}$"
                if re.search(pattern, rv):
                    word = word[: -len(ending)]
                    rv, r1, r2 = get_regions(word)
                    ends_with_p_gerund = True

            if ending in perfective_gerund_2:
                word = word[: -len(ending)]
                rv, r1, r2 = get_regions(word)
                ends_with_p_gerund = True
            break

    def test_alt_if(word):
        rv, r1, r2 = get_regions(word)

        for ending in sorted(reflexive, key=len, reverse=True):
            if rv.endswith(ending):
                word = word[: -len(ending)]
                rv, r1, r2 = get_regions(word)
                break

        for ending in sorted(adjective, key=len, reverse=True):
            if rv.endswith(ending):
                word = word[: -len(ending)]
                rv, r1, r2 = get_regions(word)

                for participle_ending in sorted(participle, key=len, reverse=True):
                    if rv.endswith(participle_ending):

                        if participle_ending in participle_1:
                            pattern = rf"(а|я){participle_ending}$"
                            if re.search(pattern, rv):
                                word = word[: -len(participle_ending)]
                                rv, r1, r2 = get_regions(word)
                                return word

                        if participle_ending in participle_2:
                            word = word[: -len(participle_ending)]
                            rv, r1, r2 = get_regions(word)
                            return word

                return word

        for ending in sorted(verb, key=len, reverse=True):
            if rv.endswith(ending):
                if ending in verb_1:
                    pattern = rf"(а|я){ending}$"
                    if re.search(pattern, rv):
                        word = word[: -len(ending)]
                        rv, r1, r2 = get_regions(word)
                        return word

                if ending in verb_2:
                    word = word[: -len(ending)]
                    rv, r1, r2 = get_regions(word)
                    return word

        for ending in noun:
            if rv.endswith(ending):
                word = word[: -len(ending)]
                return word
        return word

    if ends_with_p_gerund is False:
        word = test_alt_if(word)
        rv, r1, r2 = get_regions(word)

    # Step 2
    if rv.endswith("и"):
        word = word[:-1]
        rv, r1, r2 = get_regions(word)

    # Step 3
    for ending in sorted(derivational, key=len, reverse=True):
        if r2.endswith(ending):
            word = word[: -len(ending)]
            rv, r1, r2 = get_regions(word)
            break

    # Step 4

    for ending in sorted(superlative, key=len, reverse=True):
        if rv.endswith(ending):
            word = word[: -len(ending)]
            rv, r1, r2 = get_regions(word)
            break
    if rv.endswith("нн"):
        word = word[:-1]

    elif rv.endswith("ь"):
        word = word[:-1]

    return word


def compare_files(voc_file, output_file):
    stop_words = set(
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

    with open(voc_file, "r", encoding="utf-8") as voc:
        voc_words = [line.strip() for line in voc]
    print(f"Number of words: {len(voc_words)}")
    with open(output_file, "r", encoding="utf-8") as out:
        output_words = [line.strip() for line in out]

    mismatched_count = 0
    for voc_word, output_word in zip(voc_words, output_words):
        voc_word = voc_word.replace("ё", "е")
        output_word = output_word.replace("ё", "е")

        if voc_word in stop_words:
            continue
        stemmed_word = porter_stem(voc_word)
        if stemmed_word != output_word:
            print(f"{voc_word} -> {stemmed_word} does not match {output_word}")
            mismatched_count += 1

    return mismatched_count


# Example usage
if __name__ == "__main__":
    voc_file = "voc.txt"
    output_file = "output.txt"

    mismatched_count = compare_files(voc_file, output_file)
    print(f"Number of mismatched words: {mismatched_count}")
