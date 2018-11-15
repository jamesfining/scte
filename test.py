#!/usr/bin/env
from scte import Scte35

s = Scte35.Scte35()

test_string = "/DBIAAAAAsrbAP/wBQb/sbn3DQAyAjBDVUVJ/////3//AAAba98JHHVybjpuYmN1bmkuY29tOmJyYzozNTA3NTU4OTMxBQCk1C6w"

myEvent = s.parse_splice_event(test_string)

print(myEvent.splice_info_section)
