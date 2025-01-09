import os
import polib
import requests
import time
import json
from dotenv import load_dotenv

load_dotenv()
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

if not DEEPL_API_KEY:
    raise ValueError("DEEPL_API_KEY environment variable not set")

def translate_with_deepl(text, target_lang="ZH", delay=2):
    # request headers
    headers = {
        "Authorization": DEEPL_API_KEY,
        "Content-Type": "application/json",
    }
    data = json.dumps({
        "text": [text],
        "target_lang": target_lang,
    })
    try:
        time.sleep(delay)
        
        response = requests.post(DEEPL_API_URL, data=data, headers=headers)
        print(text + "\n" + response.json()["translations"][0]["text"] + "\n\n" + "-" * 50 + "\n")
        
        response.raise_for_status()
        return response.json()["translations"][0]["text"]
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def process_po_file(input_file, output_file, target_lang="ZH"):
    po = polib.pofile(input_file)
    # Loop through all entries in the po file
    for entry in po:
        if not entry.msgstr:
            # If no translation, do the translation
            translated_text = translate_with_deepl(entry.msgid, target_lang)
            if translated_text:
                entry.msgstr = translated_text
            else:
                pass
        else:
            pass # Skip the entry if already translated
    po.save(output_file)
    print(f"Translation has been done and saved to {output_file}")


if __name__ == "__main__":
    # input_file = "../s25client/external/languages/rttr-zh_CN.po"
    input_file = "rttr-zh_CN.po"
    output_file = "rttr-zh_CN.po"
    target_lang = "ZH"
    process_po_file(input_file, output_file, target_lang)
