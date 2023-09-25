from importlib import resources

MODELS_FOLDER = 'ml.classification.models'
MODELS_PATH = resources.files(MODELS_FOLDER)

CLASSIFICATION_MAPPING = {
    '3N_3N': 0,
    '3N_7C': 1,
    '3N_7N': 2,
    '3N_15C': 3,
    '3N_15N': 4,
    '7C_3N': 5,
    '7C_7C': 6,
    '7C_7N': 7,
    '7C_15C': 8,
    '7C_15N': 9,
    '7N_3N': 10,
    '7N_7C': 11,
    '7N_7N': 12,
    '7N_15C': 13,
    '7N_15N': 14,
    '15C_3N': 15,
    '15C_7C': 16,
    '15C_7N': 17,
    '15C_15C': 18,
    '15C_15N': 19,
    '15N_3N': 20,
    '15N_7C': 21,
    '15N_7N': 22,
    '15N_15C': 23,
    '15N_15N': 24
}

INVERSE_CLASSIFICATION_MAPPING = {
    v: k
    for k, v in CLASSIFICATION_MAPPING.items()
}
