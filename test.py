#!/usr/bin/env
from scte import Scte35

s = Scte35.Scte35()

test_string = "/DBKAAAAAsrbAP/wBQb+PGICLAA0AjJDVUVJAAAAAX/TAALpzRwBHjAwMDM1TUEwMDAwMDAwMDAyMTZUMTAzMDE4MjAwMAEBAGl25uA="

myEvent = s.parse_splice_event(test_string)

print(myEvent.splice_info_section)
