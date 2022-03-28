import tensorflow as tf
import functools

from .retina import retinanet
from ..backbone.effnet import effnet_b0, effnet_b1, effnet_b2, effnet_b3, effnet_b4, effnet_b5, effnet_b6
from ..neck import bifpn, FeaturePyramidNetwork

def normalize(axis = -1, momentum = 0.997, epsilon = 1e-4, **kwargs):
    return tf.keras.layers.BatchNormalization(axis = axis, momentum = momentum, epsilon = epsilon, **kwargs)

def effdet(x, n_class = 21, image_shape = [1024, 1024], n_feature = 224, n_depth = 4, sub_sampling = 2,
           scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True,
           sub_n_feature = None, sub_momentum = 0.997, sub_epsilon = 1e-4, fpn = functools.partial(bifpn, n_feature = 224), fpn_n_depth = 7,
           cls_activation = tf.nn.swish, bbox_activation = tf.nn.swish):
    out = retinanet(x, n_class = n_class, image_shape = image_shape, n_feature = n_feature, n_depth = n_depth, sub_sampling = sub_sampling,
                    scale = scale, ratio = ratio, auto_scale = auto_scale,
                    sub_n_feature = sub_n_feature, sub_momentum = sub_momentum, sub_epsilon = sub_epsilon, fpn = fpn, fpn_n_depth = fpn_n_depth,
                    cls_activation = cls_activation, bbox_activation = bbox_activation)
    return out

def effdet_d0(x, n_class = 21,
              n_feature = 64, n_depth = 3,
              scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
              sub_n_feature = None, sub_momentum = 0.997, sub_epsilon = 1e-4, fpn = functools.partial(bifpn, n_feature = 64), fpn_n_depth = 3,
              cls_activation = tf.nn.swish, bbox_activation = tf.nn.swish):
    #image_shape = [512, 512]
    feature = effnet_b0(x, weights = weights)[-3:]
    out = effdet(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth, sub_sampling = 2,
                 scale = scale, ratio = ratio, auto_scale = auto_scale,
                 sub_n_feature = sub_n_feature, sub_momentum = sub_momentum, sub_epsilon = sub_epsilon, fpn = fpn, fpn_n_depth = fpn_n_depth,
                 cls_activation = cls_activation, bbox_activation = bbox_activation)
    return out
                    
def effdet_d1(x, n_class = 21,
              n_feature = 88, n_depth = 3,
              scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
              sub_n_feature = None, sub_momentum = 0.997, sub_epsilon = 1e-4, fpn = functools.partial(bifpn, n_feature = 88), fpn_n_depth = 4,
              cls_activation = tf.nn.swish, bbox_activation = tf.nn.swish):
    #image_shape = [640, 640]
    feature = effnet_b1(x, weights = weights)[-3:]
    out = effdet(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth, sub_sampling = 2,
                 scale = scale, ratio = ratio, auto_scale = auto_scale,
                 sub_n_feature = sub_n_feature, sub_momentum = sub_momentum, sub_epsilon = sub_epsilon, fpn = fpn, fpn_n_depth = fpn_n_depth,
                 cls_activation = cls_activation, bbox_activation = bbox_activation)
    return out
                    
def effdet_d2(x, n_class = 21,
              n_feature = 112, n_depth = 3,
              scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
              sub_n_feature = None, sub_momentum = 0.997, sub_epsilon = 1e-4, fpn = functools.partial(bifpn, n_feature = 112), fpn_n_depth = 5,
              cls_activation = tf.nn.swish, bbox_activation = tf.nn.swish):
    #image_shape = [768, 768]
    feature = effnet_b2(x, weights = weights)[-3:]
    out = effdet(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth, sub_sampling = 2,
                 scale = scale, ratio = ratio, auto_scale = auto_scale,
                 sub_n_feature = sub_n_feature, sub_momentum = sub_momentum, sub_epsilon = sub_epsilon, fpn = fpn, fpn_n_depth = fpn_n_depth,
                 cls_activation = cls_activation, bbox_activation = bbox_activation)
    return out
                    
def effdet_d3(x, n_class = 21,
              n_feature = 160, n_depth = 4,
              scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
              sub_n_feature = None, sub_momentum = 0.997, sub_epsilon = 1e-4, fpn = functools.partial(bifpn, n_feature = 160), fpn_n_depth = 6,
              cls_activation = tf.nn.swish, bbox_activation = tf.nn.swish):
    #image_shape = [896, 896]
    feature = effnet_b3(x, weights = weights)[-3:]
    out = effdet(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth, sub_sampling = 2,
                 scale = scale, ratio = ratio, auto_scale = auto_scale,
                 sub_n_feature = sub_n_feature, sub_momentum = sub_momentum, sub_epsilon = sub_epsilon, fpn = fpn, fpn_n_depth = fpn_n_depth,
                 cls_activation = cls_activation, bbox_activation = bbox_activation)
    return out
                    
def effdet_d4(x, n_class = 21,
              n_feature = 224, n_depth = 4,
              scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
              sub_n_feature = None, sub_momentum = 0.997, sub_epsilon = 1e-4, fpn = functools.partial(bifpn, n_feature = 224), fpn_n_depth = 7,
              cls_activation = tf.nn.swish, bbox_activation = tf.nn.swish):
    #image_shape = [1024, 1024]
    feature = effnet_b4(x, weights = weights)[-3:]
    out = effdet(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth, sub_sampling = 2,
                 scale = scale, ratio = ratio, auto_scale = auto_scale,
                 sub_n_feature = sub_n_feature, sub_momentum = sub_momentum, sub_epsilon = sub_epsilon, fpn = fpn, fpn_n_depth = fpn_n_depth,
                 cls_activation = cls_activation, bbox_activation = bbox_activation)
    return out
                    
def effdet_d5(x, n_class = 21,
              n_feature = 288, n_depth = 4,
              scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
              sub_n_feature = None, sub_momentum = 0.997, sub_epsilon = 1e-4, fpn = functools.partial(bifpn, n_feature = 288), fpn_n_depth = 7,
              cls_activation = tf.nn.swish, bbox_activation = tf.nn.swish):
    #image_shape = [1280, 1280]
    feature = effnet_b5(x, weights = weights)[-3:]
    out = effdet(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth, sub_sampling = 2,
                 scale = scale, ratio = ratio, auto_scale = auto_scale,
                 sub_n_feature = sub_n_feature, sub_momentum = sub_momentum, sub_epsilon = sub_epsilon, fpn = fpn, fpn_n_depth = fpn_n_depth,
                 cls_activation = cls_activation, bbox_activation = bbox_activation)
    return out
                    
def effdet_d6(x, n_class = 21,
              n_feature = 384, n_depth = 5,
              scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
              sub_n_feature = None, sub_momentum = 0.997, sub_epsilon = 1e-4, fpn = functools.partial(bifpn, n_feature = 384, weighted_add = False), fpn_n_depth = 8,
              cls_activation = tf.nn.swish, bbox_activation = tf.nn.swish):
    #image_shape = [1280, 1280] > d6
    #image_shape = [1536, 1536] > d7
    feature = effnet_b6(x, weights = weights)[-3:]
    out = effdet(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth, sub_sampling = 2,
                 scale = scale, ratio = ratio, auto_scale = auto_scale,
                 sub_n_feature = sub_n_feature, sub_momentum = sub_momentum, sub_epsilon = sub_epsilon, fpn = fpn, fpn_n_depth = fpn_n_depth,
                 cls_activation = cls_activation, bbox_activation = bbox_activation)
    return out

effdet_d7 = effdet_d6

def effdet_d7x(x, n_class = 21,
               n_feature = 384, n_depth = 5,
               scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
               sub_n_feature = None, sub_momentum = 0.997, sub_epsilon = 1e-4, fpn = functools.partial(bifpn, n_feature = 384, weighted_add = False), fpn_n_depth = 8,
               cls_activation = tf.nn.swish, bbox_activation = tf.nn.swish):
    #image_shape = [1536, 1536]
    feature = effnet_b7(x, weights = weights)[-3:]
    out = effdet(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth, sub_sampling = 2,
                 scale = scale, ratio = ratio, auto_scale = auto_scale,
                 sub_n_feature = sub_n_feature, sub_momentum = sub_momentum, sub_epsilon = sub_epsilon, fpn = fpn, fpn_n_depth = fpn_n_depth,
                 cls_activation = cls_activation, bbox_activation = bbox_activation)
    return out
    
try:
    from ..backbone.effnet import effnet_lite_b0, effnet_lite_b1, effnet_lite_b2, effnet_lite_b3, effnet_lite_b4

    def bifpn_lite(n_feature = 88, use_bias = True, weighted_add = False, method = "nearest", normalize = normalize, activation = tf.nn.relu6, mode = "bifpn", **kwargs):
        return FeaturePyramidNetwork(mode = mode, n_feature = n_feature, use_bias = use_bias, weighted_add = weighted_add, method = method, normalize = normalize, activation = activation, **kwargs)

    def effdet_lite(x, n_class = 21, image_shape = [384, 384], n_feature = 88, n_depth = 3, sub_sampling = 2,
                    scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True,
                    sub_n_feature = None, sub_momentum = 0.997, sub_epsilon = 1e-4, fpn = functools.partial(bifpn_lite, n_feature = 88), fpn_n_depth = 4,
                    cls_activation = tf.nn.relu6, bbox_activation = tf.nn.relu6):
        out = retinanet(x, n_class = n_class, image_shape = image_shape, n_feature = n_feature, n_depth = n_depth, sub_sampling = sub_sampling,
                        scale = scale, ratio = ratio, auto_scale = auto_scale,
                        sub_n_feature = sub_n_feature, sub_momentum = sub_momentum, sub_epsilon = sub_epsilon, fpn = fpn, fpn_n_depth = fpn_n_depth,
                        cls_activation = cls_activation, bbox_activation = bbox_activation)
        return out

    def effdet_lite_d0(x, n_class = 21,
                       n_feature = 64, n_depth = 3,
                       scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
                       sub_n_feature = None, sub_momentum = 0.997, sub_epsilon = 1e-4, fpn = functools.partial(bifpn_lite, n_feature = 64), fpn_n_depth = 3,
                       cls_activation = tf.nn.relu6, bbox_activation = tf.nn.relu6):
        #image_shape = [320, 320]
        feature = effnet_lite_b0(x, weights = weights)[-3:]
        out = effdet_lite(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth, sub_sampling = 2,
                          scale = scale, ratio = ratio, auto_scale = auto_scale,
                          sub_n_feature = sub_n_feature, sub_momentum = sub_momentum, sub_epsilon = sub_epsilon, fpn = fpn, fpn_n_depth = fpn_n_depth,
                          cls_activation = cls_activation, bbox_activation = bbox_activation)
        return out

    def effdet_lite_d1(x, n_class = 21,
                       n_feature = 88, n_depth = 3,
                       scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
                       sub_n_feature = None, sub_momentum = 0.997, sub_epsilon = 1e-4, fpn = functools.partial(bifpn_lite, n_feature = 88), fpn_n_depth = 4,
                       cls_activation = tf.nn.relu6, bbox_activation = tf.nn.relu6):
        #image_shape = [384, 384]
        feature = effnet_lite_b1(x, weights = weights)[-3:]
        out = effdet_lite(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth, sub_sampling = 2,
                          scale = scale, ratio = ratio, auto_scale = auto_scale,
                          sub_n_feature = sub_n_feature, sub_momentum = sub_momentum, sub_epsilon = sub_epsilon, fpn = fpn, fpn_n_depth = fpn_n_depth,
                          cls_activation = cls_activation, bbox_activation = bbox_activation)
        return out
                        
    def effdet_lite_d2(x, n_class = 21,
                       n_feature = 112, n_depth = 3,
                       scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
                       sub_n_feature = None, sub_momentum = 0.997, sub_epsilon = 1e-4, fpn = functools.partial(bifpn_lite, n_feature = 112), fpn_n_depth = 5,
                       cls_activation = tf.nn.relu6, bbox_activation = tf.nn.relu6):
        #image_shape = [448, 448]
        feature = effnet_lite_b2(x, weights = weights)[-3:]
        out = effdet_lite(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth, sub_sampling = 2,
                          scale = scale, ratio = ratio, auto_scale = auto_scale,
                          sub_n_feature = sub_n_feature, sub_momentum = sub_momentum, sub_epsilon = sub_epsilon, fpn = fpn, fpn_n_depth = fpn_n_depth,
                          cls_activation = cls_activation, bbox_activation = bbox_activation)
        return out
                        
    def effdet_lite_d3(x, n_class = 21,
                       n_feature = 160, n_depth = 4,
                       scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
                       sub_n_feature = None, sub_momentum = 0.997, sub_epsilon = 1e-4, fpn = functools.partial(bifpn_lite, n_feature = 160), fpn_n_depth = 6,
                       cls_activation = tf.nn.relu6, bbox_activation = tf.nn.relu6):
        #image_shape = [512, 512]
        feature = effnet_lite_b3(x, weights = weights)[-3:]
        out = effdet_lite(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth, sub_sampling = 2,
                          scale = scale, ratio = ratio, auto_scale = auto_scale,
                          sub_n_feature = sub_n_feature, sub_momentum = sub_momentum, sub_epsilon = sub_epsilon, fpn = fpn, fpn_n_depth = fpn_n_depth,
                          cls_activation = cls_activation, bbox_activation = bbox_activation)
        return out
                        
    def effdet_lite_d3x(x, n_class = 21,
                        n_feature = 200, n_depth = 4,
                        scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
                        sub_n_feature = None, sub_momentum = 0.997, sub_epsilon = 1e-4, fpn = functools.partial(bifpn_lite, n_feature = 200), fpn_n_depth = 6,
                        cls_activation = tf.nn.relu6, bbox_activation = tf.nn.relu6):
        #image_shape = [640, 640]
        feature = effnet_lite_b3(x, weights = weights)[-3:]
        out = effdet_lite(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth, sub_sampling = 2,
                          scale = scale, ratio = ratio, auto_scale = auto_scale,
                          sub_n_feature = sub_n_feature, sub_momentum = sub_momentum, sub_epsilon = sub_epsilon, fpn = fpn, fpn_n_depth = fpn_n_depth,
                          cls_activation = cls_activation, bbox_activation = bbox_activation)
        return out
                        
    def effdet_lite_d4(x, n_class = 21,
                       n_feature = 224, n_depth = 4,
                       scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], auto_scale = True, weights = "imagenet",
                       sub_n_feature = None, sub_momentum = 0.997, sub_epsilon = 1e-4, fpn = functools.partial(bifpn_lite, n_feature = 224), fpn_n_depth = 7,
                       cls_activation = tf.nn.relu6, bbox_activation = tf.nn.relu6):
        #image_shape = [640, 640]
        feature = effnet_lite_b4(x, weights = weights)[-3:]
        out = effdet_lite(feature, n_class = n_class, image_shape = x, n_feature = n_feature, n_depth = n_depth, sub_sampling = 2,
                          scale = scale, ratio = ratio, auto_scale = auto_scale,
                          sub_n_feature = sub_n_feature, sub_momentum = sub_momentum, sub_epsilon = sub_epsilon, fpn = fpn, fpn_n_depth = fpn_n_depth,
                          cls_activation = cls_activation, bbox_activation = bbox_activation)
        return out
except:
    print("If you want to use 'EfficientDet-Lite', please install 'keras'")