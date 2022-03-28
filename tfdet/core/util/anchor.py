import tensorflow as tf
import numpy as np

def generate_anchors(feature, image_shape = [1024, 1024], scale = [0.03125, 0.0625, 0.125, 0.25, 0.5], ratio = [0.5, 1, 2], normalize = True, auto_scale = True, flatten = True, concat = True, dtype = tf.float32):
    """
    feature = feature or [features] or shape or [shapes]
    scale = anchor_size scale
    ratio = anchor_height * np.sqrt(ratio), anchor_weight / np.sqrt(ratio)
    """
    if tf.is_tensor(feature) or not isinstance(feature, list) or isinstance(feature[0], int):
        feature = [feature]
    if not isinstance(scale, list):
        scale = [scale]
    if not isinstance(ratio, list):
        ratio = [ratio]

    if not isinstance(scale[0], list):
        if auto_scale and (len(scale) % len(feature)) == 0:
            scale = tf.split(scale, len(feature))
        else:
            scale = [scale] * len(feature)
    if not isinstance(ratio[0], list):
        ratio = [ratio] * len(feature)

    out = []
    for x, scale, ratio in zip(feature, scale, ratio):
        if not isinstance(scale, list) and not (tf.is_tensor(scale) and tf.keras.backend.ndim(scale) != 0):
            scale = [scale]
        scale = [scale, scale]
        
        feature_shape = x
        if tf.is_tensor(x) and 2 < tf.keras.backend.ndim(x) or (not tf.is_tensor(x) and 2 < np.ndim(x)):
            feature_shape = tf.shape(x) if tf.keras.backend.int_shape(x)[-3] is None else tf.keras.backend.int_shape(x)
            dtype = x.dtype
        if 2 < np.shape(feature_shape)[0]:
            feature_shape = feature_shape[-3:-1]
        
        stride = [1, 1]
        if 1 < tf.reduce_max(scale[0]):
            if normalize:
                scale = tf.cast(tf.divide(scale, tf.expand_dims(image_shape, axis = -1)), dtype)
            else:
                stride = image_shape
        
        # Generate base anchor
        scale = tf.cast(tf.expand_dims(scale, axis = 1), dtype = dtype)
        ratio = tf.cast(tf.expand_dims(ratio, axis = 1), dtype = dtype)

        h = tf.reshape(scale[0] * tf.sqrt(ratio), (-1, 1))
        w = tf.reshape(scale[1] / tf.sqrt(ratio), (-1, 1))

        anchors = tf.concat([-0.5 * w, -0.5 * h, 0.5 * w, 0.5 * h], axis = -1)

        # Shift base anchor
        center_x = (tf.cast(tf.range(feature_shape[1]), dtype) + tf.constant(0.5, dtype = dtype)) * tf.cast(1 / feature_shape[1], dtype) * tf.cast(stride[1], dtype)
        center_y = (tf.cast(tf.range(feature_shape[0]), dtype) + tf.constant(0.5, dtype = dtype)) * tf.cast(1 / feature_shape[0], dtype) * tf.cast(stride[0], dtype)

        center_x, center_y = tf.meshgrid(center_x, center_y)
        center_x = tf.reshape(center_x, [-1])
        center_y = tf.reshape(center_y, [-1])

        shifts = tf.expand_dims(tf.stack([center_x, center_y, center_x, center_y], axis = 1), axis = 1)
        anchors = tf.cast(tf.expand_dims(anchors, axis = 0), dtype = dtype) + shifts
        shape = [-1, 4]
        if not flatten:
            shape = tf.concat([feature_shape, shape], axis = 0)
        anchors = tf.reshape(anchors, shape)
        out.append(tf.stop_gradient(anchors))
    if len(out) == 1:
        out = out[0]
    elif concat and flatten:
        out = tf.concat(out, axis = 0)
    return out

def generate_points(feature, image_shape = [1024, 1024], stride = None, normalize = True, flatten = True, concat = True, dtype = tf.float32):
    if tf.is_tensor(feature) or not isinstance(feature, list) or isinstance(feature[0], int):
        feature = [feature]
    if not isinstance(stride, list):
        stride = [stride] * len(feature)
    
    out = []
    for x, stride in zip(feature, stride):
        shape = x
        if tf.is_tensor(x) and 2 < tf.keras.backend.ndim(x) or (not tf.is_tensor(x) and 2 < np.ndim(x)):
            shape = tf.shape(x) if tf.keras.backend.int_shape(x)[-3] is None else tf.keras.backend.int_shape(x)
        if 2 < np.shape(shape)[0]:
            shape = shape[-3:-1]
        
        stride = [stride, stride]
        if stride[0] is None:
            stride = tf.cast(tf.divide(image_shape, shape), dtype)
            if normalize:
                stride = tf.where(tf.greater(stride, 1), tf.divide(stride, tf.cast(image_shape, dtype)), stride)
        elif normalize and 1 < tf.reduce_max(stride):
            stride = tf.divide(stride, tf.cast(image_shape, dtype))
        shift = tf.cast(tf.divide(stride, 2), dtype)
        shift = tf.where(tf.greater(stride[0], 1), tf.floor(shift), shift)
        
        x, y = tf.meshgrid(tf.range(shape[0]), tf.range(shape[1]))
        point = tf.cast(tf.stack([x, y], axis = -1), dtype) * stride[::-1] + shift[::-1]
        if flatten:
            point = tf.reshape(point, [-1, 2])
        out.append(tf.stop_gradient(point))
    if len(out) == 1:
        out = out[0]
    elif concat and flatten:
        out = tf.concat(out, axis = 0)
    return out

def generate_scale(bbox_true, count = 5, decimal = 4):
    bbox_true = tf.reshape(bbox_true, (-1, 4))
    indices = tf.where(tf.reduce_max(tf.cast(0 < bbox_true, tf.int32), axis = -1))
    bbox_true = tf.gather_nd(bbox_true, indices)

    h = bbox_true[:, 3] - bbox_true[:, 1]
    w = bbox_true[:, 2] - bbox_true[:, 0]
    h, w = np.histogram2d(h, w, bins = count)[1:]
    scale = np.stack([h, w], axis = -1)
    scale = np.mean([scale[:count], scale[-count:]], axis = 0)
    return np.sort(np.round(scale, decimal), axis = 0)

def generate_scale2(min = 0.03125, max = 0.5, count = 5):
    return [min + (max - min) / (count - 1) * index for index in range(count)]

def generate_kmeans_scale(bbox_true, k = 5, decimal = 4, method = np.median, mode = "normal"):
    bbox_true = np.reshape(bbox_true, [-1, 4])
    bbox_true = bbox_true[np.max(0 < bbox_true, axis = -1)]
    wh = bbox_true - np.tile(bbox_true[..., :2], 2) #x1, y1, x2, y2 -> 0, 0, w, h
    
    n_bbox = len(wh)
    last_nearest = np.zeros((n_bbox,))

    cluster = wh[np.random.choice(n_bbox, k, replace = False)]
    while True:
        overlaps = overlap_bbox(wh, cluster, mode = mode) #(n_bbox, k)
        cur_nearest = np.argmin(1 - overlaps, axis = 0)
        if np.all(last_nearest == cur_nearest):
            break
        for index in range(k):
            cluster[index] = method(wh[cur_nearest == index], axis = 0)
        last_nearest = cur_nearest
    return np.sort(np.round(cluster[..., 2:], decimal), axis = 0)