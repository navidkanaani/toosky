

def gaurd_edge(function):
    def wrapper(*args, **kwargs):
        try:
            result = function(*args, **kwargs)
            return result
        except Exception as exc:
            #
            #  Handling error in the near future
            #
            raise
