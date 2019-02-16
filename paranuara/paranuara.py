from functools import lru_cache
from os import path

import pandas
from flask import Flask, Response, abort, jsonify


#dataclass
class Data:
    pass

@lru_cache()
def get_data():
    data = Data()

    data.companies = pandas.read_json('resources/companies.json')
    data.companies = data.companies.set_index(data.companies['company'])

    data.people = pandas.read_json('resources/people.json')
    # flatten the "friends" dictionary
    data.people['friends'] = data.people['friends'].map(lambda fs: [f['index'] for f in fs])
    # pre-calculate the usernames
    data.people['username'] = data.people['email'].map(lambda e: e.split('@')[0])
    data.people = data.people.set_index(data.people['username'])

    data.foods = pandas.read_json('resources/foods.json')
    data.foods = data.foods.set_index(data.foods['food'])

    return data


def jsonify_pd(obj, **kwargs):
    """ Make a response for a pandas type; similar to flask.jsonify but
    uses the object's .to_json method rather than json.dumps.
    """
    return Response(
        obj.to_json(**kwargs),
        mimetype='application/json'
    )


app = Flask(__name__)

@app.route("/v1/company/<string:company>/employees")
def employees(company):
    data = get_data()

    company_id = data.companies.loc[company]['index']

    employees = data.people[data.people['company_id'] == company_id]
    employees = employees[['username', 'age']]
    return jsonify_pd(employees, orient='records')

@app.route("/v1/mutual_info/<string:username1>/<string:username2>")
def mutual_info(username1, username2):
    data = get_data()
    persons = data.people.loc[[username1, username2]]
    friends1, friends2 = (set(x) for x in persons['friends'])
    mutuals = data.people.set_index(data.people['index']).loc[list(friends1 & friends2)]
    mutuals = mutuals[mutuals['eyeColor'] == 'brown']
    mutuals = mutuals[mutuals['has_died'] == False]

    persons = persons[['name', 'age', 'address', 'phone']]
    mutuals = mutuals[['name', 'age', 'address', 'phone']]

    return jsonify({
        'persons': persons.to_dict(orient='records'),
        'mutuals': mutuals.to_dict(orient='records'),
    })

@app.route("/v1/person/<string:username>/favourites")
def favourites(username):
    data = get_data()
    person = data.people.loc[username]

    favourite_by_food_group = (
        data.foods
        .loc[person['favouriteFood']]
        .groupby('group')
        .aggregate(list)
        ['food']
    )

    person = person[['username', 'age']].append(favourite_by_food_group)

    return jsonify_pd(person)
