from Utility import utility
import json
import datetime

class Component:
    def __init__(self, file_path, file_name):
        self.file_path = file_path
        self.file_name = file_name
        self.segments_dir_list = self._get_visible_dir()
        self.dirs_path = f'{self.file_path}/{self.file_name}/Segments'
        self._load_info_files()

    def _get_visible_dir(self):
        return utility.get_visible_dir(f'{self.file_path}/{self.file_name}/Segments')

    def _load_info_files(self):
        self.info_file = json.load(open(f'{self.file_path}/{self.file_name}/{self.file_name}-main_info.json','rb'))
        self.info_files = []
        for segment in self.segments_dir_list:
            segment_path = f'{self.file_path}/{self.file_name}/Segments/{segment}'
            self.info_files.append(
                json.load(open(f'{segment_path}/{segment}-info.json', 'r'))
            )

    def _update_info_file(self, component_name, component_version, error=None):
        self.info_file['process_log'].append({
            "component": component_name,
            "version": component_version,
            "time": datetime.datetime.now().isoformat(),
            "status": "success" if error == None else "failure",
            "error_code": error.__str__()
        })
        json.dump(self.info_file, open(f'{self.file_path}/{self.file_name}/{self.file_name}-main_info.json','w'), indent=3)

    def _write_info_files(self):
        for info_file in self.info_files:
            segment_path = f'{self.file_path}/{self.file_name}/Segments/{info_file["segment_name"]}'
            info_file_path = f'{segment_path}/{info_file["segment_name"]}-info.json'
            json.dump(info_file, open(info_file_path, 'w'), indent=3)

    def _start_counter(self):
        print(f"Starting {self.component_name}")
        self.start_time = datetime.datetime.now()

    def _stop_counter(self):
        now = datetime.datetime.now()
        time_taken = now - self.start_time
        print(f"Finished at {now}, in {time_taken}")

    def run(self):
        try:
            self._start_counter()
            self._try_run()
            self._update_info_file(self.component_name, self.version)
            self._stop_counter()
        except Exception as error:
            error.__str__()
            self._update_info_file(self.component_name, self.version, error=error)

class Input:
    def __init__(self):
        return
