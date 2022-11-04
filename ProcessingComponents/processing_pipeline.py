import datetime
import whisper
import json
from Utility.fuzzy_matcher import FuzzyMatcher
import os

from ProcessingComponents.component_base_class import Component
from ProcessingComponents.PipelineComponents import trancript_extractor
from ProcessingComponents.PipelineComponents.title_card_preprocessing import ScreenshootProcessor
from ProcessingComponents.PipelineComponents.speaker_continuation import SpeakerPropagator
from ProcessingComponents.PipelineComponents.audio_segmenter import AudioSegmenter
from ProcessingComponents.PipelineComponents.video_segmenter import VideoSegmenter
from ProcessingComponents.PipelineComponents.screen_shot_generator import ScreenShotsGrabber
from ProcessingComponents.PipelineComponents.video_pattern_identificator import VideoTransitionIdentificator
from ProcessingComponents.PipelineComponents.pipeline_initializer import Initializer


# transcription_model = whisper.load_model("medium")

file_path = "/Users/alex_root/PycharmProjects/multimedia_preprocessing_utility/MediaFiles"
file_name = "test_video_2"


        # os.mkdir(f'{file_path}/{file_name}/Segments')

class PipelineProcessor(Component):
    def __init__(
            self,
            file_path,
            file_name,
            channel_info_path="/Users/alex_root/PycharmProjects/multimedia_preprocessing_utility/JSONFiles/ChannelInfo",
            img_ref_path=f"/Users/alex_root/PycharmProjects/multimedia_preprocessing_utility/MediaFiles/ImgRefs"
    ):
        Component.__init__(self,file_path, file_name)
        self.channel_name = self.info_file['channel_name']
        self.program_name = self.info_file['program_name']
        self.channel_info_path = channel_info_path
        self.img_ref_path = img_ref_path
        self.channel_info = json.load(open(f'{self.channel_info_path}/{self.channel_name}.json', 'r'))
        self.video_file_format = self.info_file['file_specs']['extension']
        self.pipeline = self.channel_info['programs'][self.program_name]['components_pipeline']
        self.version = "0.1"
        self.component_name = "Processor"

        self.pipeline_lookup_table = {
            "initializer": {
                "loader": self._load_initializer,
                "runner": self._run_initializer
            },
            "silence_segmenter": {
                "loader": self._load_silence_segmenter,
                "runner": self._run_silence_segmenter
            },
            "video_segmenter": {
                "loader": self._load_video_segmenter,
                "runner": self._run_video_segmenter
            },
            "screenshot_generator": {
                "loader": self._load_screen_shot_generator,
                "runner": self._run_screen_shot_generator
            },
        }

        self._load_components()

    def _load_components(self):
        for index, component in enumerate(self.pipeline):
            if index == 1:
                self.pipeline_lookup_table[component['component_name']]["loader"](first_component=True)
            else:
                self.pipeline_lookup_table[component['component_name']]["loader"](first_component=False)

    def _try_run(self):
        for component in self.pipeline:
            self.pipeline_lookup_table[component['component_name']]["runner"]()

    def _load_initializer(self, first_component=False):
        self.initializer = Initializer(self.file_path, self.file_name, self.info_file, first_component=first_component)
        return

    def _run_initializer(self):
        self.initializer.run()
        del self.initializer

    def _load_silence_segmenter(self, first_component=False):
        self.silence_segmenter = AudioSegmenter(self.file_path, self.file_name, first_component=first_component)

    def _run_silence_segmenter(self):
        self.silence_segmenter.run()
        del self.silence_segmenter

    def _load_video_segmenter(self, first_component=False):
        self.video_segmenter = VideoSegmenter(self.file_path, self.file_name, self.video_file_format, first_component=first_component)

    def _run_video_segmenter(self):
        self.video_segmenter.run()
        del self.video_segmenter

    def _load_screen_shot_generator(self, first_component=False):
        self.screen_shot_generator = ScreenShotsGrabber(self.file_path, self.file_name, self.video_file_format, first_component=first_component)

    def _run_screen_shot_generator(self):
        self.screen_shot_generator.run()
        del self.screen_shot_generator



processor = PipelineProcessor(file_path, file_name)
processor.run()


#
# print('Generating screenshots')
# ss_generator = ScreenShotsGrabber(file_path, file_name, video_file_format)
# ss_generator.run()
# print('Screenshots generated')
# print(datetime.datetime.now() - last)
# last =datetime.datetime.now()
# #
# pattern_matcher = VideoTransitionIdentificator(file_path, file_name, img_ref_dir)
# pattern_matcher.run()
# print(datetime.datetime.now() - last)
# last =datetime.datetime.now()
#
# print("Starting transcription")
# t_extractor = trancript_extractor.Transcripter(file_path, file_name, transcription_model)
# t_extractor.run()
#
# print("Processing speakers")
# matcher = FuzzyMatcher()
# processor = ScreenshootProcessor(speaker_candidates,coordinates,file_path,file_name, matcher)
# processor.run()
# print("Speakers processed")
# print(datetime.datetime.now() - last)
# last = datetime.datetime.now()
#
# print("Propagating speakers")
# propagator = SpeakerPropagator(file_path, file_name)
# propagator.run()
# print("Speakers propagated")
#
# print(f"Pipeline competed on video {file_name}")
