import bitstring
import base64
from scte import scte35_enums
import logging


class Scte35:

    def __init__(self):
        self.log = logging.getLogger()

    def parse_splice_event(self, b64_data):
        return SpliceEvent(b64_data)


class SpliceNull:
    def __init__(self, bitarray_data):
        None


class SpliceSchedule:
    def __init__(self, bitarray_data):
        None


class SpliceInsert:
    def __init__(self, bitarray_data):
        None


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


class SegmentationDescriptor:
    def __init__(self, bitarray_data):
        None


class SpliceEvent(Scte35):
    def __parse_splice_descriptors(self, descriptor_loop_length, bitarray_data):
        splice_descriptors = []
        bytes_left = descriptor_loop_length
        while bytes_left > 0:
            new_descriptor = {}
            new_descriptor["splice_descriptor_tag"] = bitarray_data.read("uint:8")
            bytes_left -= 1
            new_descriptor["descriptor_length"] = bitarray_data.read("uint:8")
            bytes_left -= 1
            if new_descriptor["splice_descriptor_tag"] not in [0, 1, 2, 3]:
                self.log.info("Skipping Unsupported splice_descriptor_tag: " + str(new_descriptor["splice_descriptor_tag"]))
                bytes_left -= new_descriptor["descriptor_length"]
                continue
            new_descriptor["identifier"] = bitarray_data.read("uint:32")
            bytes_left -= 4
            if new_descriptor["splice_descriptor_tag"] is 0:
                # avail descriptor
                None
            elif new_descriptor["splice_descriptor_tag"] is 1:
                # DTMF Descriptor
                None
            elif new_descriptor["splice_descriptor_tag"] is 2:
                new_descriptor["is_segmentation_descriptor"] = True
                new_descriptor["segmentation_event_id"] = bitarray_data.read("uint:32")
                bytes_left -= 4
                new_descriptor["segmentation_event_cancel_indicator"] = bitarray_data.read("bool")
                # Reserved
                bitarray_data.pos += 7
                bytes_left -= 1
                if new_descriptor["segmentation_event_cancel_indicator"] is False:
                    new_descriptor["program_segmentation_flag"] = bitarray_data.read("bool")
                    new_descriptor["segmentation_duration_flag"] = bitarray_data.read("bool")
                    new_descriptor["delivery_not_restricted_flag"] = bitarray_data.read("bool")
                    if new_descriptor["delivery_not_restricted_flag"] is False:
                        new_descriptor["web_delivery_allowed_flag"] = bitarray_data.read("bool")
                        new_descriptor["no_regional_blackout_flag"] = bitarray_data.read("bool")
                        new_descriptor["archive_allowed_flag"] = bitarray_data.read("bool")
                        new_descriptor["device_restrictions"] = bitarray_data.read("uint:2")
                        bytes_left -= 1
                    else:
                        # Reserved
                        bitarray_data.pos += 5
                    bytes_left -= 1
                    if new_descriptor["program_segmentation_flag"] is False:
                        new_descriptor["component_count"] = bitarray_data.read("uint:8")
                        bytes_left -= 1
                        loop_counter = new_descriptor["component_count"]
                        new_descriptor["components"] = []
                        while loop_counter > 0:
                            new_component = {}
                            new_component["component_tag"] = bitarray_data.read("uint:8")
                            bytes_left -= 1
                            # Reserved
                            bitarray_data.pos += 7
                            new_component["pts_offset"] = bitarray_data.read("uint:33")
                            bytes_left -= 5
                            new_descriptor["components"].append(new_component)
                    if new_descriptor["segmentation_duration_flag"] is True:
                        new_descriptor["segmentation_duration"] = bitarray_data.read("uint:40")
                        bytes_left -= 5
                    new_descriptor["segmentation_upid_type"] = bitarray_data.read("uint:8")
                    bytes_left -= 1
                    new_descriptor["segmentation_upid_length"] = bitarray_data.read("uint:8")
                    bytes_left -= 1
                    # UPID Parsing needs more work
                    upid_length_bits = new_descriptor["segmentation_upid_length"] * 8
                    new_descriptor["segmentation_upid"] = bitarray_data.read("uint:"+str(upid_length_bits))
                    bytes_left -= new_descriptor["segmentation_upid_length"]
                    new_descriptor["segmentation_type_id"] = bitarray_data.read("uint:8")
                    bytes_left -= 1
                    new_descriptor["segmentation_message"] = scte35_enums.get_message(new_descriptor["segmentation_type_id"])
                    new_descriptor["segment_num"] = bitarray_data.read("uint:8")
                    bytes_left -= 1
                    new_descriptor["segments_expected"] = bitarray_data.read("uint:8")
                    if new_descriptor["segmentation_type_id"] in [52, 54]:
                        new_descriptor["sub_segment_num"] = bitarray_data.read("uint:8")
                        bytes_left -= 1
                        new_descriptor["sub_segments_expected"] = bitarray_data.read("uint:8")
            elif new_descriptor["splice_descriptor_tag"] is 3:
                # Time Descriptor
                None
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
