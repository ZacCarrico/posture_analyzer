import numpy as np
from matplotlib import pyplot as plt
from gluoncv import model_zoo, data, utils
from gluoncv.data.transforms.pose import detector_to_simple_pose, heatmap_to_coord
from pathlib import Path

NOSE_IDX = 0
RIGHT_SHOULDER_IDX = 5
LEFT_SHOULDER_IDX = 6
RIGHT_HIP_IDX = 11
LEFT_HIP_IDX = 12
CONFIDENCE_THRESHOLD = 0.15


class PoseAnalyzer:
    def __init__(self, img_path: str):
        self.img_path = img_path

    def save_analyzed_image(self) -> None:
        """Analyzes image and saves it with angle added to img_path"""
        predicted_feature_coords = self.predict_feature_coords()

        # unfortunately this try/except is necessary b/c mxnet.ndarray's can't be compared to None
        try:
            if not predicted_feature_coords:
                return None
        except:
            pass

        idxs = [
            NOSE_IDX,
            RIGHT_SHOULDER_IDX,
            LEFT_SHOULDER_IDX,
            RIGHT_HIP_IDX,
            LEFT_HIP_IDX,
        ]
        confidences = [
            confidence for i, confidence in enumerate(self.confidence[0]) if i in idxs
        ]
        if any(confidence < CONFIDENCE_THRESHOLD for confidence in confidences):
            print(f"confidence < {CONFIDENCE_THRESHOLD}")
            print(confidences)
            return

        utils.viz.plot_keypoints(
            self.img,
            self.pred_coords_mxnet_ndarray,
            self.confidence,
            self.class_IDs,
            self.bounding_boxes,
            self.scores,
            box_thresh=0.5,
            keypoint_thresh=0.2,
        )
        img_path = Path(self.img_path)
        plt.savefig(
            f"analyzed_imgs/{img_path.name.split('.')[0]}_angle{self.calc_nose_shoulders_hips_angle(predicted_feature_coords)}.jpg"
        )
        plt.close()
        img_path.rename(f"analyzed_imgs/{img_path.name}")

    def predict_feature_coords(self) -> np.ndarray:
        """
        Example coordinates with location in the comments
        array([[142.96875,  84.96875],# Nose
            [152.34375,  75.59375],# Right Eye
            [128.90625,  75.59375],# Left Eye
            [175.78125,  89.65625],# Right Ear
            [114.84375,  99.03125],# Left Ear
            [217.96875, 164.65625],# Right Shoulder
            [ 91.40625, 178.71875],# Left Shoulder
            [316.40625, 197.46875],# Right Elblow
            [  9.375  , 232.625  ],# Left Elbow
            [414.84375, 192.78125],# Right Wrist
            [ 44.53125, 244.34375],# Left Wrist
            [199.21875, 366.21875],# Right Hip
            [128.90625, 366.21875],# Left Hip
            [208.59375, 506.84375],# Right Knee
            [124.21875, 506.84375],# Left Knee
            [215.625  , 570.125  ],# Right Ankle
            [121.875  , 570.125  ]],# Left Ankle
        """
        detector = model_zoo.get_model("yolo3_mobilenet1.0_coco", pretrained=True)
        pose_net = model_zoo.get_model("simple_pose_resnet18_v1b", pretrained=True)

        # Note that we can reset the classes of the detector to only include
        # human, so that the NMS process is faster.

        detector.reset_class(["person"], reuse_weights=["person"])
        x, self.img = data.transforms.presets.ssd.load_test(self.img_path, short=512)
        print("Shape of pre-processed image:", x.shape)

        self.class_IDs, self.scores, self.bounding_boxes = detector(x)

        pose_input, upscale_bbox = detector_to_simple_pose(
            self.img, self.class_IDs, self.scores, self.bounding_boxes
        )

        # unfortunately this try/except is necessary b/c mxnet.ndarray's can't be compared to None
        try:
            if not pose_input:
                return
        except:
            predicted_heatmap = pose_net(pose_input)
            self.pred_coords_mxnet_ndarray, self.confidence = heatmap_to_coord(
                predicted_heatmap, upscale_bbox
            )

            # pred_coords is of type mxnet.ndarray.ndarray.NDArray
            return self.pred_coords_mxnet_ndarray.asnumpy()[0]

    @staticmethod
    def calc_angle_at_b(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> int:
        """Calculate the angle at vertex b of a triangle with vertexes a, b, c"""
        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)

        return np.degrees(angle).astype(int)

    @staticmethod
    def calc_nose_shoulders_hips_angle(pred_coords: np.ndarray) -> int:
        """This works best when the camera is at mid-torso height"""
        left_shoulder_coords = pred_coords[LEFT_SHOULDER_IDX]
        right_shoulder_coords = pred_coords[RIGHT_SHOULDER_IDX]
        left_hip_coords = pred_coords[LEFT_HIP_IDX]
        right_hip_coords = pred_coords[RIGHT_HIP_IDX]
        cervical_center = np.array(
            [
                np.mean([left_shoulder_coords[0], right_shoulder_coords[0]]),
                np.mean([left_shoulder_coords[1], right_shoulder_coords[1]]),
            ]
        )
        sacrum_center = np.array(
            [
                np.mean([left_hip_coords[0], right_hip_coords[0]]),
                np.mean([left_hip_coords[1], right_hip_coords[1]]),
            ]
        )

        return PoseAnalyzer.calc_angle_at_b(
            pred_coords[NOSE_IDX], cervical_center, sacrum_center
        )
