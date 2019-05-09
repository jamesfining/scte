# TODO: Unused import
import bitstring
from scte.Scte104 import scte104_enums

def manipulate_bits(bit_array, value, position, bytes):
    hex_val = hex_string(value, bytes)
    bit_array.overwrite(hex_val, pos=position)
    return bytes*8


def hex_string(value, bytes):
    s = hex(value)
    return '0x' + s[2:].zfill(bytes*2)


## Not implemented
def init_request_data(bitarray_data):
    return None

## Not implemented
def init_request_data_encode(bitarray_data, event_object, position):
    return None


## Not implemented
def alive_request_data(bitarray_data):
    return None

def alive_request_data_encode(bitarray_data, event_object, position):
    return None


## Not implemented
def alive_response_data(bitarray_data):
    return None

## Not implemented
def alive_response_data_encode(bitarray_data, event_object, position):
    return None


def splice_request_data(bitarray_data):
    request_data = {}
    request_data["splice_insert_type"] = bitarray_data.read("uint:8")
    request_data["splice_event_id"] = bitarray_data.read("uint:32")
    request_data["unique_program_id"] = bitarray_data.read("uint:16")
    request_data["pre_roll_time"] = bitarray_data.read("uint:16")
    request_data["break_duration"] = bitarray_data.read("uint:16")
    request_data["avail_num"] = bitarray_data.read("uint:8")
    request_data["avails_expected"] = bitarray_data.read("uint:8")
    request_data["auto_return_flag"] = bitarray_data.read("uint:8")
    return request_data

def splice_request_data_encode(bitarray_data, event_object, position):
    position += manipulate_bits(bitarray_data, event_object["splice_insert_type"], position, bytes=1)
    position +=manipulate_bits(bitarray_data, event_object["splice_event_id"], position, bytes=4)
    position +=manipulate_bits(bitarray_data, event_object["unique_program_id"], position, bytes=2)
    position +=manipulate_bits(bitarray_data, event_object["pre_roll_time"], position, bytes=2)
    position +=manipulate_bits(bitarray_data, event_object["break_duration"], position, bytes=2)
    position +=manipulate_bits(bitarray_data, event_object["avail_num"], position, bytes=1)
    position +=manipulate_bits(bitarray_data, event_object["avails_expected"], position, bytes=1)
    position +=manipulate_bits(bitarray_data, event_object["auto_return_flag"], position, bytes=1)
    return None


def  encrypted_dpi_request_data(bitarray_data):
    request_data = {}
    request_data["encryption_algorithm"] = bitarray_data.read("uint:8")
    request_data["cw_index"] = bitarray_data.read("uint:8")
    return request_data

def  encrypted_dpi_request_data_encode(bitarray_data, event_object, position):
    return None


def update_control_word_data(bitarray_data):
    request_data= {}
    request_data["cw_index"] = bitarray_data.read("uint:8") 
    request_data["cw_a"] = bitarray_data.read("uint:64")
    request_data["cw_b"] = bitarray_data.read("uint:64")
    request_data["cw_c"] = bitarray_data.read("uint:64")
    return request_data

def update_control_word_data_encode(bitarray_data, event_object, position):
    return None


def delete_control_word_data(bitarray_data):
    request_data = {}
    request_data["cw_index"] = bitarray_data.read("uint:8")
    return request_data

def delete_control_word_data_encode(bitarray_data, event_object, position):
    return None


## Not implmented
def component_mode_dpi_request_data(bitarray_data):
    return None

## Not implmented
def component_mode_dpi_request_data_encode(bitarray_data, event_object, position):
    return None


## Not implemented
def start_schedule_download_request_data(bitarray_data):
    return None

## Not implemented
def start_schedule_download_request_data_encode(bitarray_data, event_object, position):
    return None

## Not implemented
def schedule_definition_data(bitarray_data):
    return None


## Not implemented
def schedule_definition_data_encode(bitarray_data, event_object, position):
    return None


## Not implemented
def schedule_component_mode_request_data(bitarray_data):
    return None

## Not implemented
def schedule_component_mode_request_data_encode(bitarray_data, event_object, position):
    return None


##Not implemented
def transmit_schedule_request_data(bitarray_data):
    return None


##Not implemented
def transmit_schedule_request_data_encode(bitarray_data, event_object, position):
    return None


def time_signal_request_data(bitarray_data):
    request_data = {}
    request_data["pre_roll_time"] = bitarray_data.read("uint:16")
    return request_data

def time_signal_request_data_encode(bitarray_data, event_object, position):
    position += manipulate_bits(bitarray_data, event_object["pre_roll_time"], position, bytes=2)
    return None


## Not implemented
def insert_avail_descriptor_request_data(bitarray_data):
    return None

## Not implemented
def insert_avail_descriptor_request_data_encode(bitarray_data, event_object, position):
    return None


## Not implemented
def insert_descriptor_request_data(bitarray_data):
    return None

## Not implemented
def insert_descriptor_request_data_encode(bitarray_data, event_object, position):
    return None


##Not implemented
def insert_DTMF_descriptor_request_data(bitarray_data):
    return None

def insert_DTMF_descriptor_request_data_encode(bitarray_data, event_object, position):
    return None


##Not implemented
def insert_segmentation_descriptor_request_data(bitarray_data):
    return None

def insert_segmentation_descriptor_request_data_encode(bitarray_data, event_object, position):
    return None


##Not implemented
def proprietary_command_request_data(bitarray_data):
    return None

##Not implemented
def proprietary_command_request_data_encode(bitarray_data, event_object, position):
    return None


def splice_null_request_data(bitarray_data):
    return {}

def splice_null_request_data_encode(bitarray_data, event_object, position):
    return {}


def inject_section_data_request(bitarray_data):
    request_data = {}
    request_data["scte35_command_length"] = bitarray_data.read("uint:16")
    request_data["scte35_protocol_version"] = bitarray_data.read("uint:8")
    request_data["scte35_command_length"] = bitarray_data.read("uint:8")
    request_data["scte35_command_contents"] = bitarray_data.read("uint" + str(request_data["scte35_command_length"]))
    return request_data

def inject_section_data_request_encode(bitarray_data, event_object, position):
    return None


def insert_avail_descriptor_request_data(bitarray_data):
    request_data = {}
    request_data["num_provider_avails"] = bitarray_data.read("uint:8")
    request_data["avails"] = []
    [request_data["avails"].append(bitarray_data.read("uint:32")) for i in range(request_data["num_provider_avails"])]
    return

def insert_avail_descriptor_request_data_encode(bitarray_data, event_object, position):
    return None

def insert_segmentation_descriptor_request_data(bitarray_data):
    request = {}
    
    try:
        request["segmentation_event_id"] = bitarray_data.read("uint:32")
        request["segmentation_event_cancel_indicator"] = bitarray_data.read("uint:8")
        request["duration"] = bitarray_data.read("uint:16")
        request["segmentation_upid_type"] = bitarray_data.read("uint:8")
        request["segmentation_upid_length"] = bitarray_data.read("uint:8")
        request["segmentation_upid"] = bitarray_data.read("uint:" + str(request["segmentation_upid_length"]*8))
        request["segmentation_type_id"] = {"decimal": bitarray_data.read("uint:8")}
        request["segmentation_type_id"]["name"] = scte104_enums.get_segmentation_type(request["segmentation_type_id"]["decimal"])
        request["segment_num"] = bitarray_data.read("uint:8")
        request["segments_expected"] = bitarray_data.read("uint:8")
        request["duration_extension_frames"] = bitarray_data.read("uint:8")
        request["delivery_not_restricted_flag"] = bitarray_data.read("uint:8")
        request["web_delivery_allowed_flag"] = bitarray_data.read("uint:8")
        request["no_regional_blackout_flag"] = bitarray_data.read("uint:8")
        request["archive_allowed_flag"] = bitarray_data.read("uint:8")
        request["device_restrictions"] = bitarray_data.read("uint:8")
        request["insert_sub_segment_info"] = bitarray_data.read("uint:8")
        request["sub_segment_num"] = bitarray_data.read("uint:8")
        request["sub_segments_expected"] = bitarray_data.read("uint:8")
    except:
        return request
    return request

def insert_segmentation_descriptor_request_data_encode(bitarray_data, event_object, position):
    position += manipulate_bits(bitarray_data, event_object["segmentation_event_id"], position, bytes=4)
    position += manipulate_bits(bitarray_data, event_object["segmentation_event_cancel_indicator"], position, bytes=1)
    position += manipulate_bits(bitarray_data, event_object["duration"], position, bytes=2)
    position += manipulate_bits(bitarray_data, event_object["segmentation_upid_type"], position, bytes=1)
    position += manipulate_bits(bitarray_data, event_object["segmentation_upid_length"], position, bytes=1)
    position += manipulate_bits(bitarray_data, event_object["segmentation_upid"], position, bytes=event_object["segmentation_upid_length"])
    position += manipulate_bits(bitarray_data, event_object["segmentation_type_id"]["decimal"], position, bytes=1)
    position += manipulate_bits(bitarray_data, event_object["segment_num"], position, bytes=1)
    position += manipulate_bits(bitarray_data, event_object["segments_expected"], position, bytes=1)
    position += manipulate_bits(bitarray_data, event_object["duration_extension_frames"], position, bytes=1)
    position += manipulate_bits(bitarray_data, event_object["delivery_not_restricted_flag"], position, bytes=1)
    position += manipulate_bits(bitarray_data, event_object["web_delivery_allowed_flag"], position, bytes=1)
    position += manipulate_bits(bitarray_data, event_object["no_regional_blackout_flag"], position, bytes=1)
    position += manipulate_bits(bitarray_data, event_object["archive_allowed_flag"], position, bytes=1)
    position += manipulate_bits(bitarray_data, event_object["device_restrictions"], position, bytes=1)
    if "insert_sub_segment_info" in event_object.keys():
        position += manipulate_bits(bitarray_data, event_object["insert_sub_segment_info"], position, bytes=1)
    if "sub_segment_num" in event_object.keys():
        position += manipulate_bits(bitarray_data, event_object["sub_segment_num"], position, bytes=1)
    if "sub_segments_expected" in event_object.keys():
        position += manipulate_bits(bitarray_data, event_object["sub_segments_expected"], position, bytes=1)
    return None

## Not implemented
def proprietary_cmmand_request_data(bitarray_data):
    return None

def proprietary_cmmand_request_data_encode(bitarray_data, event_object, position):
    return None


def insert_tier_data(bitarray_data):
    return {"insert_tier_data": bitarray_data.read("uint:16")}

def insert_tier_data_encode(bitarray_data, event_object, position):
    position += manipulate_bits(bitarray_data, event_object["insert_tier_data"], position, bytes=2)
    return None


## Not implemented
def insert_time_descriptor(bitarray_data):
    return None

## Not implemented
def insert_time_descriptor_encode(bitarray_data, value, position):
    return None


##Not implemented
def reserved(bitarray_data):
    return None

##Not implemented
def reserved_encode(bitarray_data, value, position):
    return None
