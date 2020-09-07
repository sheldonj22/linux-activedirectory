def test_init_computer(ld, test_ou, comp_name="lab"):
    comp = ld.get_computer(comp_name)
    dc_ou = ld.get_ou("Domain Controllers")
    assert len(dc_ou) == 1
    dc_ou = dc_ou[0]
    assert len(comp) == 1
    comp = comp[0]
    print(comp)
    assert "Domain Controller" in comp.distinguishedName
    comp.move(test_ou)
    comp = comp.refresh()
    assert test_ou.distinguishedName in comp.distinguishedName
    comp.move(dc_ou)
    comp = comp.refresh()
    assert dc_ou.distinguishedName in comp.distinguishedName
