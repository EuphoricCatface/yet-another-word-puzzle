class Evaluation:
    dict = set()

    @classmethod
    def load(cls):
        print("loading dictionary")
        with open("backend/dictionary.txt") as f:
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
        if not cls.dict:
            cls.load()
        return word in cls.dict

