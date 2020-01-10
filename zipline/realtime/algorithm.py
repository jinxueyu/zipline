from six import (
    exec_,
    iteritems,
    itervalues,
    string_types,
)
# from api_support import (
#     api_method
# )
import online_api
import functools

def api_method(f):
    # Decorator that adds the decorated class method as a callable
    # function (wrapped) to zipline.api
    @functools.wraps(f)
    def wrapped(self, *args, **kwargs):
        # Get the instance and call the method
        return f(self, *args, **kwargs)
    # Add functor to zipline.api
    setattr(online_api, f.__name__, wrapped)
    # online_api.__all__.append(f.__name__)
    f.is_api_method = True
    return f

class RealtimeAlgorithm(object):

    def __init__(self,script=None,algo_filename=None,order_callback=None):
        self.algoscript = script
        self.namespace = {}
        self._order_callback = order_callback

        def noop(*args, **kwargs):
            pass

        if self.algoscript is not None:
            if algo_filename is None:
                algo_filename = '<string>'
            code = compile(self.algoscript, algo_filename, 'exec')
            exec_(code, self.namespace)

            self._initialize = self.namespace.get('initialize', noop)
            self._handle_data = self.namespace.get('handle_data', noop)
        else:
            self._initialize = None
            self._handle_data = None
            raise ValueError(
                    "Must have 'initialize' and 'handle_data' methods in algorithem file!"
                )

    def handle_data(self, data):
        if self._handle_data:
            self._handle_data(self, data)
            
    def initialize(self, *args, **kwargs):
        """
        Call self._initialize with `self` made available to Zipline API
        functions.
        """
        if self._initialize:
            self._initialize(self, *args, **kwargs)

    @api_method
    def order(self, data):
        # print(data)
        self._order_callback(data)

def decorator(method):
    @functools.wraps(method)
    def wrapped_method(self, *args, **kwargs):
        return method(self, *args, **kwargs)
    return wrapped_method



