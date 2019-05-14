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


def get_message(type_id):
    return __segmentation_type_ids[type_id]["message"]


def get_hex_string(type_id):
    # TODO
    return None


def get_id_from_message(message):
    for type_id in __segmentation_type_ids:
        if __segmentation_type_ids[type_id]["message"] is message:
            return type_id
