from functools import lru_cache
from os import path

import pandas
from flask import Flask, Response, abort, jsonify

DATA_PATH_PREFIX = 'resources'
DEFAULT_COMPANIES_JSON = path.join(DATA_PATH_PREFIX, 'companies.json')
DEFAULT_PEOPLE_JSON = path.join(DATA_PATH_PREFIX, 'people.json')
DEFAULT_FOODS_JSON = path.join(DATA_PATH_PREFIX, 'foods.json')


class Data:
    def __init__(self, *, companies_json=DEFAULT_COMPANIES_JSON,
                 people_json=DEFAULT_PEOPLE_JSON, foods_json=DEFAULT_FOODS_JSON):
        self.companies = pandas.read_json('resources/companies.json')
        self.companies = self.companies.set_index(self.companies['company'], verify_integrity=True)

        self.people = pandas.read_json('resources/people.json')
        # flatten the "friends" dictionary
        self.people['friends'] = self.people['friends'].map(lambda fs: [f['index'] for f in fs])
        # pre-calculate the usernames
        self.people['username'] = self.people['email'].map(lambda e: e.split('@')[0])
        self.people = self.people.set_index(self.people['username'], verify_integrity=True)

        self.foods = pandas.read_json('resources/foods.json')
        self.foods = self.foods.set_index(self.foods['food'], verify_integrity=True)

@lru_cache()
def get_data():
    return Data()


def jsonify_pd(obj, **kwargs):
    """ Make a response for a pandas type; similar to flask.jsonify but
    uses the object's .to_json method rather than json.dumps. Keyword
    arguments are passed to the .to_json method (eg. orient='records').
    """
    return Response(
        obj.to_json(**kwargs),
        mimetype='application/json'
    )


app = Flask(__name__)

@app.route("/v1/company/<string:company>/employees")
def employees(company):
    return jsonify_pd(_employees(company, data = get_data()), orient='records')

def _employees(company, *, data):

    company_id = data.companies.loc[company]['index']

    employees = data.people[data.people['company_id'] == company_id]
    employees = employees[['username', 'age']]
    return employees


@app.route("/v1/mutual_info/<string:username1>/<string:username2>")
def mutual_info(username1, username2):
    return jsonify(_mutual_info(username1, username2, data=get_data()))

def _mutual_info(username1, username2, *, data):
    persons = data.people.loc[[username1, username2]]
    friends1, friends2 = (set(x) for x in persons['friends'])
    mutuals = data.people.set_index(data.people['index']).loc[list(friends1 & friends2)]
    mutuals = mutuals[mutuals['eyeColor'] == 'brown']
    mutuals = mutuals[mutuals['has_died'] == False]

    persons = persons[['name', 'age', 'address', 'phone']]
    mutuals = mutuals[['name', 'age', 'address', 'phone']]

    return {
        'persons': persons.to_dict(orient='records'),
        'mutuals': mutuals.to_dict(orient='records'),
    }


@app.route("/v1/person/<string:username>/favourites")
def favourites(username):
    return jsonify_pd(_favourites(username, data=get_data()))

def _favourites(username, *, data):
    person = data.people.loc[username]

    favourite_by_food_group = (
        data.foods
        .loc[person['favouriteFood']]
        .groupby('group')
        .aggregate(list)
        ['food']
    )

    person = person[['username', 'age']].append(favourite_by_food_group)

    return person
