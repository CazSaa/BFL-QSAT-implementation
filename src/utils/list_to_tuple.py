# https://stackoverflow.com/a/60980685/14851412
def list_to_tuple(function):
    def wrapper(*args):
        tuple_args = [tuple(x) if type(x) == list else x for x in args]
        return function(*tuple_args)
    return wrapper
