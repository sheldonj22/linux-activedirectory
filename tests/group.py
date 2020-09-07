from src.lindap import Group, User
from tests.util import gen_random_str


def test_init_group(ld, ou, users):
    name1 = gen_random_str()
    ld.create_group(name=name1)
    g1 = ld.get_group(name1)
    assert len(g1) == 1
    g1 = g1[0]

    name2 = gen_random_str()
    desc2 = gen_random_str()
    ld.create_group(name=name2, description=desc2)
    g2 = ld.get_group(name2)
    assert len(g2) == 1
    g2 = g2[0]

    name3 = gen_random_str()
    g3 = ld.create_group(name=name3, parent_ou=ou)
    assert type(g3) == Group

    assert g1.name == name1
    assert g2.name == name2
    assert g2.description == desc2
    assert g3.name == name3
    assert ou.name in g3.distinguishedName
    # intentionally using member and members to test property alias
    assert len(g3.member) == 0 and  len(g2.members) == 0 and  len(g1.members) == 0

    # Add members and verify their addition
    g3.add_member(users[0])
    g3.add_member(users[1])
    g3 = g3.refresh()
    print(g3.members)
    assert len(g3.members) == 2
    members = g3.fetch_members()
    assert len(members) == 2
    assert users[0].objectGUID == members[0].objectGUID
    assert users[1].objectGUID == members[1].objectGUID

    # remove member and test member length and remaining member to ensure it removed the right one
    g3.remove_member(users[1])
    g3 = g3.refresh()
    assert len(g3.members) == 1
    assert users[0].distinguishedName == g3.members[0]

    # RECURSIVE MEMBERSHIP
    g3.remove_member(users[0])
    g3.add_member(g1)
    g3.add_member(g2)
    g1.add_member(users[0])
    g2.add_member(users[1])
    g3 = g3.refresh()  # TODO - find a way to eliminate/minimize the need to refresh
    # with no recursion, 2 Groups should appear
    members = g3.fetch_members(recursion_depth=0)
    assert len(members) == 2
    for member in members:
        assert type(member) == Group

    # when recursed, the 2 groups should be replace with their 2 users
    members = g3.fetch_members(recursion_depth=1)
    assert len(members) == 2
    for member in members:
        assert type(member) == User

    # get group worked at beginning with len=1, delete object and make sure len=0
    g1.delete_object(confirmed=True)
    g2.delete_object(confirmed=True)
    assert len(ld.get_group(g1.name)) == 0
    assert len(ld.get_group(g2.name)) == 0
    return g3.refresh()

