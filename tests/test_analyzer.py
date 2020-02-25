"""Unittest module for wapp analyzer."""
import os
import mock
import logging
import unittest


from wapp.analyzer.app import calculate_stats, allowed_file, is_date, week_day


class WhatsappAnalyzerTestCase(unittest.TestCase):
    def test_calculate_stats(self):
        expected_result = {
            "word_cloud": {
                "pork": 972,
                "ribs": 728,
                "beef": 727,
                "bacon": 580,
                "ham": 507,
                "loin": 482,
                "short": 471,
                "amet": 339,
                "ipsum": 338,
                "dolor": 337,
                "spare": 273,
                "shank": 272,
                "salami": 270,
                "boudin": 265,
                "hock": 263,
                "shoulder": 261,
                "drumstick": 260,
                "doner": 259,
                "landjaeger": 258,
                "sirloin": 257,
                "corned": 256,
                "ribeye": 255,
                "ground": 254,
                "jerky": 253,
                "round": 252,
            },
            "message_count": {
                "asta": 67,
                "luffy": 63,
                "vegeta": 62,
                "goku": 59,
                "shin": 55,
                "saitama": 53,
            },
            "the_talker": "asta",
            "the_silent_spectator": "saitama",
            "media_count": {
                "asta": 9,
                "goku": 8,
                "saitama": 7,
                "luffy": 5,
                "vegeta": 4,
                "shin": 2,
            },
            "media_share_freak": "asta",
            "date_chart": {
                "01/05/2019": 93,
                "27/04/2019": 90,
                "30/04/2019": 86,
                "26/04/2019": 44,
                "28/04/2019": 33,
                "29/04/2019": 7,
                "02/04/2019": 6,
            },
            "most_active_date": "01/05/2019",
            "active_day_of_week": "Wednesday",
            "active_hour_of_day": "5 AM - 6 AM",
            "avg_no_of_msgs_per_day": 51.29,
        }
        result = calculate_stats("tests/fixtures/chat.txt", "Month First")
        self.assertEqual(result, expected_result)

    def test_allowed_file(self):
        result = allowed_file("chat.txt")
        self.assertEqual(result, True)

        result = allowed_file("chat.csv")
        self.assertEqual(result, False)

    def test_is_date(self):
        result = is_date("2019-05-02")
        self.assertEqual(result, True)

        result = is_date("May 2 2019")
        self.assertEqual(result, True)

        result = is_date("date")
        self.assertEqual(result, False)

    def test_week_day(self):
        result = week_day(0)
        self.assertEqual(result, "Monday")
