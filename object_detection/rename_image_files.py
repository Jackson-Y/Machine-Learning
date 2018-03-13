# Copyright 2018 CNKI Authors. All Rights Reserved.
#
# Date: 2018-03-13
#================================================================
r"""Rename the image files in the directory.

To run,
    python rename_image_files.py
    python rename_image_files.py your_image_directory

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys

image_dir = 'G:\\program_files\\LabelImg_win_v1.3.0\\image'


def rename_files(image_dir):
	count = 1
	for f in os.listdir(image_dir):
		os.rename(os.path.join(image_dir, f),
			os.path.join(image_dir, "%05d.jpg" % count))
		count += 1


def main():
    path = image_dir
    if len(sys.argv) > 1:
        path = sys.argv[1]
    rename_files(path)


if __name__ == "__main__":
	main()
