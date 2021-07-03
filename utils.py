from json import load, dump
from flask import jsonify


def get_data_from_file(filename):
    with open(filename, mode='r') as f:
        return load(f)


def save_data_to_file(filename, dataDict):
    with open(filename, mode='w') as f:
        dump(dataDict, f, indent=2)


def good_response(payload=None, msg="Success"):
    return jsonify({
        'status': 200,
        'msg': msg,
        'payload': payload
    })


def bad_response(status=400, payload=None, msg="Request not successful"):
    return jsonify({
        'status': status,
        'msg': msg,
        'payload': payload
    })


def pathString_to_contrObject(contributors_data, path_string):
    [contr_name, contr_index] = path_string.split('/')
    contr_index = int(contr_index)
    return [contributors_data[contr_name]['contributions'][contr_index], contr_name, contr_index]
