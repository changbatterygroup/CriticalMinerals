

RESERVES_PLOT_ID = 'reserves-plot'
BODY_ID = "placeholder"
CATHODE_DROPDOWN_ID = "cathode-dropdown"

NMC_INPUT_ID = "nmc-input"
NMC_LABEL_ID = "NMC-label"

POROSITY_INPUT_ID = "porosity-input"
POROSITY_LABEL_ID = "porosity-pct-label"

THICKNESS_INPUT_ID = "thickness-input"
THICKNESS_LABEL_ID = "thickness-pct-label"

PARTICLE_SIZE_INPUT_ID = "particle-size-input"
PARTICLE_SIZE_LABEL_ID = "particle-size-label"

                      

ELYTE = 0.005863
CATHODE_SPECS = {
                    "NMC811": {
                                "capacity": 0.200,
                                "composition": [0.07136 + ELYTE, 0.4828, 0.05648, 0.06059],
                                "template": "Chen2020"
                    },
                    "NMC622": {
                                "capacity": 0.180,
                                "composition": [0.07162 + ELYTE, 0.3634, 0.1134, 0.1216],
                                "template": "Chen2020"
                    },
                    "NMC532": {
                                "capacity": 0.170,
                                "composition": [0.07190 + ELYTE, 0.3040, 0.1707, 0.1221],
                                "template": "Mohtat2020"
                    },
                    "NMC111": {
                                "capacity": 0.160,
                                "composition": [0.0328 + ELYTE,  0.2775, 0.2598, 0.2787],
                                "template": "Chen2020"
                    },

                    "LFP": {
                            "capacity": 0.120,
                            "composition": [0.044 + ELYTE, 0, 0, 0],
                            "template": "Prada2013"
                    },
                    "NCA": {
                            "capacity": 0.180,
                            "composition": [0.0723 + ELYTE, 0.489, 0.092, 0],
                            "template": "Chen2020"
                    }
                }

CATHODE_OPTIONS = list(CATHODE_SPECS.keys())



