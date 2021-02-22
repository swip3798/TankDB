def pad(num):
    num = str(num)
    if len(num) < 2:
        return "0" + num
    return num

from .batch_iterator import BatchIterator