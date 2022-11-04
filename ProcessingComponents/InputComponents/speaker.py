from ProcessingComponents.component_base_class import Input
from Utility.fuzzy_matcher import FuzzyMatcher

class Speaker(Input):
    def __init__(self, first_name="", last_name="", title="", qid="", type=""):
        Input.__init__(self)
        self.first_name = first_name
        self.last_name = last_name
        self.title = title,
        self.qid = qid,
        self.type = type

    def to_json(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "title": self.title,
            "qid": self.qid,
            "type": self.type
        }

    def resolve_from_candidate_list(self):
        return

    def resolve_from_wikipedia(self):
        return
