# This script contains functions for donors route


from utils import get_data_from_file


def get_updated_donors(donors_diff):
    donors = get_data_from_file('./donors.json')
    for key, value in donors_diff.items():
        if(value == 'DELETED'):
            del donors[key]
        else:
            donors[key] = value
    return donors
