import tensorflow as tf

from ..util.bbox import bbox2offset, offset2centerness
from ..util.overlap import overlap_point

def point_target(y_true, bbox_true, y_pred, bbox_pred, points, regress_range, centerness_pred = None, sampling_count = 256, positive_ratio = 0.5):
    """
    y_true = label #(padded_num_true, 1 or num_class)
    bbox_true = [[x1, y1, x2, y2], ...] #(padded_num_true, bbox)
    y_pred = classifier logit #(num_points, 1 or num_class)
    bbox_pred = classifier regress #(num_points, offset)
    points = [[center_x, center_y], ...] #(num_points, point)
    regress_range = [[min_offset_range, max_offet_range], ...] #(num_points, regress_range)
    centerness_pred = classifier centerness(heat map) #(num_points, 1)
    """
    pred_count = tf.shape(points)[0]
    valid_indices = tf.where(tf.reduce_max(tf.cast(0 < bbox_true, tf.int32), axis = -1))
    y_true = tf.gather_nd(y_true, valid_indices)
    bbox_true = tf.gather_nd(bbox_true, valid_indices)
    
    overlaps = overlap_point(bbox_true, points, regress_range)
    max_area = tf.reduce_max(overlaps, axis = -1)
    
    positive_indices = tf.where(max_area != 0)[:, 0]
    negative_indices = tf.where(max_area == 0)[:, 0]
    
    if sampling_count is not None:
        positive_count = tf.cast(sampling_count * positive_ratio, tf.int32)
        positive_indices = tf.random.shuffle(positive_indices)[:positive_count]
        positive_count = tf.cast(tf.shape(positive_indices)[0], tf.float32)
        negative_count = tf.cast(1 / positive_ratio * positive_count - positive_count, tf.int32)
        negative_indices = tf.random.shuffle(negative_indices)[:negative_count]
    else:
        sampling_count = pred_count
    pred_indices = tf.concat([positive_indices, negative_indices], axis = 0)
    
    positive_overlaps = tf.gather(overlaps, positive_indices)
    true_indices = tf.cond(tf.greater(tf.shape(positive_overlaps)[1], 0), true_fn = lambda: tf.argmax(positive_overlaps, axis = -1), false_fn = lambda: tf.cast(tf.constant([]), tf.int64))
    y_true = tf.gather(y_true, true_indices)
    bbox_true = tf.gather(bbox_true, true_indices)
    y_pred = tf.gather(y_pred, pred_indices)
    bbox_pred = tf.gather(bbox_pred, positive_indices)
    points = tf.gather(points, positive_indices)
    if centerness_pred is not None:
        centerness_pred = tf.gather(centerness_pred, positive_indices)
    
    if tf.keras.backend.int_shape(true_indices)[0] != 0:
        bbox_true = bbox2offset(bbox_true, points) #offset
        if centerness_pred is not None:
            centerness_true = offset2centerness(bbox_true)
    else:
        if centerness_pred is not None:
            centerness_true = tf.zeros_like(centerness_pred, dtype = centerness_pred.dtype)
        
    n_class = tf.shape(y_true)[-1]
    negative_count = tf.shape(negative_indices)[0]
    pad_count = tf.maximum(sampling_count - tf.shape(pred_indices)[0], 0)
    y_true = tf.cond(tf.equal(n_class, 1), true_fn = lambda: tf.pad(y_true, [[0, negative_count + pad_count], [0, 0]]), false_fn = lambda: tf.concat([y_true, tf.cast(tf.pad(tf.ones([negative_count + pad_count, 1]), [[0, 0], [0, n_class - 1]]), y_true.dtype)], axis = 0))
    bbox_true = tf.pad(bbox_true, [[0, negative_count + pad_count], [0, 0]])
    y_pred = tf.pad(y_pred, [[0, pad_count], [0, 0]])
    bbox_pred = tf.pad(bbox_pred, [[0, negative_count + pad_count], [0, 0]])
    result = y_true, bbox_true, y_pred, bbox_pred
    if centerness_pred is not None:
        centerness_true = tf.pad(centerness_true, [[0, negative_count + pad_count], [0, 0]])
        centerness_pred = tf.pad(centerness_pred, [[0, negative_count + pad_count], [0, 0]])
        result = y_true, bbox_true, centerness_true, y_pred, bbox_pred, centerness_pred
    return result