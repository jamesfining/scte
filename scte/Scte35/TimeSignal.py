class TimeSignal:
    def __init__(self, bitarray_data):
        self.splice_time = {}
        self.splice_time["time_specified_flag"] = bitarray_data.read("bool")
        if self.splice_time["time_specified_flag"] is True:
            bitarray_data.pos += 6
            self.splice_time["pts_time"] = bitarray_data.read("uint:33")

    def __str__(self):
        return str(self.splice_time)

    def __repr__(self):
        return self.__str__()
