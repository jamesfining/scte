import logging


class SpliceNull:
    def __init__(self, bitarray_data, logger=None):
        if logger is not None:
            self._log = logger
        else:
            self._log = logging.getLogger()
        None
