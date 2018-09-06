
# coding: utf-8

# In[1]:


import numpy as np
import os
import io
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import math
#import msgpack
import fuzzyfunc as fz

p=np.arange(15,dtype=float).reshape(5,3)
p[0,0]=0.04678426
p[0,1]=0.54678426
p[0,2]=0.94678426
p[1,0]=1.0
p[1,1]=0.57228076
p[1,2]=0.0
p[2,0]=0.0873352
p[2,1]=0.59873352
p[2,2]=0.99873352
p[3,0]=1.0
p[3,1]=0.58989477
p[3,2]=0.0
#this is trained parameters of membership function's shape

sys.path.append("/home/user/Documents/calcrisk/object_detection/")

from collections import defaultdict
from matplotlib import pyplot as plt
from PIL import Image

if tf.__version__ != '1.4.0':
  raise ImportError('Please upgrade your tensorflow installation to v1.4.0!')


# In[2]:


# This is needed to display the images.
#get_ipython().magic(u'matplotlib inline')

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")


# In[3]:


from utils import label_map_util

from utils import visualization_utils as vis_util


# In[8]:


# What model to download.
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
#MODEL_FILE = MODEL_NAME + '.tar.gz'
#DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90


# In[9]:


#opener = urllib.request.URLopener()
#opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
#tar_file = tarfile.open(MODEL_FILE)
#for file in tar_file.getmembers():
#  file_name = os.path.basename(file.name)
#  if 'frozen_inference_graph.pb' in file_name:
#    tar_file.extract(file, os.getcwd())


# In[10]:


detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


# In[11]:


label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# In[12]:


def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


# In[13]:


# For the sake of simplicity we will use only 2 images:
# image1.jpg
# image2.jpg
# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
PATH_TO_TEST_IMAGES_DIR = 'test_images'
TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'screenshot{}.png'.format(i)) for i in range(1, 2) ]

# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)


# In[14]:


def detection(img):
    with detection_graph.as_default():
      with tf.Session(graph=detection_graph) as sess:
        # Definite input and output Tensors for detection_graph
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        image = Image.open(img)
        # the array based representation of the image will be used later in order to prepare the
        # result image with boxes and labels on it.
        image_np = load_image_into_numpy_array(image)
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        # Actual detection.
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})
        # Visualization of the results of a detection.
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=8)
        plt.figure(figsize=IMAGE_SIZE)
	#image.save("test_images/screenshot.png")
        #plt.imshow(image_np)
        a=np.zeros(6)
	text=""
        for i in range(0,20):
	    print (boxes[0,i,1]+boxes[0,i,3])*0.5,1-boxes[0,i,2],scores[0,i],classes[0,i]
            if (scores[0,i]>0.2):
                l=fz.directionguide(boxes[0,i])
                r=fz.calcriskmodel2(boxes[0,i],classes[0,i],p)
		for j in range(0,4):
		    text+=str(boxes[0,i,j])+":"
		text+=str(classes[0,i])+":"
		text+=str(r)+"@"
                a[l]=a[l]+r

	text+=str(fz.decideaction(a))
	#print (fz.decideaction(a))
        return text


# In[ ]:

from flask import Flask,request
    
app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return "Hello"


i=0
@app.route("/test_api", methods=["POST"])
def test():
    if request.method == "POST":       
	image_bytes = request.files["post_data"]
	result = detection(image_bytes)
        #print str(result)
	return result

if __name__ == "__main__":
    app.debug = True
    app.run("0.0.0.0")

