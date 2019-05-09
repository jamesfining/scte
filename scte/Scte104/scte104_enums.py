from scte.Scte104 import read_splice_event


def read_data(op_id, bitarray_data):
    op_data = __op_ids_multi_op[op_id]
    if not op_data: return None

    parse_function = op_data["decode_function"]
    return parse_function(bitarray_data)

def encode_data(op_id, bitarray_data, event_object, position):
    op_data = __op_ids_multi_op[op_id]
    if not op_data: return None

    encode_function = op_data["encode_function"]
    return encode_function(bitarray_data, event_object, position)

def get_op_id_type(op_id):
    if op_id >= 0x0013 and op_id <= 0x00FF: return "RESERVED FOR FUTURE BASIC REQUESTS"
    if op_id >= 0x0100 and op_id <= 0x7FFF: return "Reserved"
    if op_id >= 0x8000 and op_id <= 0xBFFF: return "User Defined"
    if op_id >= 0xC000 and op_id <= 0xFFFE: return "Reserved"
    return __op_ids_single_op[op_id]["type"]


def get_op_id_type_from_hex_string(hex_string):
    return __op_ids_single_op[int(hex_string, 16)]["type"]


def get_multi_op_id_type(op_id):
    if op_id >= 0x0000 and op_id <= 0x00FF: return "Reserved"
    if op_id >= 0x0111 and op_id <= 0x02FF: return "Reserved"
    if op_id >= 0x0302 and op_id <= 0x7FFF: return "Reserved"
    if op_id >= 0x8000 and op_id <= 0xBFFF: return "Reserved"
    if op_id >= 0xC000 and op_id <= 0xFFFE: return "User"
    return __op_ids_multi_op[op_id]["type"]


# TODO: get_multi_message_type is undefined
def get_multi_op_id_type_string(hex_string):
    return None
    #return get_multi_message_type(int(hex_string, 16))


def get_segmentation_type(type_id):
    return __segmentation_type_ids[type_id]["message"]


# TODO: The functions above can't access these objects. Move them to top of file
__op_ids_single_op = {
    0x0000: {
        "type": "general_response_data"
    },
    0x0001: {
        "type": "init_request_data"
    },
    0x0002: {
        "type": "init_response_data"
    },
    0x0003: {
        "type": "alive_request_data"
    },
    0x0004: {
        "type": "alive_response_data"
    },
    0x0005: {
        "type": "User Defined"
    },
    0x0006: {
        "type": "User Defined"
    },
    0x0007: {
        "type": "inject_response_data"
    },
    0x00008: {
        "type": "inject_complete_response_data"
    },
    0x0009: {
        "type": "config_request_data"
    },
    0x000A: {
        "type": "config_response_data"
    },
    0x000B: {
        "type": "provisioning_request_data"
    },
    0x000C: {
        "type": "provisioning_response_data"
    },
    0x000D: {
        "type": "Reserved"
    },
    0x000E: {
        "type": "Reserved"
    },
    0x000F: {
        "type": "fault_request_data"
    },
    0x0010: {
        "type": "fault_response_data"
    },
    0x0011: {
        "type": "AS_alive_request_data"
    },
    0x0012: {
        "type": "AS_alive_response_data"
    },

    0xFFFF: {
        "type": "Reserved for multiple operations"
    }
}

__op_ids_multi_op = {
    0x0100: {
        "type": "inject_section_data_request",
        "decode_function": read_splice_event.inject_section_data_request,
        "encode_function": read_splice_event.inject_section_data_request_encode},
    0x0101: {
        "type": "splice_request_data",
        "decode_function": read_splice_event.splice_request_data,
        "encode_function": read_splice_event.splice_request_data_encode},
    0x0102: {
        "type": "splice_null_request_data",
        "decode_function": read_splice_event.splice_null_request_data,
        "encode_function": read_splice_event.splice_null_request_data_encode},
    0x0103: {
        "type": "start_schedule_download_request_data",
        "decode_function": read_splice_event.start_schedule_download_request_data,
        "encode_function": read_splice_event.start_schedule_download_request_data_encode},
    0x0104: {
        "type": "time_signal_request_data",
        "decode_function": read_splice_event.time_signal_request_data,
        "encode_function": read_splice_event.time_signal_request_data_encode},
    0x0105: {
        "type": "transmit_schedule_request_data",
        "decode_function": read_splice_event.transmit_schedule_request_data,
        "encode_function": read_splice_event.transmit_schedule_request_data_encode},
    0x0106: {
        "type": "component_mode_dpi_request_data",
        "decode_function": read_splice_event.component_mode_dpi_request_data,
        "encode_function": read_splice_event.component_mode_dpi_request_data_encode},
    0x0107: {
        "type": "encrypted_dpi_request_data",
        "decode_function": read_splice_event.encrypted_dpi_request_data,
        "encode_function": read_splice_event.encrypted_dpi_request_data_encode},
    0x0108: {
        "type": "insert_descriptor_request_data",
        "decode_function": read_splice_event.insert_descriptor_request_data,
        "encode_function": read_splice_event.insert_descriptor_request_data_encode},
    0x0109: {
        "type": "insert_DTMF_descriptor_request_data",
        "decode_function": read_splice_event.insert_DTMF_descriptor_request_data,
        "encode_function": read_splice_event.insert_DTMF_descriptor_request_data_encode},
    0x010A: {
        "type": "insert_avail_descriptor_request_data",
        "decode_function": read_splice_event.insert_avail_descriptor_request_data,
        "encode_function": read_splice_event.insert_avail_descriptor_request_data_encode},
    0x010B: {
        "type": "insert_segmentation_descriptor_request_data",
        "decode_function": read_splice_event.insert_segmentation_descriptor_request_data,
        "encode_function": read_splice_event.insert_segmentation_descriptor_request_data_encode},
    0x010C: {
        "type": "proprietary_command_request_data",
        "decode_function": read_splice_event.proprietary_command_request_data,
        "encode_function": read_splice_event.proprietary_command_request_data_encode},
    0x010D: {
        "type": "schedule_component_mode_request_data",
        "decode_function": read_splice_event.schedule_component_mode_request_data,
        "encode_function": read_splice_event.schedule_component_mode_request_data_encode},
    0x010E: {
        "type": "schedule_definition_data",
        "decode_function": read_splice_event.schedule_definition_data,
        "encode_function": read_splice_event.schedule_definition_data_encode},
    0x010F: {
        "type": "insert_tier_data",
        "decode_function": read_splice_event.insert_tier_data,
        "encode_function": read_splice_event.insert_tier_data_encode},
    0x0110: {
        "type": "insert_time_descriptor",
        "decode_function": read_splice_event.insert_time_descriptor,
        "encode_function": read_splice_event.insert_time_descriptor_encode},
    0x0300: {
        "type": "delete_control_word_data",
        "decode_function": read_splice_event.delete_control_word_data,
        "encode_function": read_splice_event.delete_control_word_data_encode},
    0x0301: {
        "type": "update_control_word_data",
        "decode_function": read_splice_event.update_control_word_data,
        "encode_function": read_splice_event.update_control_word_data_encode},
    0xFFFF: {
        "type": "Reserved",
        "decode_function": read_splice_event.reserved,
        "encode_function": read_splice_event.reserved_encode}
}

__segmentation_type_ids = {
    0: {
        "message": "Not Indicated"
    },
    1: {
        "message": "Content Identification"
    },
    16: {
        "message": "Program Start"
    },
    17: {
        "message": "Program End"
    },
    18: {
        "message": "Program Early Termination"
    },
    19: {
        "message": "Program Breakaway"
    },
    20: {
        "message": "Program Resumption"
    },
    21: {
        "message": "Program Runover Planned"
    },
    22: {
        "message": "Program Runover Unplanned"
    },
    23: {
        "message": "Program Overlap Start"
    },
    24: {
        "message": "Program Blackout Override"
    },
    25: {
        "message": "Program Start - In Progress"
    },
    32: {
        "message": "Chapter Start"
    },
    33: {
        "message": "Chapter End"
    },
    34: {
        "message": "Break Start"
    },
    35: {
        "message": "Break End"
    },
    48: {
        "message": "Provider Advertisement Start"
    },
    49: {
        "message": "Provider Advertisement End"
    },
    50: {
        "message": "Distributor Advertisement Start"
    },
    51: {
        "message": "Distributor Advertisement End"
    },
    52: {
        "message": "Provider Placement Opportunity Start"
    },
    53: {
        "message": "Provider Placement Opportunity End"
    },
    54: {
        "message": "Distributor Placement Opportunity Start"
    },
    55: {
        "message": "Distributor Placement Opportunity End"
    },
    64: {
        "message": "Unscheduled Event Start"
    },
    65: {
        "message": "Unscheduled Event End"
    },
    80: {
        "message": "Network Start"
    },
    81: {
        "message": "Network End"
    }
}
