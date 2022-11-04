from ProcessingComponents.component_base_class import Component


class SpeakerPropagator(Component):
    def __init__(self, file_path, file_name):
        Component.__init__(self,file_path, file_name)

    def run(self):
        self._update_info_files()
        self._create_chunks()
        self._write_info_files()

    def _create_chunks(self):
        chunk = []
        for info_file in self.info_files:
            if "transition" in info_file and info_file['transition']:
                self._propagate_speaker_in_chunk(chunk)
                chunk = []
                continue
            chunk.append(info_file)

    def _propagate_speaker_in_chunk(self, chunk):
        speakers = []
        for info_file in chunk:
            if "speaker" not in info_file:
                continue
            if info_file["speaker"] not in speakers:
                speakers.append(info_file["speaker"])

        if len(speakers) == 0:
            return

        if len(speakers) > 1:
            print(f"Warning! Chunk starting with {chunk[0]['segment_name']} has more than one speaker")
            return

        for info_file in chunk:
            info_file["speaker"] = speakers[0]
            return


if __name__ == "__main__":
    file_path = "../../MediaFiles"
    file_name = 'test_video'
    propagator = SpeakerPropagator(file_path, file_name)
    propagator.run()