#!/usr/bin/env
from scte.Scte35 import SpliceEvent, SpliceDescriptor

#test_string = "/DBIAAAAAsrbAP/wBQb/sbn3DQAyAjBDVUVJ/////3//AAAba98JHHVybjpuYmN1bmkuY29tOmJyYzozNTA3NTU4OTMxBQCk1C6w"

#test_string = "/DAzAAAAAAAAAP/wBQb/4z6IEgAdAhtDVUVJE8WAEH+/AwxUVk5BMTAwMDAwMDEQAACj2jGV"

#test_string = "/DAzAAAAAAAAAP/wBQb+M5DyeQAdAhtDVUVJAAABRX+/AwxUVk5BMTAwMDAwMDETAACr9xhM"

#Zero Length UPID
test_string = "/DA6AAAAAsrbAP/wBQb+Bp8k9gAkAiJDVUVJAAAAAX//AAE07tIBDkVQMDAwMDExODk0OTU0AQUAONWP9g=="

myEvent = SpliceEvent(test_string)

print("event from b64 : " + str(myEvent.splice_info_section))


hx = myEvent.hex_string
print("hex of event from b64: " + hx)

myEvent = SpliceEvent.from_hex_string(hx)
print("formed from hex: " + str(myEvent.splice_info_section))


hex_descriptor = "021B43554549000000027FBF030C54564E413130303030303031300000"

descriptorObject = SpliceDescriptor.from_hex_string(hex_descriptor)

print(descriptorObject.as_dict)

print("serialized: " + descriptorObject.hex_string)
print("original:   " + hex_descriptor)



descriptor_dictionary = {'splice_descriptor_tag': 2,
                         'descriptor_length': 27,
                         'identifier': 1129661769,
                         'segmentation_event_id': 2,
                         'segmentation_event_cancel_indicator': False,
                         'program_segmentation_flag': True,
                         'segmentation_duration_flag': False,
                         'delivery_not_restricted_flag': True,
                         'segmentation_upid_type': 3,
                         'segmentation_upid_length': 12,
                         'segmentation_upid': b'EP9990118900',
                         'segmentation_type_id': 48,
                         'segmentation_message': 'Provider Advertisement Start',
                         'segment_num': 0,
                         'segments_expected': 0}

descObject2 = SpliceDescriptor.from_dict(descriptor_dictionary)

print("hex desc from dict:  "+descObject2.hex_string)



event_dictionary = {'table_id': 252, 'section_syntax_indicator': False, 'private': False, 'section_length': 72, 'protocol_version': 0, 'encrypted_packet': False, 'encryption_algorithm': 0, 'pts_adjustment': 183003, 'cw_index': 0, 'tier': '000', 'splice_command_length': 5, 'splice_command_type': 6, 'time_signal': {'time_specified_flag': True, 'pts_time': 3588538282}, 'descriptor_loop_length': 50,
        'splice_descriptors': [ {'splice_descriptor_tag': 2,
            'descriptor_length': 48,
            'identifier': 1129661769,
            'is_segmentation_descriptor': True,
            'segmentation_event_id': 4294967295,
            'segmentation_event_cancel_indicator': False,
            'program_segmentation_flag': True,
            'segmentation_duration_flag': True,
            'delivery_not_restricted_flag': True,
            'segmentation_duration': 1350020,
            'segmentation_upid_type': 9,
            'segmentation_upid_length': 12,
            'segmentation_upid': b'EP9990118900',
            'segmentation_type_id': 48,
            'segmentation_message': 'Provider Advertisement Start',
            'segment_num': 3,
            'segments_expected': 3}]}

eventObject2 = SpliceEvent.from_dict(event_dictionary)

print("event from dict:  " + str(eventObject2.splice_info_section))
