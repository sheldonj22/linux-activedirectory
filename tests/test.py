import datetime
import os
import sys
import logging
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tests.ou import test_init_ou, delete_everything
from tests.user import test_init_user, test_load_user
from tests.util import get_connector, print_box
from tests.group import test_init_group
from tests.computer import test_init_computer
from colorama import Fore, Style

logging.basicConfig(level=logging.WARNING)


if __name__ == "__main__":
    st1 = datetime.datetime.now()
    ld = get_connector()
    if not ld:
        print("Error starting tests")
        exit()
    ou1, ou2 = test_init_ou(ld)
    print_box(["", f"{Fore.GREEN}Pass OU{Style.RESET_ALL}", ""])
    user, manager = test_init_user(ld, ou2)
    print_box(["", f"{Fore.GREEN}Pass User{Style.RESET_ALL}", ""])
    test_init_group(ld, ou1, [user, manager])
    test_init_computer(ld, ou1, comp_name="WIN-6ID8SRHHR9H")
    et1 = datetime.datetime.now()
    print("Creating 1000 users in ou, please wait", ou1)
    test_load_user(ld, ou1)
    print(ou1.get_children())
    print_box(["", f"{Fore.GREEN}Passed Everything{Style.RESET_ALL}", ""], border_width=4)
    delete_everything(ld, [], "localhost.com")

