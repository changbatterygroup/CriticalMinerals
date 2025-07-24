ELYTE = 0.005863
CATHODE_SPECS = {
    "NMC811": {
        "capacity": 0.200,
        "composition": [0.07136 + ELYTE, 0.4828, 0.05648, 0.06059],
        "template": "Chen2020",
        "category": "HNNMC"
    },
    "NMC622": {
        "capacity": 0.180,
        "composition": [0.07162 + ELYTE, 0.3634, 0.1134, 0.1216],
        "template": "Chen2020",
        "category": "HNNMC"
    },
    "NMC532": {
        "capacity": 0.170,
        "composition": [0.07190 + ELYTE, 0.3040, 0.1707, 0.1221],
        "template": "Mohtat2020",
        "category": "LNNMC"

    },
    "NMC111": {
        "capacity": 0.160,
        "composition": [0.0328 + ELYTE,  0.2775, 0.2598, 0.2787],
        "template": "Chen2020",
        "category": "LNNMC"
    },

    "LFP": {
        "capacity": 0.120,
        "composition": [0.044 + ELYTE, 0, 0, 0],
        "template": "Prada2013",
        "category": "LFP"
    },
    "NCA": {
        "capacity": 0.180,
        "composition": [0.0723 + ELYTE, 0.489, 0.092, 0],
        "template": "Chen2020",
        "category": "NCA"
    }
}

CATHODE_OPTIONS = list(CATHODE_SPECS.keys())
CATHODE_DEFAULT = "LFP"