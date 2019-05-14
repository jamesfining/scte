from scte.Scte35 import scte35_enums


class SegmentationDescriptor:
    def __init__(self, bitarray_data):
        new_descriptor = {}
        new_descriptor["segmentation_event_id"] = bitarray_data.read("uint:32")
        new_descriptor["segmentation_event_cancel_indicator"] = bitarray_data.read("bool")
        # Reserved
        new_descriptor["reserved1"] = bitarray_data.read("uint:7")
        if new_descriptor["segmentation_event_cancel_indicator"] is False:
            new_descriptor["program_segmentation_flag"] = bitarray_data.read("bool")
            new_descriptor["segmentation_duration_flag"] = bitarray_data.read("bool")
            new_descriptor["delivery_not_restricted_flag"] = bitarray_data.read("bool")
            if new_descriptor["delivery_not_restricted_flag"] is False:
                new_descriptor["web_delivery_allowed_flag"] = bitarray_data.read("bool")
                new_descriptor["no_regional_blackout_flag"] = bitarray_data.read("bool")
                new_descriptor["archive_allowed_flag"] = bitarray_data.read("bool")
                new_descriptor["device_restrictions"] = bitarray_data.read("bin:2")
            else:
                # Reserved
                new_descriptor["reserved2"] = bitarray_data.read("uint:5")
            if new_descriptor["program_segmentation_flag"] is False:
                new_descriptor["component_count"] = bitarray_data.read("uint:8")
                loop_counter = new_descriptor["component_count"]
                new_descriptor["components"] = []
                while loop_counter > 0:
                    new_component = {}
                    new_component["component_tag"] = bitarray_data.read("uint:8")
                    # Reserved
                    bitarray_data.pos += 7
                    new_component["pts_offset"] = bitarray_data.read("uint:33")
                    new_descriptor["components"].append(new_component)
            if new_descriptor["segmentation_duration_flag"] is True:
                new_descriptor["segmentation_duration"] = bitarray_data.read("uint:40")
            new_descriptor["segmentation_upid_type"] = bitarray_data.read("uint:8")
            new_descriptor["segmentation_upid_length"] = bitarray_data.read("uint:8")
            # UPID Parsing needs more work
            if new_descriptor["segmentation_upid_length"] > 0:
                new_descriptor["segmentation_upid"] = bitarray_data.read("bytes:" + str(new_descriptor["segmentation_upid_length"]))
            new_descriptor["segmentation_type_id"] = bitarray_data.read("uint:8")
            new_descriptor["segmentation_message"] = scte35_enums.get_message(
                new_descriptor["segmentation_type_id"])
            new_descriptor["segment_num"] = bitarray_data.read("uint:8")
            new_descriptor["segments_expected"] = bitarray_data.read("uint:8")
            if new_descriptor["segmentation_type_id"] in [52, 54]:
                new_descriptor["sub_segment_num"] = bitarray_data.read("uint:8")
                new_descriptor["sub_segments_expected"] = bitarray_data.read("uint:8")
        self.as_dict = new_descriptor
