
'''
Some stuff to make data programming easier, i guess
'''

import threading

class RunThreadFunc:
    
    '''never call explicitly, use .start to start and .finish to finish (blocking until done), .daemon
to toggle/set daemon property'''
    
    def __init__(self, thread):
        self.thread = thread
    
    def daemon(self, new=None):
        if new == None:
            self.thread.daemon = not self.thread.daemon
        elif bool(new):
            self.thread.daemon = True
        else:
            self.thread.daemon = False
    
    def start(self):
        self.thread.start()
    
    def finish(self):
        self.thread.join()

class ThreadFunc:
    
    '''A function that runs as a thread, returns RunThreadFunc object'''
    
    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args, **kwargs):
        return RunThreadFunc(threading.Thread(target=self.func, args=args, kwargs=kwargs))

class CacheFunc:
    
    '''Function with a cache'''
    
    def __init__(self, func):
        self.func = func
        self.cache = {}
    
    def __call__(self, *args, **kwargs):
        ak = (tuple(args), tuple(kwargs.keys()), tuple(kwargs.values()))
        if ak in cache:
            return cache[ak]
        else:
            x = self.func(*args, **kwargs)
            cache[ak] = x
            return x

def chain(value, *funcs):
    '''chain a value through functions'''
    for func in funcs:
        value = func(value)
    return value
