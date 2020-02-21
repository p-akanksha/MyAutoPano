"""
CMSC733 Spring 2019: Classical and Deep Learning Approaches for
Geometric Computer Vision
Homework 0: Alohomora: Phase 2 Starter Code


Author(s):
Nitin J. Sanket (nitinsan@terpmail.umd.edu)
PhD Candidate in Computer Science,
University of Maryland, College Park
"""

import tensorflow as tf
import sys
import numpy as np
from Misc.TFSpatialTransformer import transformer
from Misc.TensorDLT import TensorDLT
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

# Don't generate pyc codes
sys.dont_write_bytecode = True

def SupervisedModel(Img, ImageSize, MiniBatchSize):
    """
    Inputs: 
    Img is a MiniBatch of the current image
    ImageSize - Size of the Image
    Outputs:
    prLogits - logits output of the network
    prSoftMax - softmax output of the network
    """

    #############################
    # Fill your network here!
    #############################
    x = tf.layers.conv2d(inputs=Img, padding='same', filters=64, kernel_size=[3,3], activation=None, strides = 1)
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)


    x = tf.layers.conv2d(inputs=x, padding='same', filters=64, kernel_size=[3,3], activation=None, strides = 1)
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)
    x=tf.layers.max_pooling2d(inputs=x, pool_size=[2,2], strides=2, padding='VALID')


    x = tf.layers.conv2d(inputs=x, padding='same', filters=64, kernel_size=[3,3], activation=None, strides = 1)
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)


    x = tf.layers.conv2d(inputs=x, padding='same', filters=64, kernel_size=[3,3], activation=None, strides = 1)
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)
    x=tf.layers.max_pooling2d(inputs=x, pool_size=[2,2], strides=2, padding='VALID')


    x = tf.layers.conv2d(inputs=x, padding='same', filters=128, kernel_size=[3,3], activation=None, strides = 1)
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)


    x = tf.layers.conv2d(inputs=x, padding='same', filters=128, kernel_size=[3,3], activation=None, strides = 1)
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)
    x=tf.layers.max_pooling2d(inputs=x, pool_size=[2,2], strides=2, padding='VALID')


    x = tf.layers.conv2d(inputs=x, padding='same', filters=128, kernel_size=[3,3], activation=None, strides = 1)
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)


    x = tf.layers.conv2d(inputs=x, padding='same', filters=128, kernel_size=[3,3], activation=None, strides = 1)
    x = tf.layers.batch_normalization(x)
    x = tf.nn.relu(x)
    x = tf.nn.dropout(x, keep_prob=0.5)
    
    x = tf.layers.flatten(x)  

    x = tf.layers.dense(inputs=x, name='fc_1',units=1024, activation=tf.nn.relu)
    x = tf.nn.dropout(x, keep_prob=0.5)
    x = tf.layers.batch_normalization(x)

    x = tf.layers.dense(inputs=x, name='fc_2',units=8, activation= None)



    #prLogits is defined as the final output of the neural network
    prLogits = x
    
    #prSoftMax is defined as normalized probabilities of the output of the neural network
    # prSoftMax = tf.nn.softmax(logits = prLogits)
    
    return prLogits

def UnsupervisedModel(Img,IA,CA, PB,ImageSize, MiniBatchSize):
    H4pt = SupervisedModel(Img, ImageSize, MiniBatchSize)
    C4A_pts = tf.reshape(CA,[MiniBatchSize,8])
   
    H_mat = TensorDLT(H4pt, C4A_pts, MiniBatchSize)
    img_h = ImageSize[0]
    img_w = ImageSize[1]
    # Constants and variables used for spatial transformer
    M = np.array([[img_w/2.0, 0., img_w/2.0],
                  [0., img_h/2.0, img_h/2.0],
                  [0., 0., 1.]]).astype(np.float32)

    M_tensor  = tf.constant(M, tf.float32)
    M_tile   = tf.tile(tf.expand_dims(M_tensor, [0]), [MiniBatchSize, 1,1])
    # Inverse of M
    M_inv = np.linalg.inv(M)
    M_tensor_inv = tf.constant(M_inv, tf.float32)
    M_tile_inv   = tf.tile(tf.expand_dims(M_tensor_inv, [0]), [MiniBatchSize,1,1])

    y_t = tf.range(0, MiniBatchSize*img_w*img_h, img_w*img_h)
    z =  tf.tile(tf.expand_dims(y_t,[1]),[1,128*128])
    batch_indices_tensor = tf.reshape(z, [-1]) # Add these value to patch_indices_batch[i] for i in range(num_pairs) # [BATCH_SIZE*WIDTH*HEIGHT]

    # Transform H_mat since we scale image indices in transformer
    H_mat = tf.matmul(tf.matmul(M_tile_inv, H_mat), M_tile)
    # Transform image 1 (large image) to image 2
    out_size = (img_h, img_w)

    
    warped_images, _ = transformer(IA, H_mat, out_size)
    # print(warped_images.get_shape())
    pred_PB = tf.reduce_mean(warped_images, 3)

    pred_PB = tf.reshape(pred_PB, [MiniBatchSize, 128, 128, 1])


    return pred_PB,PB


