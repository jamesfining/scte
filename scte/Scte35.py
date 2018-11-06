import bitstring
import base64


class Scte35:

    def __init__(self, message_text=None):
        None

    def parse_splice_event(self, b64_data):
        return SpliceEvent(b64_data)


class SpliceEvent(Scte35):
    def __parse_splice_descriptors(self, descriptor_loop_length, bitarray_data):
        return None

    def __init__(self, b64_data):
        decoded_data = base64.standard_b64decode(b64_data)
        bitarray_data = bitstring.BitString(bytes=decoded_data)
        self.splice_info_section = {}
        self.splice_info_section.table_id = bitarray_data.read("uint:8")
        self.splice_info_section.section_syntax_indicator = bitarray_data.read("bool")
        self.splice_info_section.private = bitarray_data.read("bool")
        bitarray_data.pos += 2
        self.splice_info_section.section_length = bitarray_data.read("uint:12")
        self.splice_info_section.protocol_version = bitarray_data.read("uint:8")
        self.splice_info_section.encrypted_packet = bitarray_data.read("bool")
        self.splice_info_section.encryption_algorithm = bitarray_data.read("uint:6")
        self.splice_info_section.pts_adjustment = bitarray_data.read("uint:33")
        self.splice_info_section.cw_index = bitarray_data.read("uint:8")
        self.splice_info_section.tier = bitarray_data.read("hex:12")
        self.splice_info_section.splice_command_length = bitarray_data.read("uint:12")
        self.splice_info_section.splice_command_type = bitarray_data.read("uint:8")
        if self.splice_info_section.splice_command_type is 0:
            self.is_splice_null = True
            self.splice_null = SpliceNull(bitarray_data)
        elif self.splice_info_section.splice_command_type is 4:
            self.is_splice_schedule = True
            self.splice_schedule = SpliceSchedule(bitarray_data)
        elif self.splice_info_section.splice_command_type is 5:
            self.is_splice_insert = True
            self.splice_insert = SpliceInsert(bitarray_data)
        elif self.splice_info_section.splice_command_type is 6:
            self.is_time_signal = True
            self.time_signal = TimeSignal(bitarray_data)
        # Loop length is number of total bytes for descriptors
        self.splice_info_section.descriptor_loop_length = bitarray_data.read("uint:16")
        if self.splice_info_section.descriptor_loop_length > 0:
            self.splice_info_section.splice_descriptors = self.__parse_splice_descriptors(self.splice_info_section.descriptor_loop_length, bitarray_data)


class SpliceNull:
    def __init__(self, bitarray_data):
        None


class SpliceSchedule:
    def __init__(self, bitarray_data):
        None


class SpliceInsert:
    def __init__(self, bitarray_data):
        self.splice_time = {}
        self.splice_time.time_specified_flag = bitarray_data.read("bool")
        if self.splice_time.time_specified_flag is 1:
            bitarray_data.pos += 6
            self.splice_time.pts_time = bitarray_data.read("uint:33")


class TimeSignal:
    def __init__(self, bitarray_data):
        None


class SegmentationDescriptor:
    def __init__(self, bitarray_data):
        None
