import json
from PIL import ImageChops, Image
import math, operator
import functools
from Utility import utility


class VideoTransitionIdentificator:
    def __init__(self, file_path, file_name, ref_imgs_dir):
        self.filepath = file_path
        self.file_name = file_name
        self.ref_imgs_dir = ref_imgs_dir
        self._get_ref_imgs()

    def _get_ref_imgs(self):
        imgs = utility.get_visible_dir(self.ref_imgs_dir)
        print(imgs)
        self.imgs_ref = [Image.open(f'{self.ref_imgs_dir}/{path_ref}') for path_ref in imgs]

    def _try_run(self):
        segments = utility.get_visible_dir(f'{self.filepath}/{self.file_name}/Segments')

        for segment in segments:
            segment_path = f'{self.filepath}/{self.file_name}/Segments/{segment}'
            info = json.load(open(f'{segment_path}/{segment}-info.json','r'))

            for ss in utility.get_visible_dir(f'{segment_path}/Screenshots'):
                im2 = Image.open(f'{self.filepath}/{self.file_name}/Segments/{segment}/Screenshots/{ss}')
                for im1 in self.imgs_ref:
                    diff = self._rmsdiff(im1, im2)

                    if diff < 60:
                        info["transition"] = True
                        print(f'{segment} is transition')
                        break
            json.dump(info, open(f'{segment_path}/{segment}-info.json', 'w'), indent=3)

    def _rmsdiff(self, im1, im2):
        "Calculate the root-mean-square difference between two images"

        h = ImageChops.difference(im1, im2).histogram()

        # calculate rms
        return math.sqrt(
            functools.reduce(operator.add,
            map(lambda h, i: h*(i**2), h, range(256))
        ) / (float(im1.size[0]) * im1.size[1]))

if __name__ == "__main__":
    img_ref_dir = "../../MediaFiles/ImgRefs"
    filepath = "../../MediaFiles"
    file_name = 'test_video'

    pattern_matcher = VideoTransitionIdentificator(filepath, file_name, img_ref_dir)
    pattern_matcher.run()
