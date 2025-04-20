from dotenv import load_dotenv
import deepl
import os
load_dotenv()

deepl_api_key = os.getenv('DEEPL_API_KEY')


def translate_to_english_deepl(text, target_language='AR'):

    return text
    """
    Translate using DeepL API (requires authentication key)
    """
    try:
        translator = deepl.Translator(deepl_api_key)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except Exception as e:
        print(f"DeepL translation failed: {e}")
        return None

if __name__ == "__main__":
    print(translate_to_english_deepl("https://github.com/Wouze/csc281-project, this is my website"))
