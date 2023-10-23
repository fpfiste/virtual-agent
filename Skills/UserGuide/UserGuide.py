

class UserGuide():
    def __init__(self, config):
        self.config = config

    def get_skill_doc_strings(self):
        docstrings = [value.__doc__ for key, value in self.config.INTENT_SKILL_DICT.items()]
        return docstrings



