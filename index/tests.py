from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.urls import reverse
import json


class appsTest(TestCase):
    def test_dicty(self):
        with open('./index/static/index/jsontest.json') as data_file:
         dicty=json.load(data_file)
        self.assertEqual(dicty,{"1": {"4": {"15": {"371": 51.18181818181818, "278": 185.63636363636363, "224": 38.666666666666664, "388": 25.933333333333334, "399": 87.12, "392": 132.52173913043478, "85": 74.5, "10": 149.56521739130434}}}} )





class viewindex(TestCase):
    def test_index_view_connect(self):
        response=self.client.get(reverse('index:index'))
        self.assertEqual(response.status_code,200)

    def test_index_view_context(self):
        response = self.client.get(reverse('index:index'))
        self.assertEqual(response.context['stops'],[10,
 12,
 14,
 15,
 17,
 18,
 19,
 21,
 44,
 45,
 46,
 47,
 48,
 49,
 50,
 51,
 52,
 85,
 119,
 203,
 204,
 205,
 213,
 214,
 220,
 221,
 222,
 223,
 224,
 225,
 226,
 226,
 227,
 228,
 229,
 230,
 231,
 265,
 271,
 278,
 319,
 340,
 350,
 351,
 352,
 353,
 354,
 355,
 356,
 357,
 371,
 372,
 373,
 374,
 375,
 376,
 377,
 378,
 380,
 381,
 382,
 383,
 384,
 385,
 387,
 388,
 389,
 390,
 391,
 392,
 393,
 395,
 396,
 397,
 398,
 399,
 400,
 1620,
 1641,
 1642,
 2804,
 4432,
 4451,
 7525,
 7526,
 7527,
 7528,
 7529]
)

    def test_index_view_arr(self):
        response = self.client.get(reverse('index:index'))
        self.assertEqual(response.context['arr'],['6',
 '7',
 '8',
 '9',
 '10',
 '11',
 '12',
 '13',
 '14',
 '15',
 '16',
 '17',
 '18',
 '19',
 '20',
 '21',
 '22']
)

class moblieTest(TestCase):
    def test_mobile_view_(self):
        response=self.client.get(reverse('index:indexmobile'))
        self.assertEqual(response.status_code,200)

