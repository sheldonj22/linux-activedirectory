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
  "description": "descrasdfasd fasdf asd fsadf sad"  
}
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
    "someLdapAttribute":"Some VAlue",
    "someOtherAttr":"Some other Value"
}
# if there are additional attributes that aren't normally returned 
return_attributes = ["FetchNonDefaultAttribute","AnotherAttribute"]
results = ld.get_user(search_attrs=search_attributes, 
                            properties=return_attributes)
# 0th index is the first user that matched the query, 1st is the second, and so on. 
results[0].samAccountName   
results[0].title
results[0].FetchNonDefaultAttribute      
results[0].AnotherAttribute                    
```
get_user always returns a list, if there are matches, items will be User objects. The user object's attributes are set based on the attributes that were fetched from the query.
