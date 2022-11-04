import json

from PIL import Image
from pytesseract import pytesseract
from Utility import fuzzy_matcher, utility
import re
from collections import Counter
from ProcessingComponents.component_base_class import Component
from Utility.wiki_matcher import Wikifetcher

class ScreenshootProcessor(Component):
    def __init__(self, speaker_candidates, img_mapping, file_path, file_name, matcher, fuzz_compare_threshold=80):
        Component.__init__(self, file_path, file_name)
        self.speaker_candidates = speaker_candidates
        self.img_mapping = img_mapping

        self.matcher = matcher
        self.fuzz_compare_threshold = fuzz_compare_threshold
        self._update_info_files()
        self.wikifetcher = Wikifetcher(self.info_file[''])

    def run(self):
        for segment in self.segments_dir_list:
            seg_candidates = []
            for ss in utility.get_visible_dir(f'{self.dirs_path}/{segment}/Screenshots'):
                title = self._process_image(f'{self.dirs_path}/{segment}/Screenshots/{ss}')
                if title == {}:
                    continue

                for speaker_candidate in self.speaker_candidates:
                    full_name = f'{title["first_name"]} {title["last_name"]}'
                    score = self.matcher.compare(speaker_candidate, full_name)
                    if score > self.fuzz_compare_threshold:
                        seg_candidates.append(speaker_candidate)
            # print(seg_candidates)
            c = Counter(seg_candidates)
            most_frequent = c.most_common()
            print(most_frequent)
            info = json.load(open(f'{self.dirs_path}/{segment}/{segment}-info.json', 'r'))
            if len(most_frequent) == 0:
                info["speaker"] = "Unknown"
                print(f'Speaker on segment {segment} is unknown')

            if len(most_frequent) == 1:
                info["speaker"] = seg_candidates[0]
                print(f'Speaker on segment {segment} is {seg_candidates[0]}')

            if len(most_frequent) > 1 and most_frequent[0][1] == most_frequent[1][1]:
                info['speaker'] = most_frequent[0][0]
                info['speaker_runner-up'] = most_frequent[1][0]

            if len(most_frequent) > 1 and most_frequent[0][1] > most_frequent[1][1]:
                info['speaker'] = most_frequent[0][0]

            json.dump(info, open(f'{self.dirs_path}/{segment}/{segment}-info.json', 'w'), indent=3)

    def _process_image(self, file_path):
        try:
            im = Image.open(file_path)
        except:
            return {}
        name_and_riding = im.crop(tuple(self.img_mapping["name_and_riding"]))
        party = im.crop(tuple(self.img_mapping["party"]))
        title = im.crop(tuple(self.img_mapping["title"]))
        topic = im.crop(tuple(self.img_mapping["topic"]))

        text_primary = re.split('[\n\r\s=]', pytesseract.image_to_string(name_and_riding)[:-1])
        text_primary_line = list(filter(lambda item: item != '', text_primary))
        title_card = {
             "party": pytesseract.image_to_string(party)[:-1],
             "text_title" : pytesseract.image_to_string(title),
             "text_topic" : pytesseract.image_to_string(topic),
         }
        try:
            if text_primary_line[-2] in ["La", "Les"]:
                text_primary_line[-2] += f' {text_primary_line.pop()}'

            title_card["riding"] = text_primary_line.pop()

            if len(text_primary_line) == 3:
                title_card["last_name"] = ' '.join(text_primary_line[:-2])
                title_card["first_name"] = text_primary_line[0]
            else:
                title_card["last_name"] = text_primary_line[1]
                title_card["first_name"] = text_primary_line[0]
        except:
            return {}
        return title_card


if __name__ == "__main__":
    file_path = "../../MediaFiles"
    img_ref_dir = "../../MediaFiles/ImgRefs"

    file_name = "test_video"
    channel_name = "test_channel"
    program_name = "program_1"

    channel_info = json.load(open(f'JSONFiles/ChannelInfo/{channel_name}.json', 'r'))
    candidate_file_name = f"{channel_info['channel_video_formats'][program_name]['speaker_candidates']['file_name']}"
    speaker_candidates = json.load(open(f"JSONFiles/{candidate_file_name}", 'r'))

    coordinates = channel_info['channel_video_formats'][program_name]["title_card_key_map"]
    video_file_format = '.mov'

    matcher = fuzzy_matcher.FuzzyMatcher()
    processor = ScreenshootProcessor(speaker_candidates,coordinates,file_path,file_name,matcher)
    processor.run()


