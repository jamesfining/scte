#!/usr/bin/env
from scte.Scte35 import SpliceEvent, SpliceDescriptor

#test_string = "/DBIAAAAAsrbAP/wBQb/sbn3DQAyAjBDVUVJ/////3//AAAba98JHHVybjpuYmN1bmkuY29tOmJyYzozNTA3NTU4OTMxBQCk1C6w"

#test_string = "/DAzAAAAAAAAAP/wBQb/4z6IEgAdAhtDVUVJE8WAEH+/AwxUVk5BMTAwMDAwMDEQAACj2jGV"

#test_string = "/DAzAAAAAAAAAP/wBQb+M5DyeQAdAhtDVUVJAAABRX+/AwxUVk5BMTAwMDAwMDETAACr9xhM"

#Zero Length UPID
test_string = "/DA6AAAAAsrbAP/wBQb+Bp8k9gAkAiJDVUVJAAAAAX//AAE07tIBDkVQMDAwMDExODk0OTU0AQUAONWP9g=="

hex_descriptor = "021B43554549000000027FBF030C54564E413130303030303031300000"

myEvent = SpliceEvent(test_string)

print(myEvent.splice_info_section)

#descriptorObject = SpliceDescriptor.from_hex_string(hex_descriptor)

#print(descriptorObject.as_dict)

#print("serialized: " + descriptorObject.hex_string)
#print("original:   " + hex_descriptor)

descriptor_dictionary = {'splice_descriptor_tag': 2,
                         'descriptor_length': 27,
                         'identifier': 1129661769,
                         'segmentation_event_id': 2,
                         'segmentation_event_cancel_indicator': False,
                         'reserved1': 127,
                         'program_segmentation_flag': True,
                         'segmentation_duration_flag': False,
                         'delivery_not_restricted_flag': True,
                         'reserved2': 31,
                         'segmentation_upid_type': 3,
                         'segmentation_upid_length': 12,
                         'segmentation_upid': 26101077992648258395619471409,
                         'segmentation_type_id': 48,
                         'segmentation_message': 'Provider Advertisement Start',
                         'segment_num': 0,
                         'segments_expected': 0}

descObject2 = SpliceDescriptor.from_dict(descriptor_dictionary)

print("from dict:  "+descObject2.hex_string)
