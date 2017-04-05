import csv
import re
import os
from datetime import date, datetime
import time


FILENAME = 'work_log.csv'


def main_menu():
    clear()
    print('--- MAIN MENU ---')
    valid_answer = False

    while not valid_answer:
        answer = input(
            'Please choose [A]dd entry, [S]earch entry, [Q]uit: ').lower()
        if answer == 'a':
            valid_answer = True
            add_entry()
        elif answer == 's':
            valid_answer = True
            search_menu()
        elif answer == 'q':
            valid_answer = True
            print('Bye Bye!')
            quit()
        else:
            print(
                'Please Enter [A] for Add entry, [S] for Search entry or [Q] '
                'to Quit program')
            continue


def setup():
    try:
        with open(FILENAME, 'a') as csvfile:
            fieldnames = ['ID', 'date', 'taskname', 'timespent', 'detail']
            entry_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            entry_writer.writeheader()
    except IOError:
        print("Error accessing file.")


def clear():
    print('\033c', end='')


def id_generator():
    max_ID = 0
    try:
        with open(FILENAME, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                max_ID += 1
        return max_ID
    except IOError:
        print("Error accessing file.")


def add_entry():
    clear()
    print('--- ADD ENTRY ---')
    taskname = input('Enter Task Name: ')

    while True:
        try:
            timespent = int(
                input('How many minute(s) did you finish the task?: '))
            break

        except (ValueError, AttributeError):
            print('Please enter only number!')
            time.sleep(1.5)
            continue

    detail = input('Enter detail of the Task: ')

    try:
        with open(FILENAME, 'a') as csvfile:
            entry_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            entry_writer.writerow({
                'ID': id_generator(),
                'date': date.today().strftime('%Y%m%d'),
                'taskname': taskname,
                'timespent': timespent,
                'detail': detail
            })
    except IOError:
        print("Error adding entry to file.")

    print('SUCCESSFULLY ADD NEW ENTRY')
    time.sleep(1.5)


def search_menu():
    valid_answer = False

    while not valid_answer:
        clear()
        print('--- SEARCH MENU ---')
        answer = input(
            'Search by [T]ext, [P]attern, [M]inute spent, [D]ate of entry or '
            '[Q]uit to main menu: ').lower()
        if answer == 't':
            search_text()
        elif answer == 'm':
            search_minute()
        elif answer == 'p':
            search_pattern()
            pass
        elif answer == 'd':
            search_date()
        elif answer == 'q':
            valid_answer = True
        else:
            print('You enter invalid command!')
            continue


def search_text():
    navigate_list = []

    while True:
        clear()
        try:
            print('--- SEARCH BY TEXT ---')
            answer = input('Please enter keyword or phrase: ')
            break
        except ValueError:
            continue
    try:
        with open(FILENAME) as csvfile:
            entry_reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            for row in entry_reader:
                if row['date'] == 'date':
                    pass
                elif (
                            re.search(answer, row['taskname'], re.IGNORECASE) or
                            re.search(answer, row['detail'], re.IGNORECASE)
                ):
                    navigate_list.append({
                        'ID': row['ID'],
                        'date': row['date'],
                        'taskname': row['taskname'],
                        'timespent': row['timespent'],
                        'detail': row['detail']
                    })
    except IOError:
        print("Error accessing file to search.")

    if not navigate_list:
        print('No entry found with that keyword!')
        time.sleep(1.5)
        clear()
    else:
        display_entry(navigate_list)


def search_pattern():
    navigate_list = []

    while True:
        clear()
        try:
            print('--- SEARCH BY REGEX PATTERN ---')
            print('Please enter REGEX pattern')
            print(
                "No r', No \" or ' or any symbol, just regex escape or text "
                "you want, Example: \d\w")
            answer = str(input(': '))
            break
        except ValueError:
            continue

    regex = "r'" + answer + "'"

    try:
        with open(FILENAME) as csvfile:
            entry_reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            for row in entry_reader:
                if row['date'] == 'date':
                    pass
                elif (
                            re.search(answer, row['taskname']) or
                            re.search(answer, row['detail'])
                ):
                    navigate_list.append({
                        'ID': row['ID'],
                        'date': row['date'],
                        'taskname': row['taskname'],
                        'timespent': row['timespent'],
                        'detail': row['detail']
                    })
    except IOError:
        print("Error accessing file to search pattern")

    if not navigate_list:
        print('No entry found with that pattern!')
        time.sleep(1.5)
        clear()
    else:
        display_entry(navigate_list)


def search_date():
    navigate_list = []

    while True:
        clear()
        try:
            print('--- SEARCH BY DATE RANGE ---')
            print('Please enter a range of entry date you want to search')
            print('INPUT FORMAT: YYYYMMDD. Only number, no space or symbol')
            min_date = int(input('Search Entry from date: '))
            max_date = int(input('Search Entry to date: '))
            break
        except ValueError:
            continue

    try:
        with open(FILENAME) as csvfile:
            entry_reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            for row in entry_reader:
                if row['date'] == 'date':
                    pass
                elif min_date <= int(row['date']) <= max_date:
                    navigate_list.append({
                        'ID': row['ID'],
                        'date': row['date'],
                        'taskname': row['taskname'],
                        'timespent': row['timespent'],
                        'detail': row['detail']
                    })
    except IOError:
        print("Search_date file read/write error.")

    if not navigate_list:
        print('Cound not find any entry in given date range')
        time.sleep(1.5)
        clear()
    else:
        display_entry(navigate_list)


def search_minute():
    navigate_list = []

    while True:
        clear()
        try:
            print('--- SEARCH BY MINUTE RANGE ---')
            print('Please enter range of task duration you want to look for')
            print('INPUT FORMAT: Only number, no space or symbol')
            min_minute = int(input('Minimum task duration: '))
            max_minute = int(input('Maximum task duration: '))
            break
        except ValueError:
            continue

    try:
        with open(FILENAME) as csvfile:
            entry_reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            for row in entry_reader:
                if row['date'] == 'date':
                    pass
                elif min_minute <= int(row['timespent']) <= max_minute:
                    navigate_list.append({
                        'ID': row['ID'],
                        'date': row['date'],
                        'taskname': row['taskname'],
                        'timespent': row['timespent'],
                        'detail': row['detail']
                    })
    except IOError:
        print("Search_minute file read/write error.")

    if not navigate_list:
        print('Could not find any entry in given duration range')
        time.sleep(1.5)
        clear()
    else:
        display_entry(navigate_list)


def display_entry(navigate_list):
    navigate = True
    navigate_index = 0

    while navigate:
        clear()
        print('Displaying entry {}/{}'.format(navigate_index + 1,
                                              len(navigate_list)))
        print('ID : {}'.format(navigate_list[navigate_index]['ID']))
        print('==========================================')
        print('Task Name: {}'.format(navigate_list[navigate_index]['taskname']))
        date_object = datetime.strptime(navigate_list[navigate_index]['date'],
                                        '%Y%m%d')
        print('Date of Entry: {}'.format(
            datetime.strftime(date_object, '<%A> %B %d, %Y')))
        print('Duration: {} Minute(s)'.format(
            navigate_list[navigate_index]['timespent']))
        print('==========================================')
        print('Detail of Entry:')
        print(navigate_list[navigate_index]['detail'])
        answer = input(
            '\n\nView [N]ext entry, '
            '[P]revious entry or '
            '[B]ack to search menu: ').lower()

        if navigate_index == 0 and answer == 'p':
            continue
        elif navigate_index == len(navigate_list) - 1 and answer == 'n':
            continue
        elif answer == 'p':
            navigate_index -= 1
            continue
        elif answer == 'n':
            navigate_index += 1
            continue
        elif answer == 'b':
            navigate = False
            clear()


fieldnames = ['ID', 'date', 'taskname', 'timespent', 'detail']

if not os.path.isfile(FILENAME):
    setup()

while True:
    main_menu()
