import time
import os
import sys
from tests.util import gen_random_str
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.lindap.pydap import LDAPWrapper


def test_init_ou(ld):
    ou1, message1 = ld.create_ou(name=gen_random_str())
    ou2, message2 = ld.create_ou(name=gen_random_str())

    print("o1", ou1, ou1.objectGUID)
    if not ou1 or not ou2:
        print("Issue creating OUs", message1, message2)
        return False

    ou1.move(target_ou=ou2)
    ou1 = ou1.refresh()
    print("ou dn", ou1.distinguishedName)
    ou3, messge3 = ld.create_ou(name=gen_random_str(), parent_ou=ou1)

    if not ou3:
        print("Issue creating ou3 inside ou1", messge3)
        return False

    ou4, message4 = ld.create_ou(name=gen_random_str(), parent_ou=ou3)
    ou5, message5 = ld.create_ou(name=gen_random_str(), parent_ou=ou3)
    if not ou4 or not ou5:
        print("Issue creating ou4 and 5 inside ou3", message4, message5)
        return False

    ou5.delete_object(confirmed=True)
    ou4.delete_object(confirmed=True)
    ou3.delete_object(confirmed=True)
    return ou1, ou2


def delete_everything(ld, save_ous, safeword_domain):
    # overly cautious checks to ensure it does not accidentally get ran in a production environment
    if ld.domain != safeword_domain:
        print("You didn't say the safeword......I'm not deleting stuff.")
        return
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("You will delete everything")
    print("")
    print("")
    print("")
    while input("Are you sure you want to delete everything?[y/n]") != "y":
        pass
    print("You have 10 seconds to cancel.....")
    time.sleep(10)
    ous = ld.get_ou(ou="*")
    for ou in ous:
        if ou.distinguishedName in save_ous:
            continue
        print("deleting", ou.distinguishedName)
        res, message = ou.delete_object(confirmed=True)
        if message == LDAPWrapper.ERR_DELETE_NONLEAF:
            print(" ERROR Deleting")
            children = ou.get_children()
            print(" ou", ou, " has children ", children)
            print("We must delete them!!!!! 3 seconds before children are destroyed.")
            time.sleep(3)
            for child in children:
                print("   deleting child ", child)
                child.delete_object(confirmed=True)
            print("now trying to delete parent again")
            success, message = ou.delete_object(confirmed=True)
            if not success:
                print("Still having issue deleting parent [", ou, "] after child destruction", message)
