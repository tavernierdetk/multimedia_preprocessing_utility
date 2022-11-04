import json
from Utility import utility


class Transcripter:
    def __init__(self, file_path, file_name, model):
        self.model = model
        self.file_path = file_path
        self.file_name = file_name
        self.segments_dir_list = self._get_visible_dir()
        self.dirs_path = f'{self.file_path}/{self.file_name}/Segments'
        self._get_info_files()

    def _get_visible_dir(self):
        return utility.get_visible_dir(f'{self.file_path}/{self.file_name}/Segments')

    def _get_info_files(self):
        self.info_files = []
        for segment in self.segments_dir_list:
            segment_path = f'{self.file_path}/{self.file_name}/Segments/{segment}'
            self.info_files.append(
                json.load(open(f'{segment_path}/{segment}-info.json', 'r'))
            )

    def run(self, range_start=None, range_end=None):
        for info_file in self.info_files:
            print(f'Processing segment {info_file["segment_name"]}')
            transcript = self.model.transcribe(f'{self.dirs_path}/{info_file["segment_name"]}/{info_file["segment_name"]}-audio.mp3')
            info_file['transcript'] = transcript
            json.dump(info_file, open(f"{self.dirs_path}/{info_file['segment_name']}/{info_file['segment_name']}-info.json", 'w'), indent=3)
