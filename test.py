from journal import journal as jour
from random import randrange

user_name = '{}{}{}{}{}'.format(randrange(10), randrange(10), randrange(10), randrange(10), randrange(10))
jour._testinit()

def test_signup():
    return jour._testsu('random_name', user_name, 'pwd', 'pwd')

def test_login():
    return jour._testlogin(user_name, 'pwd')

def test_list_entries():
    return jour._testlist_entries()

def test_create_entry():
    return jour._testcreate_entry('this is a test journal entry')

if test_signup() and test_login() and test_create_entry() and test_list_entries():
    print('Test passed')
else:
    print('Test failed')