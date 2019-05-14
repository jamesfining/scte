import bitstring

class TimeSignal:
    def __init__(self, bitarray_data, init_dict=None):
        if init_dict:
            self.splice_time = init_dict
            return

        self.splice_time = {}
        self.splice_time["time_specified_flag"] = bitarray_data.read("bool")
        if self.splice_time["time_specified_flag"] is True:
            bitarray_data.pos += 6
            self.splice_time["pts_time"] = bitarray_data.read("uint:33")

    def bitstring_format(self):
        bitstring_format = 'bool=time_specified_flag'

        if self.splice_time["time_specified_flag"] is True:
            bitstring_format += ',' + 'uint:6=0,' \
                                      'uint:33=pts_time'

        return bitstring_format

    def serialize(self):
        return bitstring.pack(fmt=self.bitstring_format(), **self.splice_time)


    def __str__(self):
        return str(self.splice_time)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_dict(cls, input_dict):
        # Need to do input checking here
        return cls(bitarray_data=None, init_dict=input_dict)
