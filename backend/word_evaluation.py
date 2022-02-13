import os.path


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
        print(f"dictionary loaded: {len(cls.dict)} words total")

    def __init__(self):
        pass

    @classmethod
    def eval(cls, word):
        if cls.dict is None:
            return True
        if not cls.dict:
            cls.load()
        return word in cls.dict

