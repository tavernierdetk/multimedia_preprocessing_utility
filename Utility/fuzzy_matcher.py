from fuzzywuzzy import fuzz

class FuzzyMatcher:
    def __init__(self, threshold=.8):
        self.threshold = threshold

    def compare(self, verified_string, unverified_string):
        score = fuzz.partial_ratio(verified_string, unverified_string)
        return score




