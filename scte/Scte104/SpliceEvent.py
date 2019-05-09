from scte.Scte104 import scte104_enums
import bitstring
import json
byte_size = 8

class SpliceEvent:
    def __init__(self, bitarray_data, init_dict=None):
        if init_dict is not None:
            self.message_dict = init_dict
            return
        message_dict = {}
        message_dict["reserved"] = {"raw": bitarray_data.read("uint:16")}
        message_dict["reserved"]["type"] = scte104_enums.get_op_id_type(message_dict["reserved"]["raw"])
        message_dict["message_size"] = bitarray_data.read("uint:16")
        message_dict["protocol_version"] = bitarray_data.read("uint:8")        
        message_dict["as_index"] = bitarray_data.read("uint:8")
        message_dict["message_number"] = bitarray_data.read("uint:8")
        message_dict["dpi_pid_index"] = bitarray_data.read("uint:16")
        message_dict["scte35_protocol_version"] = bitarray_data.read("uint:8")
        message_dict["timestamp"] = {}
        message_dict["timestamp"]["time_type"] = bitarray_data.read("uint:8")
        
        if message_dict["timestamp"]["time_type"] == 1:
            message_dict["timestamp"]["UTC_seconds"] = bitarray_data.read("uint:32")
            message_dict["timestamp"]["UTC_microseconds"] = bitarray_data.read("uint:16")
        elif message_dict["timestamp"]["time_type"] == 2:
            message_dict["timestamp"]["hours"] = bitarray_data.read("uint:8")
            message_dict["timestamp"]["minutes"] = bitarray_data.read("uint:8")
            message_dict["timestamp"]["seconds"] = bitarray_data.read("uint:8")
            message_dict["timestamp"]["frames"] = bitarray_data.read("uint:8")
        elif message_dict["timestamp"]["time_type"] == 3:
            message_dict["timestamp"]["GP_number"] = bitarray_data.read("uint:8")
            message_dict["timestamp"]["GP_edge"] = bitarray_data.read("uint:8")
        message_dict["num_ops"] = bitarray_data.read("uint:8")
        message_dict["ops"] = []
        for index in range(message_dict["num_ops"]):
            message_dict["ops"].append({})
            message_dict["ops"][index]["op_id"] = bitarray_data.read("uint:16")
            message_dict["ops"][index]["type"] = scte104_enums.get_multi_op_id_type(message_dict["ops"][index]["op_id"])
            message_dict["ops"][index]["data_length"] = bitarray_data.read("uint:16")
            bit_subdata = bitstring.BitString(bytes=bytes.fromhex(bitarray_data.read("hex:" + str(message_dict["ops"][index]["data_length"]*byte_size))))
            message_dict["ops"][index]["data"] = scte104_enums.read_data(message_dict["ops"][index]["op_id"], bit_subdata) 
        self.as_dict = message_dict

    def print(self):
        print(json.dumps(self.as_dict, indent=4, sort_keys=False))

    def print_detailed(self):
        print("reserved", hex(self.as_dict['reserved']['raw']), self.as_dict['reserved']['type'])
        print("message_size", hex(self.as_dict['message_size']), self.as_dict['message_size'])
        print("protocol_version", hex(self.as_dict['protocol_version']), self.as_dict['protocol_version'])
        print("as_index", hex(self.as_dict['as_index']), self.as_dict['as_index'])
        print("message_number", hex(self.as_dict['message_number']), self.as_dict['message_number'])
        print("dpi_pid_index", hex(self.as_dict['dpi_pid_index']), self.as_dict['dpi_pid_index'])
        print("scte35_protocol_version", hex(self.as_dict['scte35_protocol_version']), self.as_dict['scte35_protocol_version'])
        print("timestamp", hex(self.as_dict['timestamp']["time_type"]), self.as_dict['timestamp']["time_type"])
        print("num_ops", hex(self.as_dict['num_ops']), self.as_dict['num_ops'])
        for key in self.as_dict['ops']:
            print("op_id", hex(self.as_dict['ops'][key]["op_id"]), self.as_dict['ops'][key]["op_id"], self.as_dict['ops'][key]["type"])
            print("data_length", hex(self.as_dict['ops'][key]["data_length"]), self.as_dict['ops'][key]["data_length"])
            print("data", self.as_dict['ops'][key]["data"])
                
    def to_binary(self):
        self.position = 0
        bit_array = bitstring.BitArray(length=self.as_dict["message_size"]*byte_size)
        self.manipulate_bits(bit_array, self.as_dict["reserved"]["raw"], bytes=2)
        self.manipulate_bits(bit_array, self.as_dict["message_size"], bytes=2)
        self.manipulate_bits(bit_array, self.as_dict["protocol_version"], bytes=1)
        self.manipulate_bits(bit_array, self.as_dict["as_index"], bytes=1)
        self.manipulate_bits(bit_array, self.as_dict["message_number"], bytes=1)
        self.manipulate_bits(bit_array, self.as_dict["dpi_pid_index"], bytes=2)
        self.manipulate_bits(bit_array, self.as_dict["scte35_protocol_version"], bytes=1)
        self.manipulate_bits(bit_array, self.as_dict["timestamp"]["time_type"], bytes=1) ##timestamp

        if self.as_dict["timestamp"]["time_type"] == 1:
            self.manipulate_bits(bit_array, self.as_dict["timestamp"]["UTC_seconds"], bytes=4)
            self.manipulate_bits(bit_array, self.as_dict["timestamp"]["UTC_microseconds"], bytes=2)
        elif self.as_dict["timestamp"]["time_type"] == 2:
            self.manipulate_bits(bit_array, self.as_dict["timestamp"]["hours"], bytes=1)
            self.manipulate_bits(bit_array, self.as_dict["timestamp"]["minutes"], bytes=1)
            self.manipulate_bits(bit_array, self.as_dict["timestamp"]["seconds"], bytes=1)
            self.manipulate_bits(bit_array, self.as_dict["timestamp"]["frames"], bytes=1)
        elif self.as_dict["timestamp"]["time_type"] == 3:
            self.manipulate_bits(bit_array, self.as_dict["timestamp"]["GP_number"], bytes=1)
            self.manipulate_bits(bit_array, self.as_dict["timestamp"]["GP_edge"], bytes=1)

        self.manipulate_bits(bit_array, self.as_dict["num_ops"], bytes=1)
        for index in range(self.as_dict["num_ops"]):
            ## Read in metadatato  bit string
            self.manipulate_bits(bit_array, self.as_dict["ops"][index]["op_id"], bytes=2)
            self.manipulate_bits(bit_array, self.as_dict["ops"][index]["data_length"], bytes=2)
            
            ## read in actual position to metadata
            scte104_enums.encode_data(self.as_dict["ops"][index]["op_id"], bit_array, self.as_dict["ops"][index]["data"], self.position)
        
            ##adjust position by data offset
            self.position = self.position + (self.as_dict["ops"][index]["data_length"]) * byte_size
        return bit_array

    def to_dict(self):
        return self.as_dict


    def manipulate_bits(self, bit_array, value, bytes=1):
        hex_val = self.hex_string(value, bytes)
        bit_array.overwrite(hex_val, pos=self.position)
        self.position = self.position + bytes*byte_size
        return None


    def hex_string(self, value, bytes):
        s = hex(value) 
        return '0x' + s[2:].zfill(bytes*2)

    def get_pre_roll_time(self):
        return self.as_dict["ops"][0]["data"]["pre_roll_time"]

    def set_pre_roll_time(self, time):
        self.as_dict["ops"][0]["data"]["pre_roll_time"] = time 