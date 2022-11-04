import os.path

from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.silence import detect_nonsilent
import json
from ProcessingComponents.component_base_class import Component

class AudioSegmenter(Component):
    def __init__(self, file_path, file_name, file_format=".mp3", silence_duration=500, silence_threshold=-48, first_component=True):
        Component.__init__(self,file_path, file_name)
        self.silence_duration = silence_duration
        self.silence_threshold = silence_threshold
        self.file_format = file_format
        self.version = "0.1"
        self.component_name = "AudioSegmenter"

        #TODO create workflow for first_component=False

    def _try_run(self):
        self._load_mp3()
        self._find_segments()
        self._find_chunks()
        self._create_folders()
        self._delete_objects()

    def _delete_objects(self):
        del self.audio_file
        return

    def create_segment(self, start_time, end_time, dest_path):
        self._load_mp3()
        self.audio_file[start_time:end_time].export(
                f"{dest_path}-audio.mp3",
                bitrate = "192k",
                format = "mp3"
            )

    def _load_video_config(self, config):
        return

    def _load_mp3(self):
        self.audio_file = AudioSegment.from_mp3(os.path.join(self.file_path,f'{self.file_name}/{self.file_name}{self.file_format}'))

    def _find_segments(self):
        self.segments = detect_nonsilent(
            self.audio_file,
            min_silence_len=self.silence_duration,
            silence_thresh=self.silence_threshold
                                    )
    def _find_chunks(self):
        self.chunks = split_on_silence(
            # Use the loaded audio.
            self.audio_file,
            # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
            min_silence_len = self.silence_duration,
            # Consider a chunk silent if it's quieter than -16 dBFS.
            # (You may want to adjust this parameter.)
            silence_thresh = self.silence_threshold
        )

    def _create_folders(self):
        total_len = 0
        for i, chunk in enumerate(self.chunks):
            total_len += chunk.duration_seconds

            # Export the audio chunk with new bitrate.
            print(f"Exporting Segment {i}.mp3.")

            segment_name = f'{self.file_name}-{str(i).zfill(4)}'

            os.mkdir(f'{self.file_path}/{self.file_name}/Segments/{segment_name}')
            chunk.export(
                f"{self.file_path}/{self.file_name}/Segments/{segment_name}/{segment_name}-audio.mp3",
                bitrate = "192k",
                format = "mp3"
            )
            segment_info = {
                "segment_start": self.segments[i][0],
                "segment_end": self.segments[i][1],
                "segment_name": segment_name
            }
            json.dump(segment_info, open(f"{self.file_path}/{self.file_name}/Segments/{segment_name}/{segment_name}-info.json", 'w'), indent=3)



if __name__ == "__main__":
        filepath = "../../MediaFiles"
        file_name = '20211005_CH_130451'
        file_format = '.mp3'
        print("loading_segmenter")
        segmenter = AudioSegmenter(filepath,file_name,file_format)

        print('creating_segment_one')
        segmenter.create_segment(0,10000,"test")

        print('creating_segment_two')
        segmenter.create_segment(0,10000,"test-2")