import json
import random
import string

from lindap.util import ssl_test
from src.lindap import LDAPWrapper


def gen_random_str(length=8, choices=string.ascii_letters + string.digits + string.ascii_uppercase):
    return ''.join([random.choice(choices) for _ in range(length - 1)]) + ''.join(
        [random.choice(string.digits) for _ in range(1)])


def get_connector(ldaps=True):
    with open('./dev.env', 'r') as f:
        settings = json.loads(f.read())
    print("Connecting to ", settings["server"],"with user", settings['user'])
    if not ssl_test(settings["server"], require_trust=False):
        print("Error getting connection for testing")
        return None
    l = LDAPWrapper(domain="localhost.com", user=settings['user'],
                    passw=settings['password'], server=settings['server'],
                    ldaps=settings['ldaps'],
                    read_only=False)
    return l


def print_box(message, border=True, horiz_border_char="|", vert_border_char="=", border_width=2):
    if type(message) == str:
        message = [message]
    max_width = 80 # 80 col window
    padd = max_width
    horiz_pad_str = ""
    vert_pad_str = ""
    if border:
        padd = max_width-border_width*2
        horiz_pad_str = ''.join([horiz_border_char for i in range(border_width)])
        vert_pad_str = ''.join(vert_border_char for i in range(max_width))
    for i in range(border_width):
        print(vert_pad_str)
    format_string = '{0: ^'+str(padd)+'}'
    for line in message:
        print(len(horiz_pad_str), "-", len(line))
        print(horiz_pad_str+format_string.format(line)+horiz_pad_str)
    for i in range(border_width):
        print(vert_pad_str)
