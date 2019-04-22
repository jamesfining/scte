import base64
import bitstring
from scte.Scte35.TimeSignal import TimeSignal
from scte.Scte35.SpliceDescriptor import SpliceDescriptor
from scte.Scte35.SpliceNull import SpliceNull
from scte.Scte35.SpliceInsert import SpliceInsert
from scte.Scte35.SpliceSchedule import SpliceSchedule


class SpliceEvent:
    def __parse_splice_descriptors(self, descriptor_loop_length, bitarray_data):
        splice_descriptors = []
        bytes_left = descriptor_loop_length
        while bytes_left > 0:
            new_descriptor = SpliceDescriptor(bitarray_data).as_dict
            # Descriptor Length does not include splice_descriptor_tag
            bytes_left -= new_descriptor["descriptor_length"]+2
            splice_descriptors.append(new_descriptor)
        return splice_descriptors

    def __init__(self, b64_data):
        super(SpliceEvent, self).__init__()
        decoded_data = base64.standard_b64decode(b64_data)
        bitarray_data = bitstring.BitString(bytes=decoded_data)
        self.splice_info_section = {}
        self.splice_info_section["table_id"] = bitarray_data.read("uint:8")
        self.splice_info_section["section_syntax_indicator"] = bitarray_data.read("bool")
        self.splice_info_section["private"] = bitarray_data.read("bool")
        bitarray_data.pos += 2
        self.splice_info_section["section_length"] = bitarray_data.read("uint:12")
        self.splice_info_section["protocol_version"] = bitarray_data.read("uint:8")
        self.splice_info_section["encrypted_packet"] = bitarray_data.read("bool")
        self.splice_info_section["encryption_algorithm"] = bitarray_data.read("uint:6")
        self.splice_info_section["pts_adjustment"] = bitarray_data.read("uint:33")
        self.splice_info_section["cw_index"] = bitarray_data.read("uint:8")
        self.splice_info_section["tier"] = bitarray_data.read("hex:12")
        self.splice_info_section["splice_command_length"] = bitarray_data.read("uint:12")
        self.splice_info_section["splice_command_type"] = bitarray_data.read("uint:8")
        if self.splice_info_section["splice_command_type"] is 0:
            self.is_splice_null = True
            self.splice_info_section["splice_null"] = SpliceNull(bitarray_data)
        elif self.splice_info_section["splice_command_type"] is 4:
            self.is_splice_schedule = True
            self.splice_info_section["splice_schedule"] = SpliceSchedule(bitarray_data)
        elif self.splice_info_section["splice_command_type"] is 5:
            self.is_splice_insert = True
            self.splice_info_section["splice_insert"] = SpliceInsert(bitarray_data)
        elif self.splice_info_section["splice_command_type"] is 6:
            self.is_time_signal = True
            self.splice_info_section["time_signal"] = TimeSignal(bitarray_data)
        # Loop length is number of total bytes for descriptors
        self.splice_info_section["descriptor_loop_length"] = bitarray_data.read("uint:16")
        if self.splice_info_section["descriptor_loop_length"] > 0:
            self.splice_info_section["splice_descriptors"] = self.__parse_splice_descriptors(self.splice_info_section["descriptor_loop_length"], bitarray_data)
