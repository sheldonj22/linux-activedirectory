
# Description  
This is a wrapper around python-ldap that attempts to create a more convenient way to perform basic Active Directory (although it will likely work for other LDAP compliant directories) tasks from a Linux machine.  
  
Some tasks that are supported: Creating, reading, updating and deleting users, ous, groups and computers, add/removing users from groups, moving objects to different OUs, resetting passwords (LDAPS required), recursive group membership checking, set/modify account expiration, testing authentication credentials against the DC, and others.  
  
# Create Connection  
Create an LDAP connection object. Note that without LDAPS you can't create/change user passwords.  
  
domain: the domain of the directory, is appended to usernames during bind and used as the server if server is not supplied.  
server: the LDAP server (ip or host) to connect to  
ldaps: Whether or not to attempt to setup LDAPS  
read_only: will skip over actions that make changes and only perform get operations.  
```  
ld = LDAPWrapper(domain="localhost.com", user=settings['user'],    
  passw=settings['password'], server=settings['server'],    
  ldaps=True,    
  read_only=False)  
```  
  
# Users  
## Create  
```  
  
username = "bob1"  
user = {    
  "samAccountName": username,    
  "cn": username,    
  "givenName": username,    
  "sn": "last",    
  "password": "superRSecurePa@ssvv0rd",    
  "title": "Test Title",    
  "displayname": "name name",    
  "department": "department",    
"description": "descrasdfasd fasdf asd fsadf sad" }  
user1 = ld.create_user(ou=ou, user_attrs=user1_attrs)  
print(user1.samAccountName)  
```  
  
## Read / Search  
```  
# some helper paramaters so you can quickly query common attributes  
ld.get_user(sam=user1.samAccountName)  
ld.get_user(title="\*Manager*")  
ld.get_user(department="finance")  
  
# Specify your own attributes to search by with a dictionary  
search_attributes = {  
 "someLdapAttribute":"Some VAlue", "someOtherAttr":"Some other Value"}  
# if there are additional attributes that aren't normally returned return_attributes = ["FetchNonDefaultAttribute","AnotherAttribute"]  
results = ld.get_user(search_attrs=search_attributes,   
                            properties=return_attributes)  
# 0th index is the first user that matched the query, 1st is the second, and so on. results[0].samAccountName results[0].title  
results[0].FetchNonDefaultAttribute results[0].AnotherAttribute
```

get_user always returns a list, if there are matches, items will be User objects. The user object's attributes are set based on the attributes that were fetched from the query.

## Update
```
# get User objects
user = results[0]
manager = results[1]

# Helper functions for common attributues
user.set_email("bob@bob.com")
user.set_manager(manager)
user.set_manager(None)
user.set_name(first="Bob", last="Jackson")
user.set_description("This is my new description")
user.append_description("->Add to end of existing description")  
user.prepend_description("Add to beginning of existing description<-")
user.set_office("office")
user.set_phone("phone")  
user.set_initials("initials")  
user.set_title("title")  
user.set_department("department")  
user.set_company("company")

# But you can set any arbitrary attribute
user.set_attr("attributeName", "Some value")

# the User object attributes are kepted local, changes made are not 
#   reflected in the local object until after the object is 'refreshed'. 
#   refresh the object to get the latest attributes from the LDAP server.
user = user1.refresh()

ou = ou_results[0] # See OU section if you need info on getting OU objects
user.move(ou)
user = user.refresh() # important to refresh after moves as the DN changes. 
```


## Delete
```
user = results[0]
user.delete_object() # this will prompt for confirmation
user.delete_object(confirm=True) # this will not prompt for input
```

# Groups

## Create
```
ou = ou_results[0] # See OU section if you need info on getting OU objects

ld.create_group(name="name2", description="desc2", parent_ou=ou)  
```

## Read/Search
```
group_search_results = ld.get_group("name*") # wildcard *, always returns array
group = group_search_results[0]
members = group.members # a list of DNs from the member attribute, no extra queries
members = group.fetch_members() # by default, does no recursion, returns an array of User/Group objects

# will go up to 99 groups deep and flatten things to a single dimension list of its members. 
# IE: Groups are replaced by their users as 'members' in the root group membership list, 
#     recursion does not result in arrays of arrays. 
recursed_members = group.fetch_members(recursion_depth=99)  # This results in extra server queries.
```

## Update
```
user = results[0]
group = ld.get_group("group name")[0]
group.add_member(user)
group = group.refresh()
group.members # = [<user object just added>]
group.remove_member(user)
group.fetch_members() # = []
```

## Delete
```
group = ld.get_group("group name")[0]
group.delete_obejct()
```