import json
import os
import datetime
import getpass
from pathlib import Path

home_dir = str(Path.home())
data_dir = home_dir + '/.journalrc'
f_data_dir = None
data = {'users': {}, 'data': {}}
logged_in_user = None

class NS:
    pass

def save():
    f_data_dir.seek(0)
    f_data_dir.truncate()
    f_data_dir.write(json.dumps(data).encode())

def sign_up():
    global logged_in_user
    if len(data['users'].keys()) == 10:
        print('No more users can be added')
        return

    ns = NS()
    ns.name = input('Enter Name: ')

    def _sign_up():
        ns.user_name = input('Enter Username: ')
        def input_pwd():
            ns.password = getpass.getpass('Enter Password: ')
            ns.repeat_password = getpass.getpass('Repeat Password: ')
        input_pwd()
        while not ns.password == ns.repeat_password:
            print('Passwords do no match')
            input_pwd()

    _sign_up()
    user = {'name': ns.name, 'user_name': ns.user_name, 'password': ns.password}
    data['users'][ns.user_name] = user
    data['data'][ns.user_name] = []
    save()
    logged_in_user = user

def _testinit():
    global f_data_dir, data
    if (not os.path.exists(data_dir)):
        f_data_dir = open(data_dir, 'w+b')
        save()
    else:
        f_data_dir = open(data_dir, 'r+b')
        data = json.loads(f_data_dir.read().decode())

def _testlogin(u, p):
    global data, logged_in_user
    if u not in data['users']:
        return False
    if p != data['users'][u]['password']:
        return False
    logged_in_user = data['users'][u]
    return True

def _testlist_entries():
    global logged_in_user
    if logged_in_user:
        for entry in data['data'][logged_in_user['user_name']]:
            print('{} - {}'.format(entry['timestamp'], entry['text']))
            return True
    else:
        return False


def _testcreate_entry(t):
    global logged_in_user, data
    now = datetime.datetime.now()
    if logged_in_user:
        data['data'][logged_in_user['user_name']].append({
            'timestamp': now.strftime('%d %B %Y %I:%M%p'),
            'text': t
        })
        if len(data['data'][logged_in_user['user_name']]) >= 50:
            data['data'][logged_in_user['user_name']] = data['data'][logged_in_user['user_name']][1:]
        save()
        return True
    else:
        return False


def _testsu(n, u, p, r):
    if u in data['users']:
        return False
    if p != r:
        return False
    if len(data['users']) == 10:
        return False

    data['users'][u] = {'name': n, 'user_name': u, 'password': p}
    data['data'][u] = []
    save()
    return True

def login():
    global logged_in_user
    if len(data['users'].keys()) == 0:
        print ('No users available')
        return

    ns = NS()
    def _login():
        ns.user_name = input('Enter Username: ')
        ns.password = getpass.getpass('Enter Password: ')
    _login()
    while ns.user_name not in data['users'] or data['users'][ns.user_name]['password'] != ns.password:
        print ('Invalid Username or Password. Try Again')
        _login()

    logged_in_user = data['users'][ns.user_name]



def show_welcome_screen():
    print ('Welcome to Journals\nPress\n1 for Login\n2 for Sign up\n3 to Quit')
    ns = NS()
    ns.inp = input()
    while ns.inp != '1' and ns.inp != '2' and ns.inp != '3':
        ns.inp = input()

    if ns.inp == '2':
        sign_up()
    elif ns.inp == '1':
        login()
    elif ns.inp == '3':
        quit(0)


def list_entries():
    global logged_in_user
    entries = data['data'][logged_in_user['user_name']]

    if len(entries) == 0:
        print('No Journal entry available')
        return

    for entry in entries:
        print ('{} - {}'.format(entry['timestamp'], entry['text']))

def create_entry():
    global logged_in_user

    print('Enter text:')
    text = input()
    now = datetime.datetime.now()

    data['data'][logged_in_user['user_name']].append({
        'timestamp': now.strftime('%d %B %Y %I:%M%p'),
        'text': text
    })
    if len(data['data'][logged_in_user['user_name']]) > 50:
        data['data'][logged_in_user['user_name']] = data['data'][logged_in_user['user_name']][1:]

    save()
    print('\nSaved successfully')


def logout():
    global logged_in_user
    logged_in_user = None


def show_user_screen():
    ns = NS()
    def menu():
        print('\n\nEnter\n1 to List Journal Entries\n2 to create Journal Entry\n3 to Logout\n# to Quit')
        ns.inp = input()

    menu()
    while ns.inp != '1' and ns.inp != '2' and ns.inp != '3' and ns.inp != '#':
        menu()

    if ns.inp == '1':
        list_entries()
    elif ns.inp == '2':
        create_entry()
    elif ns.inp == '3':
        logout()
    elif ns.inp == '#':
        pass
    return ns.inp


def init():
    global f_data_dir, data, logged_in_user

    if (not os.path.exists(data_dir)):
        f_data_dir = open(data_dir, 'w+b')
        save()
    else:
        f_data_dir = open(data_dir, 'r+b')
        data = json.loads(f_data_dir.read().decode())

    show_welcome_screen()

    if logged_in_user != None:
        resp = show_user_screen()

        while resp == '1' or resp == '2':
            resp = show_user_screen()

        if resp == '3':
            logged_in_user = None
            return '3'
        elif resp == '#':
            save()
            quit()
    else:
        return '3'


if __name__ == "__main__":
    ns = NS()
    try:
        ns.resp = init()
        while ns.resp == '3':
            ns.resp = init()

    finally:
        save()
        f_data_dir.close()

