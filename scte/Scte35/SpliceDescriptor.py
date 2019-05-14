import bitstring
from scte.Scte35 import SegmentationDescriptor


class SpliceDescriptor:
    def __init__(self, bitarray_data, init_dict=None):
        if init_dict:
            if 'reserved1' not in init_dict:
                init_dict['reserved1'] = 127
            if 'reserved2' not in init_dict:
                init_dict['reserved2'] = 31
            self.as_dict = init_dict
            return
        new_descriptor = {}
        new_descriptor["splice_descriptor_tag"] = bitarray_data.read("uint:8")
        new_descriptor["descriptor_length"] = bitarray_data.read("uint:8")
        if new_descriptor["splice_descriptor_tag"] not in [0, 1, 2, 3]:
            self.log.info("Skipping Unsupported splice_descriptor_tag: " + str(new_descriptor["splice_descriptor_tag"]))
        new_descriptor["identifier"] = bitarray_data.read("uint:32")
        if new_descriptor["splice_descriptor_tag"] is 0:
            # avail descriptor
            None
        elif new_descriptor["splice_descriptor_tag"] is 1:
            # DTMF Descriptor
            None
        elif new_descriptor["splice_descriptor_tag"] is 2:
            # SegmentationDescriptor
            new_descriptor.update(SegmentationDescriptor(bitarray_data).as_dict)
        elif new_descriptor["splice_descriptor_tag"] is 3:
            # Time Descriptor
            None
        self.as_dict = new_descriptor

    @classmethod
    def from_hex_string(cls, hex_string):
        bitarray_data = bitstring.BitString(bytes=bytes.fromhex(hex_string))
        return cls(bitarray_data)

    @classmethod
    def from_dict(cls, input_dict):
        # Need to do input checking here
        return cls(bitarray_data=None, init_dict=input_dict)

    @property
    def bitstring_format(self):
        bitstring_format = 'uint:8=splice_descriptor_tag,' \
                           'uint:8=descriptor_length,' \
                           'uint:32=identifier,' \
                           'uint:32=segmentation_event_id,' \
                           'bool=segmentation_event_cancel_indicator,' \
                           'uint:7=reserved1,'
        if self.as_dict['segmentation_event_cancel_indicator'] is False:
            bitstring_format += 'bool=program_segmentation_flag,' \
                                'bool=segmentation_duration_flag,' \
                                'bool=delivery_not_restricted_flag,'
            if self.as_dict['delivery_not_restricted_flag'] is False:
                bitstring_format += 'bool=web_delivery_allowed_flag,' \
                                    'bool=no_regional_blackout_flag,' \
                                    'bin:2=device_restrictions,'
            else:
                bitstring_format += 'uint:5=reserved2,'
            if self.as_dict['program_segmentation_flag'] is False:
                # Not supported yet
                None
            if self.as_dict['segmentation_duration_flag'] is True:
                bitstring_format += 'uint:40=segmentation_duration,'
            bitstring_format += 'uint:8=segmentation_upid_type,' \
                                'uint:8=segmentation_upid_length,' \
                                'bytes:' + str(self.as_dict['segmentation_upid_length']) + '=segmentation_upid,' \
                                                                                              'uint:8=segmentation_type_id,' \
                                                                                              'uint:8=segment_num,' \
                                                                                              'uint:8=segments_expected'
            if self.as_dict['segmentation_type_id'] in [0x34, 0x36]:
                bitstring_format += ',uint:8=sub_segment_num,' \
                                    'uint:8=sub_segments_expected'
        return bitstring_format

    def serialize(self):
        return bitstring.pack(fmt=self.bitstring_format, **self.as_dict)

    @property
    def hex_string(self):
        return self.serialize().hex.upper()

    def __str__(self):
        return str(self.as_dict)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_dict(cls, input_dict):
        # Need to do input checking here
        return cls(bitarray_data=None, init_dict=input_dict)
