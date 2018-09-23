import datetime as dt
import pandas as pd
import json
from flask import Flask, jsonify, request
from flask_table import Table, Col


# Declare table
class ItemTable(Table):
    status = Col('User Status')
    city = Col('City')
    product_price = Col('Product Price')    


class UserStatusSearch:

    RECORDS = [
        {'user_id': 1, 'created_at': '2017-01-01T10:00:00', 'status': 'paying'},
        {'user_id': 1, 'created_at': '2017-03-01T19:00:00', 'status': 'paying'},
        {'user_id': 1, 'created_at': '2017-02-01T12:00:00', 'status': 'cancelled'},
        {'user_id': 3, 'created_at': '2017-10-01T10:00:00', 'status': 'paying'},
        {'user_id': 3, 'created_at': '2016-02-01T05:00:00', 'status': 'cancelled'},
    ]

    def __init__(self):
        pass

    def get_status(self, user_id, date):
        for row in self.RECORDS:
            row_date = dt.datetime.strptime(str(row.get('created_at')), '%Y-%m-%dT%H:%M:%S')
            if (user_id == row.get('user_id')) & (date.date() == row_date.date() ):
                return row.get('status')

        return 'non-paying' 


class IpRangeSearch:

    RANGES = {
        'london': [
            {'start': '10.10.0.0', 'end': '10.10.255.255'},
            {'start': '192.168.1.0', 'end': '192.168.1.255'},
        ],
        'munich': [
            {'start': '10.12.0.0', 'end': '10.12.255.255'},
            {'start': '172.16.10.0', 'end': '172.16.11.255'},
            {'start': '192.168.2.0', 'end': '192.168.2.255'},
        ]
    }

    def __init__(self):
        pass

    def get_city(self, ip):
        for k, v in self.RANGES.items():
            city = k
            # print city
            for row in v:
                start_ip = row.get('start')
                end_ip = row.get('end')
                valid_ip = self.ipRange(start_ip, end_ip, ip)
                if valid_ip:
                    return city

        return 'unknown'


    def ipRange(self, start_ip, end_ip, ip):
       start = map(int, start_ip.split("."))
       end = map(int, end_ip.split("."))
       temp = start
       
       while temp != end:
          start[3] += 1
          for i in (3, 2, 1):
             if temp[i] == 256:
                temp[i] = 0
                temp[i-1] += 1
          if str(ip) == ".".join(map(str, temp)):
            return True

       return False



app = Flask(__name__)
user_status_search = UserStatusSearch()
ip_range_search = IpRangeSearch()


@app.route('/user_status/<user_id>')
def user_status(user_id):
    """
    Return user status for a give date

    /user_status/1?date=2017-10-10T10:00:00
    """

    date = dt.datetime.strptime(str(request.args.get('date')), '%Y-%m-%dT%H:%M:%S')
    
    return jsonify({'user_status': user_status_search.get_status(int(user_id), date)})


@app.route('/ip_city/<ip>')
def ip_city(ip):
    """
    Return city for a given ip

    /ip_city/192.168.1.10
    """
    return jsonify({'city': ip_range_search.get_city(ip)})


@app.route('/output')
def output():
    """
    Returns the aggregate containing the sum of `product_price`, grouped by user_status and city
    """

    # Reads transaction.json and stores in a list
    data = []
    with open("transactions.json", "r") as f:
        for line in f:
            data.append(json.loads(line))

    for row in data:

        # Appends city key to json data   
        row_ip = str(row['ip'])
        row['city'] = ip_range_search.get_city(row_ip)

        # Appends status key to json data
        row_id = str(row['user_id'])
        row_date = str(row['created_at'])
        row_date = dt.datetime.strptime(str(row_date), '%Y-%m-%dT%H:%M:%S')
        row['status'] = user_status_search.get_status(int(row_id), row_date)


    # Stores enriched json data in 'enriched_data.json' file    
    with open("enriched_data.json", "w") as f:
        json.dump(data, f)

    df = pd.DataFrame(data) 
    # Aggregate of sum of `product_price`, grouped by user_status and city
    output = df.groupby(['status','city']).agg({'product_price': sum}).reset_index() 
    output_dict = output.to_dict(orient='records')  

    # Populate the table
    table = ItemTable(output_dict)

    return (table.__html__())




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
