import cProfile


def profile(name=None):
    """ Decorator used for profiling subroutines. It outputs a stats file that
    can be viewed using cprofilev, e.g. cprofilev -f [path_to_stats_file]
    @param name: name of file to dump statistics
    """
    def inner(func):
        def wrapper(*args, **kwargs):
            prof = cProfile.Profile()
            retval = prof.runcall(func, *args, **kwargs)
            prof.dump_stats(name if name is not None else func.__name__ + ".profile")
            return retval
        return wrapper
    return inner
