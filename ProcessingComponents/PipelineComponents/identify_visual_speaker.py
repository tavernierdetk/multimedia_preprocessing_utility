import cv2
from PIL import Image
import numpy as np


class VisualSpeakerIdentifier:
    def __init__(self, media_layouts, face_reco_path, video_path):
        self.face_reco_path = face_reco_path
        self.media_layouts = media_layouts
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_file_path)
        self.face_cascade = cv2.CascadeClassifier(self.face_reco_path)
        self.faces = []

    def ident_speaker(self, scene):

        return
        # input timestamp of the scene, layout of the media with regions for each candidates
        # start by video activity level contrast to identify the speaking portion

        #level of hierarchy should be
            # => media_layout closed (  check if active speaker square is assigned to a speaker)
            #   => program closed list plus episode added candidates
            #       => media global list

    def _detect_faces(self):
        frame_count = 1
        previous_frame = None

        while True:
            frame_count += 1
            try:
                ret, img_brg = np.array(self.cap.read())
                img_gray = cv2.cvtColor(src=img_brg, code=cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(img_gray, 1.1, 4)
                if frame_count == 30:
                    self.pil_im = img_gray
            except Exception as err:
                print(err)
                break


            for candidate_face in faces:
                flag = 0
                (x, y, w, h) = candidate_face

                for identified_face in self.faces:
                    if self._compare_faces(candidate_face, identified_face['coordinates']):
                        self._extend_face(candidate_face, identified_face['coordinates'])
                        flag = 1
                if flag == 0:
                    self.faces.append({
                        "coordinates" : {
                            "x_low": x,
                            "x_high": x+w,
                            "y_low": y,
                            "y_high": y+h,
                        },
                        "movement_score": 0
                    })

    def _compare_faces(self, candidate_face, identified_face_coord):
            (x, y, w, h) = candidate_face
            mid = ((x + (w/2)),(y + (h/2)))

            if identified_face_coord['x_low'] < mid[0] < identified_face_coord['x_high'] and identified_face_coord['y_low'] < mid[1] < identified_face_coord['y_high']:
                return True
            return False

    def _extend_face(self, candidate_face, identified_face_coord):
        (x, y, w, h) = candidate_face
        if x < identified_face_coord['x_low']:
            identified_face_coord['x_low'] = x

        if x+w > identified_face_coord['x_high']:
            identified_face_coord['x_high'] = x+w

        if y < identified_face_coord['y_low']:
            identified_face_coord['y_low'] = y

        if y + h > identified_face_coord['y_high']:
            identified_face_coord['y_high'] = y + h

    def _compute_movement(self):
        frame_count = 0
        previous_frame = None

        movement_score = 0

        while True:
            frame_count += 1
            # 1. Load image; convert to RGB
            try:
                ret, img_brg = np.array(self.cap.read())

                # print(img_brg)
                # if ((frame_count % 2) == 0) :
                    # 2. Prepare image; grayscale and blur
                prepared_frame = cv2.cvtColor(img_brg, cv2.COLOR_BGR2GRAY)
                prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5, 5), sigmaX=0)

                if (previous_frame is None):
                    # First frame; there is no previous one yet
                    previous_frame = prepared_frame
                    continue

                # calculate difference and update previous frame
                diff_frame = cv2.absdiff(src1=previous_frame, src2=prepared_frame)
                previous_frame = prepared_frame

                # 4. Dilute the image a bit to make differences more seeable; more suitable for contour detection
                kernel = np.ones((5, 5))
                diff_frame = cv2.dilate(diff_frame, kernel, 1)

                # 5. Only take different areas that are different enough (>20 / 255)
                thresh_frame = cv2.threshold(src=diff_frame, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[1]

                contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    if cv2.contourArea(contour) < 50:
                        # too small: skip!
                        continue
                    (x, y, w, h) = cv2.boundingRect(contour)
                    contour_mid = ((x + (w / 2)), (y + (h / 2)))
                    for face in self.faces:
                        coord = face['coordinates']
                        if coord['x_low'] < contour_mid[0] < coord['x_high'] and coord['y_low'] < contour_mid[1] < coord['y_high']:
                            face["movement_score"] += w*h
                    # cv2.rectangle(img=img_gray, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=2)


                # cv2.imshow('Motion detector', img_rgb)
            except Exception as e:
                break

    def _generate_screenshot(self):
        self.faces.sort(key=lambda x: x["movement_score"], reverse=True)
        coordinates = self.faces[0]['coordinates']

        # im = self.cap.ImageGrab(bbox=(coordinates['x_low'],coordinates['x_high'],coordinates['y_low'],coordinates['y_high']))


        cv2.imshow('image', self.pil_im)


if __name__ == "__main__":
    print("Testing visual speaker ID")
    video_file_path = "/Users/alex_root/PycharmProjects/multimedia_preprocessing_utility/MediaFiles/Streams/RDI-TV-Q3456752/telejournal/RDI-TV-Q3456752_telejournal_2022-11-03-1512-1522/RDI-TV-Q3456752_telejournal_2022-11-03-1512-1522-0.mp4"
    face_reco_path= "/Users/alex_root/PycharmProjects/multimedia_preprocessing_utility/JSONFiles/haarcascade_frontalface_default.xml"

    speaker_ider = VisualSpeakerIdentifier([], face_reco_path, video_file_path)
    speaker_ider._detect_faces()

    # speaker_ider.faces = [
    #     {'coordinates': {'x_low': 176, 'x_high': 301, 'y_low': 58, 'y_high': 184}, 'movement_score': 0},
    #     {'coordinates': {'x_low': 608, 'x_high': 730, 'y_low': 67, 'y_high': 190}, 'movement_score': 0},
    #     {'coordinates': {'x_low': 246, 'x_high': 623, 'y_low': 23, 'y_high': 360}, 'movement_score': 0},
    #     {'coordinates': {'x_low': 772, 'x_high': 828, 'y_low': 327, 'y_high': 384}, 'movement_score': 0},
    #     {'coordinates': {'x_low': 357, 'x_high': 511, 'y_low': 184, 'y_high': 360}, 'movement_score': 0},
    #     {'coordinates': {'x_low': 268, 'x_high': 325, 'y_low': 277, 'y_high': 338}, 'movement_score': 0},
    #     {'coordinates': {'x_low': 271, 'x_high': 336, 'y_low': 193, 'y_high': 258}, 'movement_score': 0}
    # ]
    speaker_ider._compute_movement()

    speaker_ider._generate_screenshot()