#!/usr/bin/env
from scte import Scte35

s = Scte35()

#test_string = "/DBIAAAAAsrbAP/wBQb/sbn3DQAyAjBDVUVJ/////3//AAAba98JHHVybjpuYmN1bmkuY29tOmJyYzozNTA3NTU4OTMxBQCk1C6w"
test_string = "/DAxAAAAAAAAAP/wFAUAAAAAf+/+B/bDv/4AUmXAAAEAAAAMAQpDVUVJUIAxMjEqiqDixg=="

hex_descriptor = "021B43554549000000027FBF030C54564E413130303030303031300000"


myEvent = s.parse_splice_event(test_string)

print(myEvent.splice_info_section)

descriptorObject = s.parse_segmentation_descriptor(hex_descriptor)

print(descriptorObject.as_dict)

print("serialized: " + descriptorObject.hex_string)
print("original:   " + hex_descriptor)
