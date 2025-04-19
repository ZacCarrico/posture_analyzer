import os
import gc
import time
from main import PoseAnalyzer


if __name__ == "__main__":
    dir = "non_analyzed_imgs"

    if os.path.isdir(dir):
        print("keeps running because it's assuming pictures are constantly being added")
        while True:
            files = [
                os.path.join(dir, f)
                for f in os.listdir(dir)
                if os.path.isfile(os.path.join(dir, f))
            ]
            for file in files:
                pa = PoseAnalyzer(file)
                pa.save_analyzed_image()
                del pa
                gc.collect()
            time.sleep(0.1)

    else:
        PoseAnalyzer(dir).save_analyzed_image()
