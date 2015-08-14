__author__ = 'wojtek'

def std_list(*xs):
    frame = map(lambda x: "{"+str(x)+"}", range(len(xs)))
    return "\t->\t".join(frame).format(*xs)