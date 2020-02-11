from scte.Scte35 import scte35_enums
import logging


class AvailDescriptor:
    def __init__(self, bitarray_data, logger=None):
        if logger is not None:
            self._log = logger
        else:
            self._log = logging.getLogger()
        new_descriptor = {}
        new_descriptor["provider_avail_id"] = bitarray_data.read("uint:32")
        self.as_dict = new_descriptor
