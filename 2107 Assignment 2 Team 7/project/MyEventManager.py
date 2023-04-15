# Make sure you are logged into your Monash student account.
# Go to: https://developers.google.com/calendar/quickstart/python
# Click on "Enable the Google Calendar API"
# Configure your OAuth client - select "Desktop app", then proceed
# Click on "Download Client Configuration" to obtain a credential.json file
# Do not share your credential.json file with anybody else, and do not commit it to your A2 git repository.
# When app is run for the first time, you will need to sign in using your Monash student account.
# Allow the "View your calendars" permission request.
# can send calendar event invitation to a student using the student.monash.edu email.
# The app doesn't support sending events to non student or private emails such as outlook, gmail etc
# students must have their own api key
# no test cases for authentication, but authentication may required for running the app very first time.
# http://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.html


# Code adapted from https://developers.google.com/calendar/quickstart/python
from __future__ import print_function
#from curses import keyname
import datetime
import email
import pickle
import os.path
from sqlite3 import DateFromTicks
import datetime
from EventClass import *

#from sys import ps1
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def create_event(api):
    try:
        Event(api)
        return True
    except:
        raise Exception("Invalid details")


def getOption(maxIndex, events, message):
    try:
        item = int(input(message))
        if item >= maxIndex or item <= 0:
            raise Exception("Index out of range!")
        else:
            obj = events[item-1]
            return obj
    except:
        raise Exception("Input must be an integer")


def update_event(api, time_now):
    events = get_past_events(api, time_now, None)
    events += get_upcoming_events(api, time_now, None)
    header = "All Events Found\n"
    [i, noEvent] = print_events(events, header)
    if noEvent == True:
        return
    # choose what field to be updated
    message = "Select the index of event to be updated: "
    update_event = getOption(i, events, message)
    if update_event == None:
        return
    else:
        menu = "[1] Update event Name\n"
        menu += "[2] Update event Location\n"
        menu += "[3] Update event Date\n"
        menu += "Option: "
        try:
            option = int(input(menu))
            if option > 3 or option <= 0:
                raise Exception("Index out of range!")
            else:
                id = update_event['id']
                if option == 1:
                    new_name = input("New event name: ")
                    update_event = {
                        'summary': new_name
                    }
                    api.events().patch(calendarId='primary', eventId=id,
                                       sendNotifications=True, body=update_event).execute()
                elif option == 2:
                    new_loc = input("New event location: ")
                    new_loc = new_loc.split(" ")
                    if new_loc[0].lower() == "online":
                        valid_new_loc = new_loc
                    elif len(new_loc) >= 5 and (new_loc[0].isnumeric()) and (new_loc[len(new_loc)-1].isnumeric() or new_loc[len(new_loc)-2].isnumeric()):
                        valid_new_loc = new_loc
                    else:
                        raise Exception(
                            "Invalid location!!!! Only Australian or American address is acceptable!")
                    update_event = {
                        'location': valid_new_loc
                    }
                    api.events().patch(calendarId='primary', eventId=id,
                                       sendNotifications=True, body=update_event).execute()
                elif option == 3:
                    eventStartDate = input("Enter Start date: ")
                    try:
                        eventStartDate == datetime.datetime.strptime(
                            eventStartDate, "%Y-%m-%d").strftime('%Y-%m-%d')
                    except:
                        # print(eventStartDate)
                        date = datetime.datetime.strptime(
                            eventStartDate, '%d-%b-%y')
                        f_date = date.strftime('%d-%b-%y')
                        # print(f_date)
                        if eventStartDate == f_date.upper():
                            eventStartDate = date.date()
                        else:
                            raise Exception(
                                "Date format must be in dd-MON-yy or YYYY-MM-DD format")
                    eventEndDate = input("Enter End date: ")
                    try:
                        eventEndDate == datetime.datetime.strptime(
                            eventEndDate, "%Y-%m-%d").strftime('%Y-%m-%d')
                    except:
                        # print(eventStartDate)
                        date = datetime.datetime.strptime(
                            eventEndDate, '%d-%b-%y')
                        f_date = date.strftime('%d-%b-%y')
                        # print(f_date)
                        if eventEndDate == f_date.upper():
                            eventEndDate = date.date()
                        else:
                            raise Exception(
                                "Date format must be in dd-MON-yy or YYYY-MM-DD format")
                    update_event = {
                        'start': {
                            'date': '2022-09-28',
                            'timeZone': 'America/Los_Angeles',
                        },
                        'end': {
                            'date': '2022-09-28',
                            'timeZone': 'America/Los_Angeles',
                        }
                    }
                    update_event['start'] = {}
                    update_event['start'] = {'date': str(eventStartDate)}
                    update_event['end'] = {}
                    update_event['end'] = {'date': str(eventEndDate)}
                    api.events().patch(calendarId='primary', eventId=id,
                                       sendNotifications=True, body=update_event).execute()
        except:
            raise Exception("Input must be an integer")


def to_delete_event(api, time_now):
    events = get_past_events(api, time_now, None)
    events += get_upcoming_events(api, time_now, None)
    header = "ALL EVENT"
    [i, noEvent] = print_events(events, header)
    if noEvent == True:
        return
    message = "Select the index of event to be deleted: "
    deleted_event = getOption(i, events, message)
    if deleted_event != None:
        delete_event(api, deleted_event, time_now)


def delete_event(api, deleted_event, time_now):
    if deleted_event['start']['date'] < time_now:
        id = deleted_event['id']
        api.events().delete(calendarId='primary', eventId=id).execute()
        print("Event is deleted!")
    else:
        raise Exception("Only past events can be deleted!")


def to_cancel_event(api, time_now):
    events = get_upcoming_events(api, time_now, None)
    events += get_upcoming_events(api, time_now, None)
    header = "ALL EVENTS"
    [i, noEvent] = print_events(events, header)
    if noEvent == True:
        return
    message = "Select the index of event to be canceled: "
    canceled_event = getOption(i, events, message)
    if canceled_event != None:
        cancel_event(api, canceled_event, time_now)


def cancel_event(api, canceled_event, time_now):
    if canceled_event['start']['date'] > time_now:
        id = canceled_event['id']
        canceled_event = {
            'status': "cancelled"
        }
        api.events().patch(calendarId='primary', eventId=id,
                           sendNotifications=True, body=canceled_event).execute()
    else:
        raise Exception("Only future events can be canceled!")


def change_event_owner(api, time_now):
    events = get_upcoming_events(api, time_now, None)
    header = "UPCOMING EVENTS"
    [i, noEvent] = print_events(events, header)
    if noEvent == True:
        return
    message = "Select the index of event to have its owner changed: "
    changed_event_owner = getOption(i, events, message)
    if changed_event_owner != None:
        id = changed_event_owner['id']
        changed_event_owner = {
            'status': "cancelled"
        }
        newOwner = input(message)  # need to make sure it is an email address
        api.events().move(calendarId='primary', eventId=id,
                          destination=newOwner).execute()
    print("Owner has been changed to" + newOwner)


def add_attendees(api, time_now):
    # First retrieve the event from the API.
    events = get_upcoming_events(api, time_now, None)
    header = "ADD ATTENDEES"
    [i, noEvent] = print_events(events, header)
    if noEvent == True:
        return
    message = "Select the index of event to add attendees: "
    add_attendees = getOption(i, events, message)
    attendees_list = []
    if add_attendees != None:
        id = add_attendees['id']
        current_attendees = add_attendees['attendees']
        isStop = False
        attendees_list.append(current_attendees)
        while isStop == False:
            print("Enter attendee's email address:")
            new_email = input()
            if new_email == "S":
                isStop = True
            else:
                attendees_list = {
                    "attendees": [
                        {
                            "email": str(new_email),
                        }
                    ]
                }
        api.events().patch(calendarId='primary', eventId=id,
                           body=attendees_list).execute()


def delete_attendees(api, time_now):
    # First retrieve the event from the API.
    events = get_upcoming_events(api, time_now, None)
    header = "DELETE ATTENDEES"
    [i, noEvent] = print_events(events, header)
    if noEvent == True:
        return
    message = "Select the index of event to add attendees: "
    delete_attendees = getOption(i, events, message)
    if delete_attendees != None:
        id = delete_attendees['id']
        selected_attendees = delete_attendees['attendees']
        print(selected_attendees)
        isStop = False
        while isStop == False:
            print("Enter attendee's email address:")
            selected_attendees = input()
            if selected_attendees == None:
                print("The email you entered does not exist!")
                isStop = True
            else:
                api.events().delete(calendarId='primary', eventId=id,
                                    body=selected_attendees).execute()


def notify_attendees(api, time_now):
    events = get_upcoming_events(api, time_now, None)
    header = "NOTIFY ATTENDEES"
    [i, noEvent] = print_events(events, header)
    if noEvent == True:
        return
    message = "Select the index of event to notify attendees: "
    notify_attendees = getOption(i, events, message)
    if notify_attendees != None:
        id = notify_attendees['id']
    api.events().patch(calendarId='primary', eventId=id, sendUpdates='all').execute()


def responses_attendees(api, time_now):
    # First retrieve the event from the API.
    events = get_upcoming_events(api, time_now, None)
    header = "INVITATION RESPONSE"
    [i, noEvent] = print_events(events, header)
    if noEvent == True:
        return
    message = "Select the index of event to respond to: "
    responses_attendees = getOption(i, events, message)
    isStop = False
    while isStop == False:
        id = responses_attendees['id']
        responses_attendees = responses_attendees['attendees']
        if responses_attendees != None:
            print("Enter your email:")
            response_email = input()
            print(
                "Enter your response: Accept[Y],Decline[N],Maybe[M], Stop[S]:")
            response = input()
        elif response == "Y":
            converted_response = "accepted"
        elif response == "N":
            converted_response = "declined"
        elif response == "M":
            converted_response = "tentative"
        elif response == "S":
            isStop = True
        else:
            print("Invalid response!")
    final_response = {
        "attendees": [{
            "email": str(response_email),
            "responseStatus": str(converted_response)
        }]
    }
    api.events().patch(calendarId='secondary', eventId=id,
                       body=final_response).execute()


def view_event(api, time_now):
    events = get_past_events(api, time_now, None)
    events += get_upcoming_events(api, time_now, None)
    i = 0
    while i < len(events):
        event = events[i]
        option = display_event(event)
        if option == "<":
            if i == 0:
                print("No older evvents to be displayed!\n")
                return
            else:
                i -= 1
                continue
        elif option == ">":
            if i == len(events)-1:
                print("No further evvents to be displayed!\n")
                return
            else:
                i += 1
                continue
        elif option == "0":
            return
        else:
            raise Exception("Invalid option!")


def display_event(event):
    menu = "[>] Navigate froward\n"
    menu += "[<] Navigate Backward\n"
    menu += "[0] Quit viewing\n"
    print(menu)
    ret = " \tEvent name: "+event['summary']+"\n"
    ret += " \tEvent location: "+event['location']+"\n"
    ret += "<\tEvent starting date: " + \
        event['start'].get('date', event['start'].get('date'))+"\t\t>\n"
    ret += " \tEvent ending date: " + \
        event['end'].get('date', event['end'].get('date'))+"\n"
    if event['reminders']['useDefault']:
        ret += ' \tReminder in 10 minutes before event'
    else:
        for reminder in event['reminders']['overrides']:
            ret += ' \tReminder in ' + str(reminder['minutes']) + ' minutes before event as ' + reminder[
                'method']
    print(ret)
    option = input("Option: ")
    return option

# # reminder


def set_up_reminder(api, time_now):
    events = get_upcoming_events(api, time_now, None)
    header = "Add REMINDER"
    [i, noEvent] = print_events(events, header)
    if noEvent == True:
        return
    message = "Select the index of event to add reminder: "
    setup_reminder = getOption(i, events, message)
    if setup_reminder != None:
        id = setup_reminder['id']
        setup_reminder['reminders'] = {
            'useDefault': True
        }
        print(setup_reminder['reminders'])
    api.events().patch(calendarId='primary', eventId=id,
                       sendNotifications=True, body=setup_reminder).execute()
    print("Reminder has been added!")


# def navigate_date():
#     pass


# def navigate_month():
#     pass


def navigate_year(api, time_now, target_year):
    events = get_past_events(api, time_now, None)
    events += get_upcoming_events(api, time_now, None)
    target_event = []

    for event in events:
        if event['start']['date'][0:4] == target_year:
            target_event.append(event)
    if len(target_event) == 0:
        print("No event found")
        return

    print("Found events......")
    for event in target_event:
        print('\n')
        ret = "Event name: "+event['summary']+"\n"
        ret += "Event location: "+event['location']+"\n"
        ret += "Event starting date: " + \
            event['start'].get('date', event['start'].get('date'))+"\n"
        ret += "Event ending date: " + \
            event['end'].get('date', event['end'].get('date'))+"\n"
        if event['reminders']['useDefault']:
            ret += 'Reminder in 10 minutes before event'
        else:
            for reminder in event['reminders']['overrides']:
                ret += 'Reminder in ' + str(reminder['minutes']) + ' minutes before event as ' + reminder[
                    'method']
        print(ret)


def navigate_month(api, time_now, target_month):
    events = get_past_events(api, time_now, None)
    events += get_upcoming_events(api, time_now, None)
    target_event = []

    for event in events:
        if event['start']['date'][5:7] == target_month:
            target_event.append(event)
    if len(target_event) == 0:
        print("No event found")
        return

    print("Found events......")
    for event in target_event:
        print('\n')
        ret = "Event name: "+event['summary']+"\n"
        ret += "Event location: "+event['location']+"\n"
        ret += "Event starting date: " + \
            event['start'].get('date', event['start'].get('date'))+"\n"
        ret += "Event ending date: " + \
            event['end'].get('date', event['end'].get('date'))+"\n"
        if event['reminders']['useDefault']:
            ret += 'Reminder in 10 minutes before event'
        else:
            for reminder in event['reminders']['overrides']:
                ret += 'Reminder in ' + str(reminder['minutes']) + ' minutes before event as ' + reminder[
                    'method']
        print(ret)


def navigate_date(api, time_now, target_date):
    events = get_past_events(api, time_now, None)
    events += get_upcoming_events(api, time_now, None)
    target_event = []

    for event in events:
        if event['start']['date'][8:10] == target_date:
            target_event.append(event)
    if len(target_event) == 0:
        print("No event found")
        return

    print("Found events......")
    for event in target_event:
        print('\n')
        ret = "Event name: "+event['summary']+"\n"
        ret += "Event location: "+event['location']+"\n"
        ret += "Event starting date: " + \
            event['start'].get('date', event['start'].get('date'))+"\n"
        ret += "Event ending date: " + \
            event['end'].get('date', event['end'].get('date'))+"\n"
        if event['reminders']['useDefault']:
            ret += 'Reminder in 10 minutes before event'
        else:
            for reminder in event['reminders']['overrides']:
                ret += 'Reminder in ' + str(reminder['minutes']) + ' minutes before event as ' + reminder[
                    'method']
        print(ret)


def search_from_name(api, time_now, keyword):
    events = get_past_events(api, time_now, None)
    events += get_upcoming_events(api, time_now, None)
    target_event = []

    for event in events:
        if keyword in event['summary']:
            target_event.append(event)
    if len(target_event) == 0:
        print("No event found")
        return

    print("Found events......")
    i = 0
    while i < len(target_event):
        event = target_event[i]
        option = display_event(event)
        i = 0
        if option == "<":
            if i == 0:
                print("No older events to be displayed!\n")
                return
            else:
                i -= 1
                continue
        elif option == ">":
            if i == len(target_event)-1:
                print("No further events to be displayed!\n")
                return
            else:
                i += 1
                continue
        elif option == "0":
            return
        else:
            raise Exception("Invalid option!")


def search_from_date(api, time_now, keyword):
    events = get_past_events(api, time_now, None)
    events += get_upcoming_events(api, time_now, None)
    target_event = []

    for event in events:
        if keyword in event['start']['date']:
            target_event.append(event)
    if len(target_event) == 0:
        print("No event found")
        return
    print("Found events......")
    i = 0
    while i < len(target_event):
        event = target_event[i]
        option = display_event(event)
        if option == "<":
            if i == 0:
                print("No older evvents to be displayed!\n")
                return
            else:
                i -= 1
                continue
        elif option == ">":
            if i == len(target_event)-1:
                print("No further evvents to be displayed!\n")
                return
            else:
                i += 1
                continue
        elif option == "0":
            return
        else:
            raise Exception("Invalid option!")


def search_from_keyword(api, time_now, keyword):
    events = get_past_events(api, time_now, None)
    events += get_upcoming_events(api, time_now, None)
    target_event = []

    for event in events:
        if (keyword in event['start']['date']) or (keyword in event['summary']):
            target_event.append(event)
    if len(target_event) == 0:
        print("No event found")
        return

    print("Found events......")
    i = 0
    while i < len(target_event):
        event = target_event[i]
        option = display_event(event)
        if option == "<":
            if i == 0:
                print("No older evvents to be displayed!\n")
                return
            else:
                i -= 1
                continue
        elif option == ">":
            if i == len(target_event)-1:
                print("No further evvents to be displayed!\n")
                return
            else:
                i += 1
                continue
        elif option == "0":
            return
        else:
            raise Exception("Invalid option!")


# def import_event():
#     pass


# def export_event():
#     pass


def get_calendar_api():
    """
    Get an object which allows you to consume the Google Calendar API.
    You do not need to worry about what this function exactly does, nor create test cases for it.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def get_upcoming_events(api, starting_time, number_of_events):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next n events on the user's calendar.
    """
    if(number_of_events == None):
        events_result = api.events().list(calendarId='primary', timeMin=starting_time, singleEvents=True,
                                          orderBy='startTime').execute()
        return events_result.get('items', [])

    if (number_of_events <= 0):
        raise ValueError("Number of events must be at least 1.")

    events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                      maxResults=number_of_events, singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])


def get_past_events(api, starting_time, number_of_events):
    if(number_of_events == None):
        events_result = api.events().list(calendarId='primary', timeMax=starting_time, singleEvents=True,
                                          orderBy='startTime').execute()
        return events_result.get('items', [])
    if (number_of_events <= 0):
        raise ValueError("Number of events must be at least 1.")

    events_result = api.events().list(calendarId='primary', timeMax=starting_time,
                                      maxResults=number_of_events, singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])


def print_events(events, header):
    print(header)
    noEvent = False
    if not events:
        print('No events found.')
        noEvent = True
    i = 1
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print("["+str(i)+"]"+start, event['summary'])
        i += 1
    return i, noEvent

### Main Function In charge of executing the UI ###


def event_organizer(api, time_now):
    '''
    Event organiser is the person who creates the event.
    Event organiser can
    - create events on behalf of others 
    - can create and update events at present and future dates - no later than 2050
    - the owner of the event, however, the organiser can change event owners (by assigning the event to another person)
    - can add, delete or update the attendees.
    '''

    print("----------MyEventManager------------")
    events = get_upcoming_events(api, time_now, 10)
    print("\nUPCOMING EVENTS")

    if not events:
        print('No upcoming events found.')
    for event in events:
        print(event.get('transparency'))
        # if event.get('transparency')=="opaque":
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    ret = "\n[1] Create event\n"
    ret += "[2] Update event\n"
    ret += "[3] Delete past event\n"
    ret += "[4] Cancel future event\n"
    ret += "[5] Navigate by year\n"
    ret += "[6] Navigate by month\n"
    ret += "[7] Navigate by date\n"
    ret += "[8] Search event by name\n"
    ret += "[9] Search event by date\n"
    ret += "[10] Search event by keyword\n"
    ret += "[11] Change Event Owner\n"
    ret += "[12] Add attendees\n"
    ret += "[13] Remove attendees\n"
    ret += "[14] Notify attendees\n"
    ret += "[15] Invitation response\n"
    ret += "[16] View Event\n"
    ret += "[0] Exit\n"
    ret += "Option: "
    try:
        option = int(input(ret))
        if option > 17 or option < 0:
            raise Exception("Option not availabe!")
    except:
        raise Exception("Option not availabe!")
    return option


def main():
    api = get_calendar_api()
    time_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    looping = True
    while (looping == True):
        option = event_organizer(api, time_now)
        if option == 1:
            create_event(api)
            events = get_upcoming_events(api, time_now, None)
            print(events)
        elif option == 2:
            update_event(api, time_now)
        elif option == 3:
            to_delete_event(api, time_now)
        elif option == 4:
            to_cancel_event(api, time_now)
        elif option == 5:
            target = input("Enter your target year: ")
            navigate_year(api, time_now, target)
        elif option == 6:
            target = input(
                "Enter your target month in numerical number such as 02 for February: ")
            navigate_month(api, time_now, target)
        elif option == 7:
            target = input(
                "Enter your target date in 2 digit numerical number such as 02: ")
            navigate_date(api, time_now, target)
        elif option == 8:
            keyword = input("Event name to search: ")
            search_from_name(api, time_now, keyword)
        elif option == 9:
            keyword = input("Event date to search: ")
            search_from_date(api, time_now, keyword)
        elif option == 10:
            keyword = input("Keyword to search: ")
            search_from_keyword(api, time_now, keyword)
        elif option == 11:
            keyword = input("New Event Owner: ")
            change_event_owner(api, time_now)
        elif option == 12:
            add_attendees(api, time_now)
        elif option == 13:
            delete_attendees(api, time_now)
        elif option == 14:
            notify_attendees(api, time_now)
        elif option == 15:
            responses_attendees(api, time_now)
        elif option == 16:
            view_event(api, time_now)
        elif option == 0:
            looping = False
    print("End")


if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    api = get_calendar_api()
    time_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    set_up_reminder(api, time_now)
    main()
