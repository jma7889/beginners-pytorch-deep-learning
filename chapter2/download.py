# download.py

import itertools
import os
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import urllib3
from urllib3.util import Retry

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

classes = ["cat", "fish"]
set_types = ["train", "test", "val"]


def download_image(url, klass, data_type):
    basename = os.path.basename(urlparse(url).path)
    filename = "{}/{}/{}".format(data_type, klass, basename)
    if not os.path.exists(filename):
        try:
            timeout = urllib3.util.Timeout(connect=2.0, read=7.0)
            http = urllib3.PoolManager(retries=Retry(connect=1, read=1, redirect=2), timeout=timeout)
            with http.request("GET", url, preload_content=False) as resp, open(filename, "wb") as out_file:
                if resp.status == 200:
                    shutil.copyfileobj(resp, out_file)
                else:
                    print("Error writing {}".format(url))
            resp.release_conn()
        except urllib3.exceptions.MaxRetryError:
            print("Error downloading {}".format(url))


if __name__ == "__main__":
    ROOT_DIR = Path(__file__).parent
    os.chdir(ROOT_DIR)
    if not os.path.exists("images.csv"):
        print("Error: can't find images.csv!")
        sys.exit(0)

    # get args and create output directory
    imagesDF = pd.read_csv("images.csv")

    for set_type, klass in list(itertools.product(set_types, classes)):
        path = "./{}/{}".format(set_type, klass)
        if not os.path.exists(path):
            print("Creating directory {}".format(path))
            os.makedirs(path)

    print("Downloading {} images".format(len(imagesDF)))

    result = [
        download_image(url, klass, data_type)
        for url, klass, data_type in zip(
            imagesDF["url"], imagesDF["class"], imagesDF["type"]
        )
    ]

    missing = 0
    zero = 0
    available = 0
    for url, klass, data_type in zip(imagesDF["url"], imagesDF["class"], imagesDF["type"]):
        basename = os.path.basename(urlparse(url).path)
        filename = Path(data_type) / klass / basename
        if not filename.exists():
            missing += 1
        elif filename.stat().st_size == 0:
            zero += 1
            filename.unlink()
        else:
            available += 1
    print(available, zero, missing)

    sys.exit(0)
