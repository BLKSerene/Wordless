def convert_lang(parent, lang):
    # Text -> Code
    if lang[0].isupper():
        return parent.file_langs[lang]
    # Code -> Text
    else:
        for lang_text, lang_code in parent.file_langs.items():
            if lang_code == lang:
                return lang_text

def convert_ext(parent, ext):
    # Text -> Code
    return parent.file_exts[ext].split(' (')[0]

def convert_encoding(parent, encoding, lang = None):
    # Text -> Code
    if encoding.find('(') > -1:
        encoding_code = parent.file_encodings[encoding]
        encoding_lang = encoding.split('(')[0]

        return (encoding_code, encoding_lang)

    # Code -> Text
    else:
        for encoding_text, encoding_code in parent.file_encodings.items():
            if encoding == encoding_code:
                # Distinguish between different languages
                if lang:
                    if encoding_text.find(lang) > -1:
                        return encoding_text
                else:
                    return encoding_text

def fetch_files(self):
    files = [file for file in self.files if file.selected]

    if files == []:
        QMessageBox.warning(self,
                            self.tr('Generation Failed'),
                            self.tr('There are no files being currently selected!'),
                            QMessageBox.Ok)

    return files

def multiple_sorting(item):
    keys = []

    for freq in item[1]:
        keys.append(-freq)
    keys.append(item[0])

    return keys
