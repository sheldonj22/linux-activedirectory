import datetime
import string
from tests.util import gen_random_str
from colorama import Fore, Style
NOW = datetime.datetime.now()
TOM = datetime.datetime.now() + datetime.timedelta(days=1)
TOM30 = datetime.datetime.now() + datetime.timedelta(days=1, minutes=30)
TOM60 = datetime.datetime.now() + datetime.timedelta(days=1, minutes=60)
YEST = datetime.datetime.now() - datetime.timedelta(days=1)


def gen_user():
    p = gen_random_str(choices=string.ascii_lowercase)+gen_random_str(choices=string.digits)+gen_random_str(choices=string.ascii_uppercase)
    u = gen_random_str()

    user = {
            "samAccountName": u,
            "cn": u,
            "givenName": u,
            "sn": "last",
            "password": p,
            "title": "Test Title",
            "displayname": "name name",
            "department": "department",
            "description": "descrasdfasd fasdf asd fsadf sad"
            }
    return user, p


# create users
def test_init_user(ld, ou):
    user1_attrs, passw1 = gen_user()
    user1 = ld.create_user(ou=ou, user_attrs=user1_attrs)
    print(f"{Fore.CYAN}ATTEMPTING INITIAL AUTH{Style.RESET_ALL}")
    assert ld.auth(user1.samAccountName, passw1)
    print(f"{Fore.GREEN}[ X ]{Style.RESET_ALL} Passed initial authentication")

    new_pw=gen_random_str(choices=string.ascii_lowercase)+gen_random_str(choices=string.digits)+gen_random_str(choices=string.ascii_uppercase)
    print(f"{Fore.CYAN}ATTEMPTING PASSWORD RESET{Style.RESET_ALL}")
    user1.reset_password(new_password=new_pw)
    print(f"{Fore.CYAN}ATTEMPTING RESET AUTHENTICATION{Style.RESET_ALL}")
    assert ld.auth(user1.samAccountName, new_pw)
    print(f"{Fore.GREEN}[ X ]{Style.RESET_ALL} Passed PW reset and authentication")

    """
        Expiration
    """
    print(f"{Fore.CYAN}ATTEMPTING EXPIRATION SET{Style.RESET_ALL}")
    user1.set_expiration(YEST)
    assert user1.is_expired
    assert not ld.auth(user1.samAccountName, new_pw)
    print(f"{Fore.GREEN}[ X ]{Style.RESET_ALL} Passed expired auth test")

    print(f"{Fore.CYAN}ATTEMPTING EXPIRATION SET 2{Style.RESET_ALL}")
    user1.set_expiration(TOM30)
    user1 = user1.refresh()
    assert not user1.is_expired
    assert ld.auth(user1.samAccountName, new_pw)
    print(f"{Fore.GREEN}[ X ]{Style.RESET_ALL} Passed not expired auth test")

    print(f"{Fore.CYAN}ATTEMPTING GET & CLEAR EXPIRATION{Style.RESET_ALL}")
    # test ballpark accuracy of actual timestamps
    assert TOM < user1.expiration < TOM60
    # ensure we can not authenticate
    user1.set_expiration(YEST)
    assert not ld.auth(user1.samAccountName, new_pw)
    # clear expiration and ensure we retrieved it properly and we can authenticate
    user1.set_expiration(None)
    user1 = ld.get_user(sam=user1.samAccountName)[0]
    assert not user1.expiration
    assert ld.auth(user1.samAccountName, new_pw)
    print(f"{Fore.GREEN}[ X ]{Style.RESET_ALL} Passed ALL expiration tests")


    """
        Enable/Disable
    """
    print(f"{Fore.CYAN}ATTEMPTING DISABLE/ENABLE{Style.RESET_ALL}")
    user1.disable()
    user1 = user1.refresh()
    assert user1.is_disabled
    assert not ld.auth(user1.samAccountName, new_pw)
    user1.enable()
    user1 = user1.refresh()
    assert not user1.is_disabled
    assert ld.auth(user1.samAccountName, new_pw)
    print(f"{Fore.GREEN}[ X ]{Style.RESET_ALL} Passed Disable/Enable")

    """
        Set/Get various attributes
    """
    fn = "bob"
    ln = "tom"
    email = "bob@bob.com"
    description = "new desc"
    description_ap = "||"
    office = "office"
    phone = "phone"
    initials = "123"
    title = "title2"
    department = "department2"
    company = "company2"

    manager = ld.create_user(ou, gen_user()[0])
    user1.set_email(email)
    user1.set_manager(manager)
    user1.set_name(first=fn, last=ln)
    user1.set_description(description)
    user1 = user1.refresh()
    assert user1.givenName == fn
    assert user1.sn == ln
    assert user1.manager == manager.distinguishedName
    assert user1.email == email
    assert user1.description == description
    user1.append_description(description_ap)
    user1.prepend_description(description_ap)
    user1.set_office(office)
    user1.set_phone(phone)
    user1.set_initials(initials)
    user1.set_title(title)
    user1.set_department(department)
    user1.set_company(company)
    user1 = user1.refresh()
    print("desc:", user1.office)
    assert user1.description == description_ap+description+description_ap
    assert user1.office == office
    assert user1.phone == phone
    assert user1.initials == initials
    assert user1.title == title
    assert user1.department == department
    assert user1.company == company
    print(f"{Fore.GREEN}[ X ]{Style.RESET_ALL} Passed setting/getting attributes")
    return user1, manager


def test_load_user(ld, ou, number=1000):
    st = datetime.datetime.now()
    users = []
    for i in range(number):
        user1_attrs, passw1 = gen_user()
        users.append({"attr":user1_attrs, "pw":passw1})
        ld.create_user(ou=ou, user_attrs=user1_attrs)


    et = datetime.datetime.now()
    print("Run time: ", et-st)