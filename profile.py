import time

def timeit(fn):
    def timed(*args, **kw):
        ts = time.time()
        result = fn(*args, **kw)
        te = time.time()
        timed.times = '%2.2f' % (te - ts)
        return result
    return timed

def counted(fn):
    def wrapper(*args, **kwargs):
        wrapper.called+= 1
        return fn(*args, **kwargs)
    wrapper.called= 0
    wrapper.__name__= fn.__name__
    return wrapper

def counting(other):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            other.called= 0
            try:
                return fn(*args, **kwargs)
            finally:
                print '%s was called %i times' %\
                    (other.__name__, other.called)
        wrapper.__name__= fn.__name__
        return wrapper
    return decorator
