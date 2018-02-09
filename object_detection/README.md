# Object Detection
================
## Tensorflow Models
[Tensorflow Object Detection API](https://github.com/tensorflow/models/blob/master/research/object_detection)

**Ubuntu17.04**
**Python2.7.13**
**Tensorflow1.4.0**

### Step 1: Installation
- **Dependences**
```
sudo apt-get install protobuf-compiler python-pil python-tk python-lxml
sudo pip install pillow
sudo pip install jupyter
sudo pip install matplotlib
sudo pip install tensorflow  (For CPU)
sudo pip install tensorflow-gpu  (For GPU)
```

- **protobuf**

While `sudo apt-get install protobuf-compiler`, you may meet the ERROR `E: Unable to locate package protobuf-compiler`. Then you can check the config file `/etc/apt/source.list`: 
    ```
    deb http://us.archive.ubuntu.com/ubuntu trusty main multiverse
    ```
protobuf-compiler is in the **'trusty'**. 

Also, you can install protobuf with Source Code. See: 
    http://blog.csdn.net/sunxianliang1/article/details/50723086

- **Protobuf Compilation**

```
cd tensorflow/models/research/
# From tensorflow/models/research/
protoc object_detection/protos/*.proto --python_out=.
```

- **Add Libraries to PYTHONPATH**

1) Temporary Solution
```
# From tensorflow/models/research/
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
```
2) Perpetual Solution
Add to the end of `~/.bashrc` file
```
MODELS_PATH=/home/code/tensorflow/models/research/
export PYTHONPATH=$PYTHONPATH:$MODELS_PATH:$MODELS_PATH/slim
```

- **Testing the Installation**

```
python object_detection/builders/model_builder_test.py
```
It run into error below:
`RuntimeError: module compiled against API version 0xb but this version of numpy is 0xa`
and
`ImportError: No module named _tkinter, please install the python-tk package`

You can:
```
sudo pip install numpy --upgrade
sudo apt-get install python-tk
```

### Step 2: Preprocess Input
Download Oxford-IIIT Pets Dataset:
```
# Under the directory: tensorflow/models/research/
wget http://www.robots.ox.ac.uk/~vgg/data/pets/data/images.tar.gz
wget http://www.robots.ox.ac.uk/~vgg/data/pets/data/annotations.tar.gz
tar -xvf images.tar.gz
tar -xvf annotations.tar.gz
```

Convert to TFRecord format:
```
python object_detection/dataset_tools/create_pet_tf_record.py   \
--label_map_path=object_detection/data/pet_label_map.pbtxt      \
--data_dir=`pwd`     \
--output=`pwd`
```

Get the model(same as yours) checkpoint trained:
```
wget http://download.tensorflow.org/models/object_detection/ssd_inception_v2_coco_2017_11_17.tar.gz
tar -xvf ssd_inception_v2_coco_2017_11_17.tar.gz
```

Get the Model(ssd_inception_v2) Configure:
```
cp object_detection/samples/configs/ssd_inception_v2_pets.config ./
cp object_detection/data/pet_label_map.pbtxt ./
```
Replace the `PATH_TO_BE_CONFIGURED` to `Your Real Path`:
```
sed -i "s/PATH_TO_BE_CONFIGURED/\/home\/code\/tensorflow\/models\/research\//g" ssd_inception_v2_pets.config
```

Up to now, the `tensorflow/models/research/` should have:
```
- ssd_inception_v2_pets.config
- model.ckpt.index
- model.ckpt.meta
- model.ckpt.data-00000-of-00001
- pet_label_map.pbtxt
- pet_train.record
- pet_val.record
```

### Step 3: Train Model
```
python object_detection/train.py --logtostderr      \
--pipeline_config_path=ssd_inception_v2_pets.config \
--train_dir=train_result/
```
For this step, it run into ERROR in my machine:

    INFO:tensorflow:Starting Session.
    INFO:tensorflow:Starting Queues.
    INFO:tensorflow:global_step/sec: 0
    Killed

The cause of the ERROR is that It was running out of memory. So,
I changed  `batch_size = 1`, it all worked.

Reference:
    [Stack Overflow](https://stackoverflow.com/questions/44833085/tensorflow-object-detection-killed-before-starting)

### Step 4: Tensorboard
```
tensorboard --logdir=train_result/
```
Use explorer: `http://localhost:6006`

### Step 5: Export
```
object_detection/export_inference_graph.py --input_type image_tensor  \
　　　　--pipeline_config_path ssd_inception_v2_pets.config \
　　　　--checkpoint_path train_result/model.ckpt-445 \
　　　　--inference_graph_path ./output_inference_graph.pb
```
Export the trained pb file: `output_inference_graph.pb`

### Step 6: Model Application

You MUST complete the Step 1 before you start.

[Object detection application in 30s](https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb) Jupyter Notebook

[Object detection application in 30s](https://github.com/Jackson-Y/Machine-Learning/blob/master/object_detection/object_detection_tutorial.py) python IDE


Completed! 

**Good Luck!**
