import logging
import copy
import bitstring

class SpliceInsert:
    def __init__(self, bitarray_data, init_dict=None, logger=None):
        if logger is not None:
            self._log = logger
        else:
            self._log = logging.getLogger()

        if init_dict:
            self.splice_insert = init_dict
            return

        self.splice_insert = {}

        self.splice_insert['splice_event_id'] = bitarray_data.read("uint:32")
        self.splice_insert['splice_event_cancel_indicator'] = bitarray_data.read("bool")

        bitarray_data.pos += 7

        if not self.splice_insert['splice_event_cancel_indicator']:
            self.splice_insert['out_of_network_indicator'] = bitarray_data.read("bool")
            self.splice_insert['program_splice_flag'] = bitarray_data.read("bool")
            self.splice_insert['duration_flag'] = bitarray_data.read("bool")
            self.splice_insert['splice_immediate_flag'] = bitarray_data.read("bool")

            bitarray_data.pos += 4

            if self.splice_insert['program_splice_flag'] and not self.splice_insert['splice_immediate_flag']:
                self.splice_insert['splice_time'] = self.splice_time(bitarray_data)

            if not self.splice_insert['program_splice_flag']:
                self.splice_insert['component_count'] = bitarray_data.read("uint:8")
                self.splice_insert['components'] = []

                for _ in range(self.splice_insert['component_count']):
                    component = {}
                    component['component_tag'] = bitarray_data.read("uint:8")

                    if not self.splice_insert['splice_immediate_flag']:
                        component['splice_time'] = self.splice_time(bitarray_data)

                    self.splice_insert['components'].append(component)

            if self.splice_insert['duration_flag']:
                self.splice_insert['break_duration'] = self.break_duration(bitarray_data)

            self.splice_insert['unique_program_id'] = bitarray_data.read("uint:16")
            self.splice_insert['avail_num'] = bitarray_data.read("uint:8")
            self.splice_insert['avails_expected'] = bitarray_data.read("uint:8")

    def break_duration(self, bitarray_data):
        break_duration = {}
        break_duration["auto_return"] = bitarray_data.read("bool")

        bitarray_data.pos += 6

        break_duration["duration"] = bitarray_data.read("uint:33")

        return break_duration

    def splice_time(self, bitarray_data):
        splice_time = {}
        splice_time["time_specified_flag"] = bitarray_data.read("bool")

        if splice_time["time_specified_flag"]:
            bitarray_data.pos += 6
            splice_time["pts_time"] = bitarray_data.read("uint:33")
        else:
            bitarray_data.pos += 7

        return splice_time


    def splice_time_bitstring_format(self, splice_time_obj):
        bitstring_format = 'bool=time_spec'
        return bitstring_format


    def splice_time_serialize(self):
        return


    @property
    def bitstring_format(self):
        """
        Return a formatted string representing the object for use by the bitstring library.
        """
        bitstring_format = 'uint:32=splice_event_id,' \
                           'bool=splice_event_cancel_indicator,' \
                           'uint:7=1'
        if self.splice_insert["splice_event_cancel_indicator"]:
            return bitstring_format
        else:
            bitstring_format += ',' \
                                'bool=out_of_network_indicator,' \
                                'bool=program_splice_flag,' \
                                'bool=duration_flag,' \
                                'bool=splice_immediate_flag,' \
                                'uint:4=1,'
        if self.splice_insert['program_splice_flag'] and not self.splice_insert['splice_immediate_flag']:
            bitstring_format += 'bool='
                                


    def serialize(self):
        return bitstring.pack(fmt=self.bitstring_format(), **self.splice_insert)

    @property
    def as_dict(self):
        return copy.deepcopy(self.splice_insert)

    def __str__(self):
        return str(self.splice_insert)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_dict(cls, input_dict):
        # Need to do input checking here
        return cls(bitarray_data=None, init_dict=input_dict)
