from scte.Scte35 import scte35_enums
import logging


class DTMFDescriptor:
    def __init__(self, bitarray_data, logger=None):
        if logger is not None:
            self._log = logger
        else:
            self._log = logging.getLogger()
        new_descriptor = {}
        new_descriptor["preroll"] = bitarray_data.read("uint:8")
        new_descriptor["dtmf_count"] = bitarray_data.read("uint:3")
        # Reserved
        new_descriptor["reserved1"] = bitarray_data.read("uint:5")

        if new_descriptor["dtmf_count"] > 0:
            new_descriptor["DTMF_chars"] = []

            for _ in range(new_descriptor["dtmf_count"]):
                new_descriptor["DTMF_chars"].append(bitarray_data.read("uint:8"))
        self.as_dict = new_descriptor
