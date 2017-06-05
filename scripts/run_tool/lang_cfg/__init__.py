exec("from " + __name__ + ".langs import LANG_MODULES")

langs_avail = dict()

for lang in LANG_MODULES:
    exec("import " + __name__ + "." + lang)
    lang_name = eval(lang + ".LANG_NAME")
    langs_avail[lang_name] = lang


def create_langunit(language, workdir_base):
    inst_string = __name__ + "." + langs_avail[language]
    inst_string += ".LangUnit("
    inst_string += '"' + workdir_base + '"'
    inst_string += ")"
    return eval(inst_string)

