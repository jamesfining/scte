import bitstring
import copy
from scte.Scte35 import SegmentationDescriptor, DTMFDescriptor, AvailDescriptor
import logging


class SpliceDescriptor:
    def __init__(self, bitarray_data, init_dict=None, logger=None):
        if logger is not None:
            self._log = logger
        else:
            self._log = logging.getLogger()
        if init_dict:
            if 'reserved1' not in init_dict:
                init_dict['reserved1'] = 1
            if 'reserved2' not in init_dict:
                init_dict['reserved2'] = 1
            self.__obj_dict = init_dict
            return
        new_descriptor = {}
        new_descriptor["splice_descriptor_tag"] = bitarray_data.read("uint:8")
        if new_descriptor["splice_descriptor_tag"] not in [0, 1, 2, 3]:
            self._log.info("Skipping Unsupported splice_descriptor_tag: " + str(new_descriptor["splice_descriptor_tag"]))
            self.__obj_dict = new_descriptor
            return

        new_descriptor["descriptor_length"] = bitarray_data.read("uint:8")
        
        new_descriptor["identifier"] = bitarray_data.read("uint:32")
        if new_descriptor["splice_descriptor_tag"] is 0:
            # avail descriptor
            new_descriptor.update(AvailDescriptor(bitarray_data).as_dict)
        elif new_descriptor["splice_descriptor_tag"] is 1:
            # DTMF Descriptor
            new_descriptor.update(DTMFDescriptor(bitarray_data).as_dict)
        elif new_descriptor["splice_descriptor_tag"] is 2:
            # SegmentationDescriptor
            new_descriptor.update(SegmentationDescriptor(bitarray_data).as_dict)
        elif new_descriptor["splice_descriptor_tag"] is 3:
            # Time Descriptor
            None
        self.__obj_dict = new_descriptor

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
                           'uint:7=1,'
        if self.__obj_dict['segmentation_event_cancel_indicator'] is False:
            bitstring_format += 'bool=program_segmentation_flag,' \
                                'bool=segmentation_duration_flag,' \
                                'bool=delivery_not_restricted_flag,'
            if self.__obj_dict['delivery_not_restricted_flag'] is False:
                bitstring_format += 'bool=web_delivery_allowed_flag,' \
                                    'bool=no_regional_blackout_flag,' \
                                    'bin:2=device_restrictions,'
            else:
                bitstring_format += 'uint:5=1,'
            if self.__obj_dict['program_segmentation_flag'] is False:
                # Not supported yet
                None
            if self.__obj_dict['segmentation_duration_flag'] is True:
                bitstring_format += 'uint:40=segmentation_duration,'
            bitstring_format += 'uint:8=segmentation_upid_type,' \
                                'uint:8=segmentation_upid_length,' \
                                'bytes:' + str(self.__obj_dict['segmentation_upid_length']) + '=segmentation_upid,' \
                                                                                              'uint:8=segmentation_type_id,' \
                                                                                              'uint:8=segment_num,' \
                                                                                              'uint:8=segments_expected'
            if self.__obj_dict['segmentation_type_id'] in [0x34, 0x36]:
                bitstring_format += ',uint:8=sub_segment_num,' \
                                    'uint:8=sub_segments_expected'
        return bitstring_format

    def serialize(self):
        return bitstring.pack(fmt=self.bitstring_format, **self.__obj_dict)

    @property
    def hex_string(self):
        return self.serialize().hex.upper()

    def as_dict(self, upid_as_str=False):
        the_dict = copy.deepcopy(self.__obj_dict)
        if upid_as_str:
            if "segmentation_upid" in the_dict:
                the_dict['segmentation_upid'] = \
                        str(the_dict['segmentation_upid'])
        return the_dict

    def __str__(self):
        return str(self.as_dict())

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_dict(cls, input_dict):
        # Need to do input checking here
        return cls(bitarray_data=None, init_dict=input_dict)
