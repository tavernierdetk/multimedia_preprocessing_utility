from ProcessingComponents.component_base_class import Component
import spacy
from Utility.wiki_matcher import Wikifetcher

class CandidateTextExtractor(Component):
    def __init__(self, file_path, file_name, nlp_model):
        Component.__init__(self,file_path, file_name)
        self.nlp_model = nlp_model
        self.wikifetcher = Wikifetcher(self.info_file['language'])

    def run(self):

        self._load_info_files()
        for info_file in self.info_files:
            ents = nlp(info_file['transcript']['text']).ents
            for ent in ents:
                if ent.label_ == "PER":
                    page = self.wikifetcher.get_wiki_page(ent)
                    print(page)

if __name__ == "__main__":
    file_path = "/Users/alex_root/PycharmProjects/multimedia_preprocessing_utility/MediaFiles"
    file_name = "test_video"

    nlp = spacy.load('fr_core_news_lg')


    candidate_text_extractor = CandidateTextExtractor(file_path, file_name, nlp)
    candidate_text_extractor.run()