#TODO
# generate summary with either fixed lenght per session or proportional amount,
# and include in overall media config_file
import spacy
from spacy.lang.fr.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest
from ProcessingComponents.component_base_class import Component
from Utility import utility
import json

class TextSummarizer(object):
    def __init__(self, nlp_model, n_most_sents=1):
        self.nlp = nlp_model
        self.summary = ''
        self.n_most_sents = n_most_sents

    def summarize(self, text):
        self.doc = self.nlp(text)
        self._find_keywords()
        self._compute_word_frequency()
        self._compute_sent_strenght()
        self._select_n_most_important_sents()
        return self.summary

    def _select_n_most_important_sents(self):
        self.summarized_sentences = nlargest(self.n_most_sents, self.sent_strength, key=self.sent_strength.get)
        final_sentences = [ w.text for w in self.summarized_sentences ]
        self.summary = ' '.join(final_sentences)


    def _compute_sent_strenght(self):
        self.sent_strength={}
        for sent in self.doc.sents:
            for word in sent:
                if word.text in self.freq_word.keys():
                    if sent in self.sent_strength.keys():
                        self.sent_strength[sent]+=self.freq_word[word.text]
                    else:
                        self.sent_strength[sent]=self.freq_word[word.text]

    def _compute_word_frequency(self):
        self.freq_word = Counter(self.keywords)
        max_freq = Counter(self.keywords).most_common(1)[0][1]
        for word in self.freq_word.keys():
            self.freq_word[word] = (self.freq_word[word]/max_freq)

    def _find_keywords(self):
        self.keywords = []
        stopwords = list(STOP_WORDS)
        pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
        for token in self.doc:
            if(token.text in stopwords or token.text in punctuation):
                continue
            if(token.pos_ in pos_tag):
                self.keywords.append(token.text)

class MediaSummarizer(Component):
    def __init__(self, file_path, file_name, text_summarizer):
        Component.__init__(self, file_path, file_name)
        self.text_summarizer = text_summarizer

    def _try_run(self):
        current_speaker = ""
        for info_file in self.info_files:
            if 'transcript' in info_file and "text" in info_file['transcript']:
                if "speaker" in info_file:
                    if info_file['speaker'] != current_speaker:
                        current_speaker = info_file['speaker']
                        print(f"------{info_file['speaker']}-----")
                print(info_file['transcript']['text'])

            # if "speaker" not in info_file:
            #     current_speaker = "Unknown speaker"
            #     print('\n\n\n')
            #     print(f"-----{current_speaker}-----")
            #     if 'transcript' in info_file and "text" in info_file['transcript']:
            #         print(info_file['transcript']['text'])
            #     continue
            # if info_file["speaker"] != current_speaker:
            #     current_speaker = info_file["speaker"]
            #     print('\n\n\n')
            #     print(f"-----{current_speaker}-----")


if __name__ == '__main__':
    nlp = spacy.load('fr_core_news_lg')


    summarizer = TextSummarizer(nlp)
    # print(summarizer.summarize(text))

    filepath = "../../MediaFiles"
    file_name = 'test_video'
    media_summarizer = MediaSummarizer(filepath, file_name, summarizer)
    media_summarizer.run()