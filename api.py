from flask import Flask, request
from flask.json import jsonify
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
    sleep(0.5)
    contr_data = get_data_from_file('./contributors.json')
    recents = get_data_from_file('./recents.json')
    for key in recents:
        latest = key
    latest_month = [int(item) for item in latest.split('/')]
    current_month = [date.today().month, date.today().year]
    contr_total = {key: 0 for key in contr_data}

    # this is to check if the current month is not in the database
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
        return good_response(payload={'list': [], 'moreAvailable': False}, msg='Index is probably out of range')
    else:
        start_index = end_index - 10
        if (start_index < 0):
            start_index = 0
    recents = recents[start_index: end_index]
    recents.reverse()
    more_available = start_index != 0

    return good_response({'list': recents, 'moreAvailable': more_available})


@app.route('/new/contribution', methods=('POST',))
@cross_origin()
def add_contribution():
    """ 
    API Reference
    Request Object:
        {
        *userName: String,
        *contObject: {*stamp: int, *amount: int}
        }
    """
    reqObj = request.get_json()
    recents = get_data_from_file('./recents.json')
    contributors = get_data_from_file('./contributors.json')

    sleep(0.5)

    for key in recents:
        latest = key
    latest_month = [int(item) for item in latest.split('/')]
    current_month = [date.today().month, date.today().year]

    # this is to check if the current month is not in the database
    if((latest_month[0] < current_month[0]) or (latest_month[1] < latest_month[1])):
        latest = f'{current_month[0]}/{current_month[1]}'
        recents[latest] = []

    # some checkings before mutations
    if (reqObj["userName"] not in contributors):
        return bad_response(msg='User Name not found!!!')

    # some mutations in the recents and contributions
    user_cont_list = contributors[reqObj["userName"]]["contributions"]
    user_cont_list.append(reqObj["contObject"])

    cont_string = f"{reqObj['userName']}/{len(user_cont_list) - 1}"
    recents[latest].append(cont_string)
    save_data_to_file('./recents.json', recents)
    save_data_to_file('./contributors.json', contributors)
    return good_response({'recentString': cont_string}, msg="New Contribution has been added")


@app.route('/check/username')
@cross_origin()
def check_username():
    username = request.args.get('userName')
    contributors = get_data_from_file('./contributors.json')
    answer = username in contributors
    return good_response(payload={"isRegistered": answer})


@app.route('/new/contributor', methods=('POST', ))
@cross_origin()
def add_contributor():
    """
        API Reference:
        Request Object: 
            {
                *name: String,
                *id: String
            }
    """
    req_obj = request.get_json()
    user_name = req_obj["name"]
    user_id = req_obj["id"]
    contributiors = get_data_from_file('./contributors.json')
    contributiors[user_id] = {
        "name": user_name,
        "id": user_id,
        "contributions": []
    }
    save_data_to_file('./contributors.json', contributiors)
    return good_response(msg='New User Has been added')


@app.route('/donors')
@cross_origin()
def get_donors():
    donors = get_data_from_file('donors.json')
    return good_response(donors)


@app.route('/check/donor')
@cross_origin()
def check_donor():
    donors = get_data_from_file('donors.json')
    reqName = request.args.get('name', '')
    return good_response(payload={"available": reqName not in donors})


if __name__ == '__main__':
    app.run(debug=True)
