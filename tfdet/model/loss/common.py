import tensorflow as tf

def smooth_l1_loss(y_true, y_pred, sigma = 1):
    diff = tf.abs(y_true - y_pred)
    less_than_one = tf.cast(tf.less(diff, (1.0 / sigma ** 2)), y_pred.dtype)
    loss = (less_than_one * (0.5 * sigma ** 2) * diff ** 2) + (1 - less_than_one) * (diff - (0.5 / sigma ** 2))
    return loss