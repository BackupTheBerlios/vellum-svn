def curry_left(func, *args):
    return lambda *callargs, **kwargs: func( *(args + callargs), **kwargs )

def curry_right(func, *args):
    return lambda *callargs, **kwargs: func( *(callargs + args), **kwargs )

curry=curry_left

def any(iterable):
    for boolean in iterable:
        if bool(boolean):
            return True
    return False

def all(iterable):
    for boolean in iterable:
        if not bool(boolean):
            return False
    return True
