from scte.Scte104 import scte104_enums
import bitstring


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
        message_dict["ops"] = {}
        for index in range(message_dict["num_ops"]):
            message_dict["ops"][index] = {}
            message_dict["ops"][index]["op_id"] = bitarray_data.read("uint:16")
            message_dict["ops"][index]["type"] = scte104_enums.get_multi_op_id_type(message_dict["ops"][index]["op_id"])
            message_dict["ops"][index]["data_length"] = bitarray_data.read("uint:16")
            bit_subdata = bitstring.BitString(bytes=bytes.fromhex(bitarray_data.read("hex:" + str(message_dict["ops"][index]["data_length"]*8))))
            message_dict["ops"][index]["data"] = scte104_enums.read_data(message_dict["ops"][index]["op_id"], bit_subdata) 
        self.as_dict = message_dict

    def print(self):
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

#TODO: Not sure these will behave like you expect them to. Looks like op_id occurs multiple times under different keys.
    @property
    def op_id(self):
        return self.as_dict[op_id]

    @property
    def message_size(self):
        return self.as_dict[message_size]

    @property
    def protocol_version(self):
        return self.as_dict[protocol_version]

    @property
    def as_index(self):
        return self.as_dict[as_index]

    @property
    def message_number(self):
        return self.as_dict[message_number]

    @property
    def dpi_pid_index(self):
        return self.as_dict[dpi_pid_index]

    @property
    def scte35_protocol(self):
        return self.as_dict[scte35_protocol]

    @property
    def timestamp(self):
        return self.as_dict[timestamp]

    @property
    def num_ops(self):
        return self.as_dict[num_ops]

    @property
    def data(self):
        return self.as_dict[data]
