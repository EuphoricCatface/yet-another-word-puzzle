import os.path

DICTIONARY_IS_UPPERCASE = True


class Evaluation:
    # Empty if before loading, None if failed to load
    dict = set()

    @classmethod
    def load(cls):
        print("loading dictionary")
        path: str = ""
        for path_candidate in ["backend/dictionary.txt", "dictionary.txt"]:
            if os.path.isfile(path_candidate):
                path = path_candidate
        if path == "":
            print("Dictionary not found! Evaluation will always return True")
            cls.dict = None
            return

        with open(path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    continue
                if len(line) <= 2:
                    continue
                cls.dict.add(line)
        print(f"Words loaded from dictionary.txt: {len(cls.dict)} words total")
        print("(Words shorter than 3 letters are omitted)")

    def __init__(self):
        pass

    @classmethod
    def eval(cls, word: str):
        if cls.dict is None:
            return True

        if not DICTIONARY_IS_UPPERCASE:
            word = word.lower()
        if not cls.dict:
            cls.load()
        return word in cls.dict

