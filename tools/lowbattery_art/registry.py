DESIGNS = []


def design(name_en, name_de, group):
    def deco(fn):
        DESIGNS.append((fn, name_en, name_de, group))
        return fn
    return deco
