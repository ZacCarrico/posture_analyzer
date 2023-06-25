import argparse
import os
import time
from main import PoseAnalyzer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="analyze images")
    parser.add_argument("--path", type=str, help="path to image or dir")
    args = parser.parse_args()

    if os.path.isdir(args.path):
        print("keeps running because it's assuming pictures are constantly being added")
        while True:
            files = [
                os.path.join(args.path, f)
                for f in os.listdir(args.path)
                if os.path.isfile(os.path.join(args.path, f))
            ]
            for file in files:
                PoseAnalyzer(file).save_analyzed_image()
            time.sleep(0.1)

    else:
        PoseAnalyzer(args.path).save_analyzed_image()
