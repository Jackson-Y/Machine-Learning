""" TF API r1.3, Convolutional Neural Network. """
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf

tf.logging.set_verbosity(tf.logging.INFO)

def cnn_model(features, labels, mode):
    """ Model function for CNN. """
    # Input layer
    # why [-1, 28, 28, 1] ?
    # 输入的图片数据的shape：[batch_size, image_width, image_height, channels]
    # batch_size: 训练时，每次梯度下降所用的样本数。
    # image_width: 图片宽度
    # image_height: 图片高度
    # channels: 图片的原色。彩色的为三原色（红，绿，蓝），此时channels为3，
    #           MNIST数据集中颜色为黑白色，原色为（黑），所用channels为1.
    # Here， MNIST数据集： [batch_size, 28, 28, 1]
    input_layer = tf.reshape(features["x"], [-1, 28, 28, 1])

    # Convolutional layer #1
    # 
    # tensorflow API r1.3:
    # tf.layers.conv2d(
    #     inputs,
    #     filters,
    #     kernel_size,
    #     strides=(1, 1),
    #     padding='valid',
    #     data_format='channels_last',
    #     dilation_rate=(1, 1),
    #     activation=None,
    #     use_bias=True,
    #     kernel_initializer=None,
    #     bias_initializer=tf.zeros_initializer(),
    #     kernel_regularizer=None,
    #     bias_regularizer=None,
    #     activity_regularizer=None,
    #     trainable=True,
    #     name=None,
    #     reuse=None
    # )
    # 下方代码中，conv1返回值shape：[batch_size, 28, 28, 32]
    conv1 = tf.layers.conv2d(
        inputs=input_layer,
        filters=32,  # 滤波器的个数，同一片区域学习出32个不同的特征。
        kernel_size=[5, 5],  # 滤波器的大小为5*5的矩阵。
        padding="same",  # “same” 表示该函数输出的tensor大小和输入的tensor大小一致，具有相同的width和height，按需自动在图片周围补0。
        activation=tf.nn.relu) # 激活函数使用tf.nn.relu，修正线性单元。
    
    # Pooling layer #1
    # 池大小为pool_size=[2, 2], 2*2大小的矩阵。
    # 池移动的步长strides=2，每次移动2个像素点。
    # 下方实例代码，pool1返回值shape： [batch_size, 14, 14, 32]
    pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)

    # Convolutional layer #2 and Pooling layer #2
    # Return shape: [batch_size, 14, 14, 64]
    conv2 = tf.layers.conv2d(
        inputs=pool1,
        filters=64,
        kernel_size=[5, 5],
        padding='same',
        activation=tf.nn.relu)
    # Return shape: [batch_size, 7, 7, 64]
    pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)

    # Dense layer(Fully connection layer)
    # 全连接层
    ## Flatten： 把 [batch_size, 7, 7, 64] 转换成 [batch_size, 7*7*64]=[batch_size, 3136]
    pool2_flat = tf.reshape(pool2, [-1, 7 * 7 * 64])
    ## 全连接映射到1024个单元上。
    dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)
    ## 增加dropout层，减小overfitting的概率。
    ## rate=0.4 意味着有40%的样本将会被随机的舍弃。
    ## Return shape： [batch_size, 1024]
    dropout = tf.layers.dropout(
        inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)
    
    # Logits layer
    ## 把上一层的结果映射到10个单元上，即最终的10个手写体数字（0-9）。
    ## Return shape: [batch_size, 10]
    logits = tf.layers.dense(inputs=dropout, units=10)

    predictions = {
        # Generate predictions (for Predict and Eval mode)
        ## 找出输入的tensor：logits中最大值得索引（位置）。
        "classes": tf.argmax(input=logits, axis=1),
        # Add `softmax_tensor` to the graph. It is used for Predict and
        # `logging_hook`.
        ## 使用softmax激活函数计算logits中的概率。
        "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
    }

    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    # Calculate loss (for both Train and Eval modes)
    ## 计算图片对应的标签labels和模型预测出来的逻辑结果logits之间的损失loss（误差）
    onehot_labels = tf.one_hot(indices=tf.cast(labels, tf.int32), depth=10)
    loss = tf.losses.softmax_cross_entropy(
        onehot_labels=onehot_labels, logits=logits)
    
    # Configure the Training Op (for Train mode)
    ## 通过梯度下降算法，最小化损失loss（误差）
    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

    # Add evaluation metrics (for Eval mode)
    ## 计算准确率，即正确识别出来的测试样本数与测试样本总数的比。
    eval_metric_ops = {
        "accuracy": tf.metrics.accuracy(
            labels=labels, predictions=predictions["classes"]
        )
    }
    return tf.estimator.EstimatorSpec(mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)

def main(unused_argv):
    """ Main function. """
    # LoadTraining and Test data
    mnist = tf.contrib.learn.datasets.load_dataset("mnist")
    train_data = mnist.train.images
    train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
    eval_data = mnist.test.images
    eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)
    # Create the Estimator
    mnist_classifier = tf.estimator.Estimator(
        model_fn=cnn_model, model_dir="mnist_cnn_model"
    )
    # Set up logging for predictions
    tensors_to_log = {"probabilites": "softmax_tensor"}
    logging_hook = tf.train.LoggingTensorHook(
        tensors=tensors_to_log, every_n_iter=50
    )
    # Train the model
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": train_data},
        y=train_labels,
        batch_size=100,
        num_epochs=None,
        shuffle=True
    )
    mnist_classifier.train(
        input_fn=train_input_fn,
        steps=2000,
        hooks=[logging_hook]
    )
    # Evalute the mode and print results
    eval_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": eval_data},
        y=eval_labels,
        num_epochs=1,
        shuffle=False
    )
    eval_results = mnist_classifier.evaluate(input_fn=eval_input_fn)
    print(eval_results)

if __name__ == "__main__":
    tf.app.run()
