from six import (
    exec_,
    iteritems,
    itervalues,
    string_types,
)

class RealtimeAlgorithm(object):

    def __init__(self,script=None,algo_filename=None):

        self.algoscript = script
        self.namespace = {}

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