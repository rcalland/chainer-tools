from __future__ import print_function

import argparse
import os

import json
from file_utils import save_json
#from skimage import io
#import cv2
import numpy as np
from PIL import Image

def get_stats(filename):
    #img = cv2.imread(filename).astype(np.float32)
    img = Image.open(filename)
    img = np.asarray(img, dtype="float32")
    return np.mean(img, axis=(0, 1)), img.std()

def sample_mean(filename):
    with open(filename, "r") as f:
        muarray, sigmaarray = zip(*[get_stats(x.split(" ")[0]) for x in f])
        avg_mu = np.mean(muarray)
        print(avg_mu)
        #avg_sigma = np.mean(sigmaarray)
        return avg_mu

def sample_mean_3ch(filename):
    mean = np.zeros((3,), dtype=np.float64)
    n = 0
    with open(filename, "r") as f:
        for x in f:
            #image = cv2.imread(x.split(" ")[0]).astype(np.float32)
            image = Image.open(x.split(" ")[0])
            image = np.asarray(image, dtype="float32")
            m = np.mean(image, axis=(0, 1))
            mean += m
            n += 1
    mean /= n
    print(mean)
    return mean / 255.0

def calc_mean(_file):
    print("processing annotation file \"{}\"".format(_file))
    #config = load_config(config_file)

    # look for these datasets in the config file.
    # NOTE: if you add more, make sure there is an underscore, as that is how the new name is added
    #dataset_types = ["train_annotation", "validation_annotation", "test_annotation"]

    config = {}

    # if the dataset exists, calculate the mean
    #for dataset in dataset_types:
    #    if dataset in config:
    #print("- Calculating mean for dataset \"{}\"...".format(dataset))
    mean = sample_mean_3ch(_file)
    config["file"] = _file
    config["mean"] = list(mean)
    #newname = "{}_mean".format(dataset.split("_")[0])
    #config[newname] = list(mean)

    filename = "{}.json".format(os.path.splitext(_file)[0])
    save_json(filename, config)
    print("Wrote file: {}".format(filename))

def main(args):

    # this is a list of configs, you could add more
    #config_files = ["../config/datasets/refined_6000perclass.json"]
    #config_files = ["../config/datasets/refined.json"]

    for i in args.annotation_files:
        calc_mean(i)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("annotation_files", nargs="+", type=str)
    args = parser.parse_args()
    main(args)
