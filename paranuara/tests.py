import itertools
from unittest import TestCase

from pandas import DataFrame, Series

import paranuara

TEST_COMPANIES = """
[
  {"index": 58, "company": "JAMNATION"},
  {"index": 59, "company": "BRAINCLIP"},
  {"index": 60, "company": "ARTWORLDS"}
]
"""

TEST_PEOPLE = """
[
  {
    "index": 0,
    "has_died": true,
    "age": 61,
    "eyeColor": "blue",
    "name": "Carmella Lambert",
    "company_id": 58,
    "email": "carmellalambert@earthmark.com",
    "phone": "+1 (910) 567-3630",
    "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
    "friends": [{"index": 0}, {"index": 1}, {"index": 2}],
    "favouriteFood": ["orange", "apple", "banana", "strawberry"]
 },
  {
    "index": 1,
    "has_died": false,
    "age": 60,
    "eyeColor": "brown",
    "name": "Decker Mckenzie",
    "company_id": 98,
    "email": "deckermckenzie@earthmark.com",
    "phone": "+1 (893) 587-3311",
    "address": "492 Stockton Street, Lawrence, Guam, 4854",
    "friends": [{"index": 0}, {"index": 1}, {"index": 2}],
    "favouriteFood": ["cucumber", "beetroot", "carrot", "celery"]
 },
  {
    "index": 2,
    "has_died": false,
    "age": 54,
    "eyeColor": "blue",
    "name": "Bonnie Bass",
    "company_id": 59,
    "email": "bonniebass@earthmark.com",
    "phone": "+1 (823) 428-3710",
    "address": "455 Dictum Court, Nadine, Mississippi, 6499",
    "friends": [{"index": 0}, {"index": 1}, {"index": 2}],
    "favouriteFood": ["orange", "beetroot", "banana", "strawberry"]
 },
  {
    "index": 3,
    "has_died": true,
    "age": 30,
    "eyeColor": "blue",
    "name": "Rosemary Hayes",
    "company_id": 48,
    "email": "rosemaryhayes@earthmark.com",
    "phone": "+1 (984) 437-3226",
    "address": "130 Bay Parkway, Marshall, Virgin Islands, 298",
    "friends": [{"index": 0}, {"index": 1}, {"index": 2}, {"index": 3},
                {"index": 4}],
    "favouriteFood": ["orange", "apple", "carrot", "celery"]
 },
  {
    "index": 4,
    "has_died": false,
    "age": 62,
    "eyeColor": "brown",
    "name": "Mindy Beasley",
    "company_id": 18,
    "email": "mindybeasley@earthmark.com",
    "phone": "+1 (862) 503-2197",
    "address": "628 Brevoort Place, Bellamy, Kansas, 2696",
    "friends": [{"index": 0}, {"index": 1}, {"index": 2}, {"index": 3},
                {"index": 4}],
    "favouriteFood": ["orange", "apple", "banana", "strawberry"]
 }
]
"""

TEST_FOODS = """
[
  {"index": 0, "food": "apple", "group": "fruits"},
  {"index": 1, "food": "banana", "group": "fruits"},
  {"index": 2, "food": "beetroot", "group": "vegetables"},
  {"index": 3, "food": "carrot", "group": "vegetables"},
  {"index": 4, "food": "celery", "group": "vegetables"},
  {"index": 5, "food": "cucumber", "group": "vegetables"},
  {"index": 6, "food": "orange", "group": "fruits"},
  {"index": 7, "food": "strawberry", "group": "fruits"}
]
"""


class ParanuaraTest(TestCase):
    def test_employees(self):
        data = paranuara.Data(companies_json=TEST_COMPANIES,
                              people_json=TEST_PEOPLE,
                              foods_json=TEST_FOODS)
        self.assertEqual(
            paranuara._employees('JAMNATION', data=data)
            .to_dict(orient='record'),
            [{'age': 61, 'username': 'carmellalambert'}]
        )

    def test_mutual_info(self):
        data = paranuara.Data(companies_json=TEST_COMPANIES,
                              people_json=TEST_PEOPLE,
                              foods_json=TEST_FOODS)

        self.assertEqual(
            paranuara._mutual_info('carmellalambert', 'deckermckenzie',
                                   data=data),
            {
                'persons': [
                    {'name': 'Carmella Lambert', 'age': 61,
                     'phone': '+1 (910) 567-3630',
                     'address': '628 Sumner Place, Sperryville, '
                                'American Samoa, 9819'},
                    {'name': 'Decker Mckenzie', 'age': 60,
                     'phone': '+1 (893) 587-3311',
                     'address': '492 Stockton Street, Lawrence, '
                                'Guam, 4854'},
                ],
                'mutuals': [
                    {'name': 'Decker Mckenzie', 'age': 60,
                     'phone': '+1 (893) 587-3311',
                     'address': '492 Stockton Street, Lawrence, '
                                'Guam, 4854'}
                ]
            }

        )

    def test_mutuals_symmetric(self):
        """ The mutual_info function should be symmetric with respect to
        argument order; test it with all combinations in the test data. """
        data = paranuara.Data(companies_json=TEST_COMPANIES,
                              people_json=TEST_PEOPLE,
                              foods_json=TEST_FOODS)
        all_pairs = itertools.combinations_with_replacement(data.people.index,
                                                            2)
        for alice, bob in all_pairs:
            ab = paranuara._mutual_info(alice, bob, data=data)
            ba = paranuara._mutual_info(bob, alice, data=data)
            self.assertEqual(ab['persons'], list(reversed(ba['persons'])))
            self.assertCountEqual(ab['mutuals'], ba['mutuals'])

    def test_favourites(self):
        data = paranuara.Data(companies_json=TEST_COMPANIES,
                              people_json=TEST_PEOPLE,
                              foods_json=TEST_FOODS)

        self.assertEqual(
            paranuara._favourites('carmellalambert', data=data).to_dict(),
            {
                "username": "carmellalambert",
                "age": "61",
                "fruits": ["orange", "apple", "banana", "strawberry"],
                "vegetables": [],
            }
        )
