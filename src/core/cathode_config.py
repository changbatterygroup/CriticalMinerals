ELYTE = 0.005863
CATHODE_SPECS = {
    "NMC811": {
        "capacity": 0.200,
        "composition": [0.07136 + ELYTE, 0.4828, 0.05648, 0.06059],
        "category": "HNNMC"
    },
    "NMC622": {
        "capacity": 0.180,
        "composition": [0.07162 + ELYTE, 0.3634, 0.1134, 0.1216],
        "category": "HNNMC"
    },
    "NMC532": {
        "capacity": 0.170,
        "composition": [0.07190 + ELYTE, 0.3040, 0.1707, 0.1221],
        "category": "LNNMC"

    },
    "NMC111": {
        "capacity": 0.160,
        "composition": [0.0328 + ELYTE,  0.2775, 0.2598, 0.2787],
        "category": "LNNMC"
    },

    "LFP": {
        "capacity": 0.120,
        "composition": [0.044 + ELYTE, 0, 0, 0],
        "category": "LFP"
    },
    "NCA": {
        "capacity": 0.180,
        "composition": [0.0723 + ELYTE, 0.489, 0.092, 0],
        "category": "NCA"
    }
}

CATHODE_MODEL_TEMPLATES = {
    "NMC811": "Chen2020",
    "NMC622": "Chen2020",
    "NMC532": "Mohtat2020",
    "NMC111":  "Chen2020",
    "LFP": "Prada2013",
    "NCA": "NCA_Kim2011"
}



