from flask import Flask, request
from utils import get_data_from_file, save_data_to_file, good_response, bad_response, pathString_to_contrObject
from flask_cors import cross_origin
from datetime import datetime, date
from time import sleep


app = Flask(__name__)


@app.route('/contributors')
@cross_origin()
def get_contributors():
    contributors = get_data_from_file('./contributors.json')
    return good_response(contributors)


@app.route('/thismonth')
@cross_origin()
def get_status():
    contr_data = get_data_from_file('./contributors.json')
    recents = get_data_from_file('./recents.json')
    for key in recents:
        latest = key
    latest_month = [int(item) for item in latest.split('/')]
    current_month = [date.today().month, date.today().year]
    contr_total = {key: 0 for key in contr_data}

    if((latest_month[0] < current_month[0]) or (latest_month[1] < latest_month[1])):
        latest = f'{current_month[0]}/{current_month[1]}'
        recents[latest] = []
        save_data_to_file('./recents.json', recents)

    for path_str in recents[latest]:

        [contribution_object, contr_name, _] = pathString_to_contrObject(
            contr_data, path_str)
        contr_total[contr_name] += contribution_object['amount']
    return good_response(contr_total)


@app.route('/recents')
@cross_origin()
def get_recents():
    index = int(request.args.get('index'))
    recentsObj = get_data_from_file('./recents.json')
    recents = []
    for recList in recentsObj.values():
        for item in recList:
            recents.append(item)
    length = len(recents)
    end_index = length - index
    if(end_index <= 0):
        return good_response(payload=[], msg='Index is probably out of range')
    else:
        start_index = end_index - 10
        if (start_index < 0):
            start_index = 0
    recents = recents[start_index: end_index]
    recents.reverse()

    return good_response(recents)


if __name__ == '__main__':
    app.run(debug=True)
