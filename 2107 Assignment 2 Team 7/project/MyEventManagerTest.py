import imp
import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
import datetime
from io import StringIO
from unittest.mock import patch
from EventClass import Event
# Add other imports here if needed


class MyEventManagerTest(unittest.TestCase):

    # # This test tests number of upcoming events.
    # def test_get_upcoming_events_number(self):
    #     num_events = 2
    #     time = "2020-08-03T00:00:00.000000Z"
    #     print("here")
    #     mock_api = Mock()
    #     events = MyEventManager.get_upcoming_events(mock_api, time, num_events)
    #
    #     self.assertEqual(
    #         mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)
    #
    #     args, kwargs = mock_api.events.return_value.list.call_args_list[0]
    #     self.assertEqual(kwargs['maxResults'], num_events)

    # test for getting valid location
    def test_set_event_location(self):
        mock_api = Mock()
        # Valid Test
        self.assertTrue(Event.location_setter(
            mock_api, "23 ABC DEF Str. 41 Australia"))

        # Valid Test
        self.assertTrue(Event.location_setter(mock_api, "Online"))

        # Invalid Test
        self.assertRaises(
            Exception, lambda: Event.location_setter(mock_api, "23 Street"))

    # test for getting valid event start date
    def test_set_event_start_date(self):
        mock_api = Mock()
        # Valid Test
        self.assertTrue(Event.start_date_setter(mock_api, "2022-9-8"))
        # Valid Test
        self.assertTrue(Event.start_date_setter(mock_api, "28-SEP-22"))
        # Invalid Tests
        self.assertRaises(
            Exception, lambda: Event.start_date_setter(mock_api, "22-sep-22"))

    # test to get valid end date
    def test_set_event_end_date(self):
        mock_api = Mock()
        # Valid Test
        self.assertTrue(Event.end_date_setter(mock_api, "2022-9-28"))
        # Valid Test
        self.assertTrue(Event.end_date_setter(mock_api, "08-SEP-22"))
        # Invalid Test
        self.assertRaises(
            Exception, lambda: Event.end_date_setter(mock_api, "22-sep-22"))

    # test to get valid attendees
    def test_set_attendees(self):
        mock_api = Mock()
        # Valid Test
        attendees = ['abc@gmail.com, def@gmail.com']
        self.assertTrue(Event.attendees_setter(mock_api, attendees))

        # Invalid Test
        attendees = []
        self.assertRaises(Exception, lambda: Event.attendees_setter(attendees))

    # test to get valid name
    def test_set_event_name(self):
        mock_api = Mock()
        self.assertTrue(Event.name_setter(mock_api, "Event 1"))

    # Test Cases for create_event() by using pairing strategy.
    # This is to test if one of the inputs are invalid, then the task will fail.
    @mock.patch('builtins.input', side_effect=['Event1', '23 ssdf sdf sdf dsf 234', '2022-09-28', '2022-09-28', 'abc@gmail.com', 'S'])
    def test_create_valid_event(self, input):
        mock_api = Mock()
        self.assertTrue(MyEventManager.create_event(mock_api))

    # invalid test case where the address is invalid
    @mock.patch('builtins.input', side_effect=['Event1', '23 ssdf ', '2022-09-28', '2022-09-28', 'abc@gmail.com', 'S'])
    def test_create_invalid_event_1(self, input):
        mock_api = Mock()
        self.assertRaises(
            Exception, lambda: MyEventManager.create_event(mock_api))

    # Invalid test where the event dates are invalid.
    @mock.patch('builtins.input', side_effect=['Event1', '23 ssdf sdf sdf dsf 234', '2022-SEP-28', '2022-34-28', 'abc@gmail.com', 'S'])
    def test_create_invalid_event_2(self, input):
        mock_api = Mock()
        self.assertRaises(
            Exception, lambda: MyEventManager.create_event(mock_api))

    # Invalid test where the event attendees are invalid.
    @mock.patch('builtins.input', side_effect=['Event1', '23 ssdf sdf sdf dsf 234', '22-SEP-23', '22-SEP-23', 'S', 'S'])
    def test_create_invalid_event_3(self, input):
        mock_api = Mock()
        self.assertRaises(
            Exception, lambda: MyEventManager.create_event(mock_api))

    # def test_update_event(self):
    #     num_events = 2
    #     mock_api = Mock()
    #     time_now = datetime.datetime.utcnow().isoformat() + 'Z'
    #     MyEventManager.update_event(mock_api,time_now)

    # test delete function where only past events can be deleted
    # valid test that can be deleted

    def test_delete_event_1(self):
        event = {
            'id': 'sdsdg2342jk532u352g352u352u5i3352',
            'transparency': "opaque",
            'summary': 'event_name',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': ' ',
            'start': {
                'date': '2022-09-21',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'date': '2022-09-21',
                'timeZone': 'America/Los_Angeles',
            },
        }
        mock_api = Mock()
        time_now = datetime.datetime.utcnow().isoformat() + 'Z'
        #event =[{'id': '1olba0rgbijmfv72m1126kpftf','summary': 'Past Event Summary','start': {'date': '2020-10-13'},'reminders': {'useDefault': True}}]
        MyEventManager.get_past_events = MagicMock(return_value=[event])
        mock_api.events().delete().execute = MyEventManager.get_past_events = MagicMock(
            return_value=[])
        MyEventManager.delete_event(mock_api, event, time_now)
        self.assertEqual([], MyEventManager.get_past_events.return_value)

    # invalid test where events cannot be deleted
    def test_delete_event_2(self):
        event = {
            'id': 'sdsdg2342jk532u352g352u352u5i3352',
            'transparency': "opaque",
            'summary': 'event_name',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': ' ',
            'start': {
                'date': '2023-09-26',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'date': '2023-09-21',
                'timeZone': 'America/Los_Angeles',
            },
        }
        mock_api = Mock()
        time_now = datetime.datetime.utcnow().isoformat() + 'Z'
        #event =[{'id': '1olba0rgbijmfv72m1126kpftf','summary': 'Past Event Summary','start': {'date': '2020-10-13'},'reminders': {'useDefault': True}}]
        MyEventManager.get_past_events = MagicMock(return_value=[event])
        mock_api.events().delete().execute = MyEventManager.get_past_events = MagicMock(
            return_value=[])
        self.assertRaises(Exception, lambda: MyEventManager.delete_event(
            mock_api, event, time_now))

    # test searching events by name
    @mock.patch('builtins.input', side_effect=['>'])
    def test_search_event_by_name(self, input):
        mock_api = Mock()
        time_now = datetime.datetime.utcnow().isoformat() + 'Z'
        MyEventManager.get_past_events = MagicMock(return_value=[{'id': '23423j523bjfdgb35bjfgd43',
                                                                 'summary': 'Past',
                                                                  'location': "loc",
                                                                  'start': {'date': '2020-12-23'},
                                                                  'end': {'date': '2020-12-23'},
                                                                  'reminders': {'useDefault': True}}])
        MyEventManager.get_upcoming_events = MagicMock(return_value=[{'id': 'dfhgsdf9sdh89df798ddyfhuisdf',
                                                                      'summary': 'Future',
                                                                      'location': "loc",
                                                                      'start': {
                                                                          'dateTime': '2023-11-29'},
                                                                      'reminders': {'useDefault': True}}])
        # Valid Test Case
        ret = "Found events......\n"
        ret += "[>] Navigate froward\n"
        ret += "[<] Navigate Backward\n"
        ret += "[0] Quit viewing\n\n"
        ret += " \tEvent name: Past"+"\n"
        ret += " \tEvent location: "+"loc"+"\n"
        ret += "<\tEvent starting date: " + "2020-12-23"+"\t\t>\n"
        ret += " \tEvent ending date: " + "2020-12-23"+"\n"
        ret += ' \tReminder in 10 minutes before event\n'
        ret += "No further events to be displayed!"
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            MyEventManager.search_from_name(mock_api, time_now, 'Past')
        # INPUT " >" DURING THE TEST
        self.assertEqual(fakeOutput.getvalue().strip(), ret)

        # Invalid Test Case
        result = MyEventManager.search_from_name(mock_api, time_now, '2012')
        self.assertEqual(None, result)

    # test searching event by date
    @mock.patch('builtins.input', side_effect=['>'])
    def test_search_event_by_date(self, input):
        mock_api = Mock()
        time_now = datetime.datetime.utcnow().isoformat() + 'Z'
        MyEventManager.get_past_events = MagicMock(return_value=[{'id': '23423j523bjfdgb35bjfgd43',
                                                                 'summary': 'Past',
                                                                  'location': "loc",
                                                                  'start': {'date': '2020-12-23'},
                                                                  'end': {'date': '2020-12-23'},
                                                                  'reminders': {'useDefault': True}}])
        MyEventManager.get_upcoming_events = MagicMock(return_value=[{'id': 'dfhgsdf9sdh89df798ddyfhuisdf',
                                                                      'summary': 'Future',
                                                                      'location': "loc",
                                                                      'start': {'date': '2021-12-23'},
                                                                      'end': {'date': '2021-12-23'},
                                                                      'reminders': {'useDefault': True}}])
        # Valid Test Case
        ret = "Found events......\n"
        ret += "[>] Navigate froward\n"
        ret += "[<] Navigate Backward\n"
        ret += "[0] Quit viewing\n\n"
        ret += " \tEvent name: Past"+"\n"
        ret += " \tEvent location: "+"loc"+"\n"
        ret += "<\tEvent starting date: " + "2020-12-23"+"\t\t>\n"
        ret += " \tEvent ending date: " + "2020-12-23"+"\n"
        ret += ' \tReminder in 10 minutes before event\n'
        ret += "No further evvents to be displayed!"
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            MyEventManager.search_from_date(mock_api, time_now, '2020')
        self.assertEqual(fakeOutput.getvalue().strip(), ret)

        # Invalid Test Case
        result = MyEventManager.search_from_name(mock_api, time_now, '2012')
        self.assertEqual(None, result)

    # test searching event by keywords where it will search throught the dates an event names.
    @mock.patch('builtins.input', side_effect=['>'])
    def test_search_event_by_keyword(self, input):
        mock_api = Mock()
        time_now = datetime.datetime.utcnow().isoformat() + 'Z'
        MyEventManager.get_past_events = MagicMock(return_value=[{'id': '23423j523bjfdgb35bjfgd43',
                                                                 'summary': 'Past12',
                                                                  'location': "loc",
                                                                  'start': {'date': '2020-12-23'},
                                                                  'end': {'date': '2020-12-23'},
                                                                  'reminders': {'useDefault': True}}])
        MyEventManager.get_upcoming_events = MagicMock(return_value=[{'id': 'dfhgsdf9sdh89df798ddyfhuisdf',
                                                                      'summary': 'Future',
                                                                      'location': "loc",
                                                                      'start': {'date': '2021-11-23'},
                                                                      'end': {'date': '2021-11-23'},
                                                                      'reminders': {'useDefault': True}}])
        # Valid Test
        ret = "Found events......\n"
        ret += "[>] Navigate froward\n"
        ret += "[<] Navigate Backward\n"
        ret += "[0] Quit viewing\n\n"
        ret += " \tEvent name: Past12"+"\n"
        ret += " \tEvent location: "+"loc"+"\n"
        ret += "<\tEvent starting date: " + "2020-12-23"+"\t\t>\n"
        ret += " \tEvent ending date: " + "2020-12-23"+"\n"
        ret += ' \tReminder in 10 minutes before event\n'
        ret += "No further evvents to be displayed!"
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            MyEventManager.search_from_keyword(mock_api, time_now, '12')
        self.assertEqual(fakeOutput.getvalue().strip(), ret)

        # Invaid Test
        result = MyEventManager.search_from_name(mock_api, time_now, '1999')
        self.assertEqual(None, result)

    # test navigate by date function
    def test_navigate_by_date(self):
        mock_api = Mock()
        time_now = datetime.datetime.utcnow().isoformat() + 'Z'
        MyEventManager.get_past_events = MagicMock(return_value=[{'id': '23423j523bjfdgb35bjfgd43',
                                                                 'summary': 'Past12',
                                                                  'location': "loc",
                                                                  'start': {'date': '2020-12-23'},
                                                                  'end': {'date': '2020-12-23'},
                                                                  'reminders': {'useDefault': True}}])
        MyEventManager.get_upcoming_events = MagicMock(return_value=[{'id': 'dfhgsdf9sdh89df798ddyfhuisdf',
                                                                      'summary': 'Future',
                                                                      'location': "loc",
                                                                      'start': {'date': '2021-11-23'},
                                                                      'end': {'date': '2021-11-23'},
                                                                      'reminders': {'useDefault': True}}])
        # Valid Tet Case 1
        ret = "Found events......\n\n\n"
        ret += "Event name: Past12\n"
        ret += "Event location: loc\n"
        ret += "Event starting date: 2020-12-23\n"
        ret += "Event ending date: 2020-12-23\n"
        ret += "Reminder in 10 minutes before event\n\n\n"
        ret += "Event name: Future\n"
        ret += "Event location: loc\n"
        ret += "Event starting date: 2021-11-23\n"
        ret += "Event ending date: 2021-11-23\n"
        ret += "Reminder in 10 minutes before event"

        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            MyEventManager.navigate_date(mock_api, time_now, '23')
        self.assertEqual(fakeOutput.getvalue().strip(), ret)

        # Valid Test Case 2
        ret = "No event found"
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            MyEventManager.navigate_date(mock_api, time_now, '01')
        self.assertEqual(fakeOutput.getvalue().strip(), ret)

    # test navigate by month function
    def test_navigate_by_month(self):
        mock_api = Mock()
        time_now = datetime.datetime.utcnow().isoformat() + 'Z'
        MyEventManager.get_past_events = MagicMock(return_value=[{'id': '23423j523bjfdgb35bjfgd43',
                                                                 'summary': 'Past12',
                                                                  'location': "loc",
                                                                  'start': {'date': '2020-12-23'},
                                                                  'end': {'date': '2020-12-23'},
                                                                  'reminders': {'useDefault': True}}])
        MyEventManager.get_upcoming_events = MagicMock(return_value=[{'id': 'dfhgsdf9sdh89df798ddyfhuisdf',
                                                                      'summary': 'Future',
                                                                      'location': "loc",
                                                                      'start': {'date': '2021-11-23'},
                                                                      'end': {'date': '2021-11-23'},
                                                                      'reminders': {'useDefault': True}}])
        # Valid Tet Case 1
        ret = "Found events......\n\n\n"
        ret += "Event name: Past12\n"
        ret += "Event location: loc\n"
        ret += "Event starting date: 2020-12-23\n"
        ret += "Event ending date: 2020-12-23\n"
        ret += "Reminder in 10 minutes before event"

        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            MyEventManager.navigate_month(mock_api, time_now, '12')
        self.assertEqual(fakeOutput.getvalue().strip(), ret)

        # Valid Test Case 2
        ret = "No event found"
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            MyEventManager.navigate_date(mock_api, time_now, 'Heelo')
        self.assertEqual(fakeOutput.getvalue().strip(), ret)

     # test navigate by year function
    def test_navigate_by_year(self):
        mock_api = Mock()
        time_now = datetime.datetime.utcnow().isoformat() + 'Z'
        MyEventManager.get_past_events = MagicMock(return_value=[{'id': '23423j523bjfdgb35bjfgd43',
                                                                 'summary': 'Past12',
                                                                  'location': "loc",
                                                                  'start': {'date': '2020-12-23'},
                                                                  'end': {'date': '2020-12-23'},
                                                                  'reminders': {'useDefault': True}}])
        MyEventManager.get_upcoming_events = MagicMock(return_value=[{'id': 'dfhgsdf9sdh89df798ddyfhuisdf',
                                                                      'summary': 'Future',
                                                                      'location': "loc",
                                                                      'start': {'date': '2021-11-23'},
                                                                      'end': {'date': '2021-11-23'},
                                                                      'reminders': {'useDefault': True}}])
        # Valid Tet Case 1
        ret = "Found events......\n\n\n"
        ret += "Event name: Future\n"
        ret += "Event location: loc\n"
        ret += "Event starting date: 2021-11-23\n"
        ret += "Event ending date: 2021-11-23\n"
        ret += "Reminder in 10 minutes before event"

        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            MyEventManager.navigate_year(mock_api, time_now, '2021')
        self.assertEqual(fakeOutput.getvalue().strip(), ret)

        # Valid Test Case 2
        ret = "No event found"
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            MyEventManager.navigate_date(mock_api, time_now, '32')
        self.assertEqual(fakeOutput.getvalue().strip(), ret)

    # to test whether the navigate forward function is workable
    @mock.patch('builtins.input', side_effect=['>', '>'])
    def test_navigate_forward(self, input):
        mock_api = Mock()
        time_now = datetime.datetime.utcnow().isoformat() + 'Z'
        MyEventManager.get_past_events = MagicMock(return_value=[{'id': '23423j523bjfdgb35bjfgd43',
                                                                 'summary': 'Past',
                                                                  'location': "loc",
                                                                  'start': {'date': '2020-12-23'},
                                                                  'end': {'date': '2020-12-23'},
                                                                  'reminders': {'useDefault': True}}])
        MyEventManager.get_upcoming_events = MagicMock(return_value=[{'id': 'dfhgsdf9sdh89df798ddyfhuisdf',
                                                                      'summary': 'Future',
                                                                      'location': "loc",
                                                                      'start': {'date': '2021-12-23'},
                                                                      'end': {'date': '2021-12-23'},
                                                                      'reminders': {'useDefault': True}}])
        # Valid Test Case
        ret = "Found events......\n"
        ret += "[>] Navigate froward\n"
        ret += "[<] Navigate Backward\n"
        ret += "[0] Quit viewing\n\n"
        ret += " \tEvent name: Past"+"\n"
        ret += " \tEvent location: "+"loc"+"\n"
        ret += "<\tEvent starting date: " + "2020-12-23"+"\t\t>\n"
        ret += " \tEvent ending date: " + "2020-12-23"+"\n"
        ret += ' \tReminder in 10 minutes before event\n'
        ret += "[>] Navigate froward\n"
        ret += "[<] Navigate Backward\n"
        ret += "[0] Quit viewing\n\n"
        ret += " \tEvent name: Future"+"\n"
        ret += " \tEvent location: "+"loc"+"\n"
        ret += "<\tEvent starting date: " + "2021-12-23"+"\t\t>\n"
        ret += " \tEvent ending date: " + "2021-12-23"+"\n"
        ret += ' \tReminder in 10 minutes before event\n'
        ret += "No further evvents to be displayed!"

        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            MyEventManager.search_from_date(mock_api, time_now, '12')
        self.assertEqual(fakeOutput.getvalue().strip(), ret)

        # Invalid Test Case
        result = MyEventManager.search_from_name(mock_api, time_now, '2012')
        self.assertEqual(None, result)

    # to test whether the navigate backward function is workable
    @mock.patch('builtins.input', side_effect=['>', '<', "<"])
    def test_navigate_backward(self, input):
        mock_api = Mock()
        time_now = datetime.datetime.utcnow().isoformat() + 'Z'
        MyEventManager.get_past_events = MagicMock(return_value=[{'id': '23423j523bjfdgb35bjfgd43',
                                                                 'summary': 'Past',
                                                                  'location': "loc",
                                                                  'start': {'date': '2020-12-23'},
                                                                  'end': {'date': '2020-12-23'},
                                                                  'reminders': {'useDefault': True}}])
        MyEventManager.get_upcoming_events = MagicMock(return_value=[{'id': 'dfhgsdf9sdh89df798ddyfhuisdf',
                                                                      'summary': 'Future',
                                                                      'location': "loc",
                                                                      'start': {'date': '2021-12-23'},
                                                                      'end': {'date': '2021-12-23'},
                                                                      'reminders': {'useDefault': True}}])
        # Valid Test Case
        ret = "Found events......\n"
        ret += "[>] Navigate froward\n"
        ret += "[<] Navigate Backward\n"
        ret += "[0] Quit viewing\n\n"
        ret += " \tEvent name: Past"+"\n"
        ret += " \tEvent location: "+"loc"+"\n"
        ret += "<\tEvent starting date: " + "2020-12-23"+"\t\t>\n"
        ret += " \tEvent ending date: " + "2020-12-23"+"\n"
        ret += ' \tReminder in 10 minutes before event\n'
        ret += "[>] Navigate froward\n"
        ret += "[<] Navigate Backward\n"
        ret += "[0] Quit viewing\n\n"
        ret += " \tEvent name: Future"+"\n"
        ret += " \tEvent location: "+"loc"+"\n"
        ret += "<\tEvent starting date: " + "2021-12-23"+"\t\t>\n"
        ret += " \tEvent ending date: " + "2021-12-23"+"\n"
        ret += ' \tReminder in 10 minutes before event\n'
        ret += "[>] Navigate froward\n"
        ret += "[<] Navigate Backward\n"
        ret += "[0] Quit viewing\n\n"
        ret += " \tEvent name: Past"+"\n"
        ret += " \tEvent location: "+"loc"+"\n"
        ret += "<\tEvent starting date: " + "2020-12-23"+"\t\t>\n"
        ret += " \tEvent ending date: " + "2020-12-23"+"\n"
        ret += ' \tReminder in 10 minutes before event\n'
        ret += "No older evvents to be displayed!"

        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            MyEventManager.search_from_date(mock_api, time_now, '12')
        self.assertEqual(fakeOutput.getvalue().strip(), ret)

        # Valid Test Case
        result = MyEventManager.search_from_name(mock_api, time_now, '2012')
        self.assertEqual(None, result)


def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(MyEventManagerTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()
