# Copyright 2018 CNKI Authors. All Rights Reserved.
#
# Date: 2018-03-13
#================================================================
# coding: utf-8
r""" Tensorflow object detection in X minutes.

To run,
    python object_detection_tutorial.py

"""
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
  
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

#%matplotlib inline
import sys
sys.path.insert(0, '/home/moxiao/code/models/research')

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection'

PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
  
NUM_CLASSES = 90


#opener = urllib.request.URLopener()  
#opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)  
#tar_file = tarfile.open(MODEL_FILE)  
#for file in tar_file.getmembers():  
#    file_name = os.path.basename(file.name)  
#    if 'frozen_inference_graph.pb' in file_name:  
#        tar_file.extract(file, os.getcwd())  


detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

PATH_TO_TEST_IMAGES_DIR = 'test_images'  
TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, '{}.jpg'.format(i)) for i in range(1, 3) ]
IMAGE_SIZE = (12, 8)

with detection_graph.as_default():
  
  with tf.Session(graph=detection_graph) as sess:
    for image_path in TEST_IMAGE_PATHS:
      image = Image.open(image_path)
      # 这个array在之后会被用来准备为图片加上框和标签
      image_np = load_image_into_numpy_array(image)
      # 扩展维度，应为模型期待: [1, None, None, 3]
      image_np_expanded = np.expand_dims(image_np, axis=0)
      image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
      # 每个框代表一个物体被侦测到.
      boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
      # 每个分值代表侦测到物体的可信度.
      scores = detection_graph.get_tensor_by_name('detection_scores:0')
      classes = detection_graph.get_tensor_by_name('detection_classes:0')
      num_detections = detection_graph.get_tensor_by_name('num_detections:0')
      # 执行侦测任务.
      (boxes, scores, classes, num_detections) = sess.run(
          [boxes, scores, classes, num_detections],
          feed_dict={image_tensor: image_np_expanded})
      # 图形化.
      vis_util.visualize_boxes_and_labels_on_image_array(
          image_np,
          np.squeeze(boxes),
          np.squeeze(classes).astype(np.int32),
          np.squeeze(scores),
          category_index,
          use_normalized_coordinates=True,
          line_thickness=8)
      plt.figure(figsize=IMAGE_SIZE)
      plt.imshow(image_np)
