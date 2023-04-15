from MyEventManager import *
import datetime


class Event:
    eventId = None
    eventStartDate = None
    eventEndDate = None
    eventName = None
    eventLoc = None
    eventAtnd = []
    '''
    Event class which stores all the related information of an event
    '''
    # setting up the class enviroment
    # api = get_calendar_api()
    # time_now = datetime.datetime.utcnow().isoformat() + \
    #     'Z'  # 'Z' indicates UTC time

    # initialising all the local variable

    def __init__(self, api) :
        eventId = None
        eventStartDate = None
        eventEndDate = None
        eventName = None
        eventLoc = None
        eventAtnd = []
        event = {
            'transparency': "opaque",
            'summary': 'event_name',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': ' ',
            'start': {
                'date': '2022-09-28',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'date': '2022-09-28',
                'timeZone': 'America/Los_Angeles',
            },
            'attendees': [
                {'email': 'lpage@example.com'},
                {'email': 'sbrin@example.com'},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
            ],
                        },
            'maxAttendees': {20}
        }

        self.get_UserInput()
        event['summary'] = self.eventName
        event['location'] = self.eventLoc
        event['start'] = {}
        event['start'] = {'date': str(self.eventStartDate)}
        event['end'] = {}
        event['end'] = {'date': str(self.eventEndDate)}
        event['attendees'] = []
        event['transparency'] = "opaque"
        event['maxAttendees'] = {20}
        for i in self.eventAtnd:
            attnd = {'email': i}
            event['attendees'].append(attnd)

        event = api.events().insert(calendarId='primary', body=event).execute()
    

    def get_eventId(self):
        if self.eventId is not None:
            return self.eventId
        else:
            return Exception("There is no event Id Stored")

    def get_eventId(self):
        if self.eventId is not None:
            return self.eventId
        else:
            return Exception("There is no event Id Stored")

    def name_setter(self,name):
        self.eventName = name
        return True
    
    def location_setter(self,eventLoc):
        eventLoc = eventLoc.split(" ")
        if eventLoc[0].lower()=="online":
            self.eventLoc = eventLoc
            return True
        elif len(eventLoc)>=5 and (eventLoc[0].isnumeric()) and (eventLoc[len(eventLoc)-1].isnumeric() or eventLoc[len(eventLoc)-2].isnumeric()):
            self.eventLoc = eventLoc
            return True
        else:
            raise Exception("Invalid location!!!! Only Australian or American address is acceptable!")
    
    def start_date_setter(self,eventStartDate):
        try:
            eventStartDate == datetime.datetime.strptime(eventStartDate, "%Y-%m-%d").strftime('%Y-% m-%d')
        except:
            # print(eventStartDate)
            date = datetime.datetime.strptime(eventStartDate, '%d-%b-%y')
            f_date = date.strftime('%d-%b-%y')
            # print(f_date)
            if eventStartDate == f_date.upper():
                eventStartDate = date.date()
                pass
            else:
                raise Exception(
                    "Date format must be in dd-MON-yy or YYYY-MM-DD format")
        self.eventStartDate = eventStartDate
        return True

    def end_date_setter(self,eventEndDate):
        try:
            eventEndDate == datetime.datetime.strptime(eventEndDate, "%Y-%m-%d").strftime('%Y-%m-%d')
        except:
            # print(eventStartDate)
            date = datetime.datetime.strptime(eventEndDate, '%d-%b-%y')
            f_date = date.strftime('%d-%b-%y')
            # print(f_date)
            if eventEndDate == f_date.upper():
                eventEndDate = date.date()
                pass
            else:
                raise Exception(
                    "Date format must be in dd-MON-yy or YYYY-MM-DD format")
        self.eventEndDate = eventEndDate
        return True

    def attendees_setter(self, attndList):
        if len(attndList)>0:
            self.eventAtnd = attndList
            return True
        else:
            raise Exception("Event must have at least one attendee!")

    def get_UserInput(self):
        # inform the user in what kind of format we want it (acceptable format)
        name = input("Enter name: ")
        self.name_setter(name)
        # inform the user in what kind of format we want it (acceptable format)

        eventLoc = input("Enter Location: ")
        self.location_setter(eventLoc)
        # inform the user in what kind of format we want it (acceptable format)
        # getting start date and validate it
        eventStartDate = input("Enter Start date: ")
        self.start_date_setter(eventStartDate)
        # getting end date and validate it
        eventEndDate = input("Enter End date: ")
        self.end_date_setter(eventEndDate)
        # for attendees we can create a while loop and the loop ends once the user enters a special character,ex: !
        # self.eventAtnd = input("Enter attendee: ")
        isStop = False
        atnd_list = []
        print("Enter [S] to stop entering attendees.")
        while isStop == False:
            attendees = input("Enter attendees email: ")
            if attendees != "S":
                atnd_list.append(attendees)
            else:
                isStop = True
        self.attendees_setter(atnd_list)
