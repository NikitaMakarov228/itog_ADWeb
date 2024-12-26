from translate import Translator


def translate_word(word, src_lang="ru", dest_lang="en") -> str:
    translator = Translator(from_lang=src_lang, to_lang=dest_lang)

    if len(word) > 100:
        answer = []
        arr = word.split(".")
        for a in arr:
            translation = translator.translate(a)
            answer.append(translation)
        return ". ".join(answer)
    try:
        translation = translator.translate(word)
        return translation.replace(".", "")
    except Exception as e:
        return f"Error: {e}"
