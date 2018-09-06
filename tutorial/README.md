# Python 3.7 queries on orientDB via orientDB REST
### Prerequisites
Linux or Mac is recommended, and you need Python 3.6+. If you are using Windows, either setup a VM or use the Linux Subsystem
Python 3.7, orientdb-3.x
- note: pyorient does not support 3.0.6 yet ->“Protocol version 37 is not supported yet by this client”

### create venv
```
python3 -m venv project_name
source <path_to_project>/bin/activate
which python3
which python
```

### Download orientdb GA Community Edition 3.0.6
- https://orientdb.com/download-previous/
- unzip to desired path, start the server
- when prompted, enter password for root->root123
```
cd <path_to_server>
./bin/server.sh
```
![Alt text](img/odb_startup.png)

### verify installation
server credentials in $ORIENTDB_HOME/config/orientdb-server-config.xml
```
./bin/console.sh
connect remote:localhost root mypassword
list databases
```
![Alt text](img/odb_console.png)

### connecting to  web studio
any of the following wil work
```
http://localhost:2480
http://127.0.0.1:2480/
http://0.0.0.0:2480
```
- Starting with OrientDB v.3.x a new demo database (demodb) is included.
- other public databases can be imported
![Alt text](img/odb_login.png)
![Alt text](img/odb_db_import.png)

### Data model
- demodb is the database of an hypothetical Travel Agency that runs a public social platform.
![Alt text](img/odb_datamodel.png)
![Alt text](img/odb_obj.png)

### Queries
- copy or clone the project
- edit settings.py where necessary
![Alt text](img/odb_settings.png)


### Example 1: Find the 'year of birth' of the Profiles, and how many Profiles were born in the same year
```
SELECT count(*) as NumberOfProfiles, Birthday.format('yyyy') AS YearOfBirth FROM Profiles GROUP BY YearOfBirth ORDER BY NumberOfProfiles DESC
```
```
python profile_eg_1.py
[
  {
    "NumberOfProfiles": 34,
    "YearOfBirth": "1997"
  },
  {
    "NumberOfProfiles": 29,
    "YearOfBirth": "1953"
  },
  {
    "NumberOfProfiles": 29,
    "YearOfBirth": "1955"
  },
  {
    "NumberOfProfiles": 28,
    "YearOfBirth": "1951"
  },
  {
    "NumberOfProfiles": 26,
    "YearOfBirth": "1959"
  },
  .....

```
![Alt text](img/odb_eg_1_rest.png)

### Example 2: Find the top 3 Profiles that have the highest number of Friends
```
SELECT @rid as Profile_RID, Name, Surname, both('HasFriend').size() AS FriendsNumber FROM `Profiles` ORDER BY FriendsNumber DESC LIMIT 3
```

```
python profile_eg_2.py
[
  {
    "Profile_RID": "#48:116",
    "Name": "Jeremiah",
    "Surname": "Schneider",
    "FriendsNumber": 12
  },
  {
    "Profile_RID": "#45:0",
    "Name": "Frank",
    "Surname": "OrientDB",
    "FriendsNumber": 11
  },
  {
    "Profile_RID": "#46:80",
    "Name": "Tom",
    "Surname": "McGee",
    "FriendsNumber": 11
  }
]
```
![Alt text](img/odb_eg_2_rest.png)

### Example 2-1: Find Colin's Friends
```
# SELECT EXPAND( BOTH() ) FROM Profiles WHERE Name = 'Colin' AND Surname='OrientDB' ORDER BY FriendsNumber
SELECT @rid as Profile_RID, Name, Surname, both('HasFriend').size() AS FriendsNumber FROM `Profiles` ORDER BY FriendsNumber DESC LIMIT 3
```
![Alt text](img/odb_eg_3_rest.png)
```
[
  {
    "@type": "d",
    "@rid": "#43:0",
    "@version": 12,
    "@class": "Profiles",
    "Email": "santo@example.com",
    "in_HasFriend": [
      "#218:0",
      "#219:1"
    ],
    "Bio": "OrientDB Team",
    "Id": 3,
    "Gender": "Male",
    "out_HasFriend": [
      "#220:2",
      "#221:2",
      "#222:2",
      "#223:2",
      "#224:2",
      "#217:3",
      "#218:3",
      "#219:3"
    ],
    "in_HasProfile": [
      "#190:0"
    ],
    "Surname": "OrientDB",
    "Name": "Santo",
    "@fieldTypes": "in_HasFriend=g,Id=l,out_HasFriend=g,in_HasProfile=g"
  },
  ........
]
```

### Example 2-2: Find Colin's friends who are also Customers
```
MATCH {Class: Profiles, as: profile, where: (Name='Colin' AND Surname='OrientDB')}-HasFriend-{Class: Profiles, as: friend}<-HasProfile-{class: Customers, as: customer}
RETURN $pathelements
```
![Alt text](img/odb_eg_4.png)
```
python profile_eg_4.py
[
  {
    "Friend_RID": "#41:1",
    "Friend_Name": "Colin",
    "Friend_Surname": "OrientDB",
    "Customer_RID": "#121:0",
    "Customer_OrederedId": 1
  },
  {
    "Friend_RID": "#45:0",
    "Friend_Name": "Frank",
    "Friend_Surname": "OrientDB",
    "Customer_RID": "#122:0",
    "Customer_OrederedId": 2
  },
  .........
```

### Example 2-3: Find Colin's Friends who are also Customers, and the Countries they are from
```
MATCH {Class: Profiles, as: profile, where: (Name='Santo' AND Surname='OrientDB')}-HasFriend-{Class: Profiles, as: friend}<-HasProfile-{class: Customers, as: customer}-IsFromCountry->{Class: Countries, as: country}
RETURN $pathelements
```
![Alt text](img/odb_eg_2_3.png)
```
python profile_eg_5.py
[{"Friend_RID":"#45:0","Friend_Name":"Frank","Friend_Surname":"OrientDB","Customer_RID":"#122:0","Customer_OrederedId":2,"FriendIsFrom":"Italy"},{"Friend_RID":"#41:0","Friend_Name":"Luca","Friend_Surname":"OrientDB","Customer_RID":"#123:0","Customer_OrederedId":3,"FriendIsFrom":"Italy"},{"Friend_RID":"#42:0","Friend_Name":"Luigi","Friend_Surname":"OrientDB","Customer_RID":"#124:0","Customer_OrederedId":4,"FriendIsFrom":"Italy"},{"Friend_RID":"#43:0","Friend_Name":"Santo","Friend_Surname":"OrientDB","Customer_RID":"#126:0","Customer_OrederedId":6,"FriendIsFrom":"Italy"},{"Friend_RID":"#42:1","Friend_Name":"Andrey","Friend_Surname":"OrientDB","Customer_RID":"#125:0","Customer_OrederedId":5,"FriendIsFrom":"Ukraine"}]
```

### Example 2-4: Find Colin's Friends who are also Customers, and the Countries they are from
```
MATCH {Class: Profiles, as: profile, where: (Name='Santo' AND Surname='OrientDB')}-HasFriend-{Class: Profiles, as: friend}<-HasProfile-{class: Customers, as: customer}-IsFromCountry->{Class: Countries, as: country}
RETURN $pathelements
```
![Alt text](img/odb_eg_2_3.png)
```
python profile_eg_5.py
[{"Friend_RID":"#45:0","Friend_Name":"Frank","Friend_Surname":"OrientDB","Customer_RID":"#122:0","Customer_OrederedId":2,"FriendIsFrom":"Italy"},{"Friend_RID":"#41:0","Friend_Name":"Luca","Friend_Surname":"OrientDB","Customer_RID":"#123:0","Customer_OrederedId":3,"FriendIsFrom":"Italy"},{"Friend_RID":"#42:0","Friend_Name":"Luigi","Friend_Surname":"OrientDB","Customer_RID":"#124:0","Customer_OrederedId":4,"FriendIsFrom":"Italy"},{"Friend_RID":"#43:0","Friend_Name":"Santo","Friend_Surname":"OrientDB","Customer_RID":"#126:0","Customer_OrederedId":6,"FriendIsFrom":"Italy"},{"Friend_RID":"#42:1","Friend_Name":"Andrey","Friend_Surname":"OrientDB","Customer_RID":"#125:0","Customer_OrederedId":5,"FriendIsFrom":"Ukraine"}]

### Example 2-5: Among Colin's Friends, find the top 3 Customers that placed the highest number of Orders
```
SELECT
  OrderedId as Customer_OrderedId,
  in('HasCustomer').size() as NumberOfOrders,
  out('HasProfile').Name as Friend_Name,
  out('HasProfile').Surname as Friend_Surname
FROM (
  SELECT expand(customer)
  FROM (
    MATCH {Class: Profiles, as: profile, where: (Name='Santo' AND Surname='OrientDB')}-HasFriend-{Class: Profiles, as: friend}<-HasProfile-{class: Customers, as: customer}
    RETURN customer
  )
)
ORDER BY NumberOfOrders DESC
LIMIT 3

```
![Alt text](img/odb_eg_2_3.png)
```
python profile_eg_6.py
[
  {
    "Customer_OrderedId": 4,
    "NumberOfOrders": 4,
    "Friend_Name": [
      "Luigi"
    ],
    "Friend_Surname": [
      "OrientDB"
    ]
  },
  {
    "Customer_OrderedId": 2,
    "NumberOfOrders": 3,
    "Friend_Name": [
      "Frank"
    ],
    "Friend_Surname": [
      "OrientDB"
    ]
  },
  {
    "Customer_OrderedId": 1,
    "NumberOfOrders": 1,
    "Friend_Name": [
      "Colin"
    ],
    "Friend_Surname": [
      "OrientDB"
    ]
  }
]
```
### Example 2-6: Find all the Friends of Customer identified with OrderedId 1 that are not Customers (so that a product can be proposed)
```
SELECT
  @Rid as Friend_RID,
  Name as Friend_Name,
  Surname as Friend_Surname
FROM (
  SELECT expand(customerFriend)
  FROM (
    MATCH {Class:Customers, as: customer, where:(OrderedId=1)}-HasProfile-{Class:Profiles, as: profile}-HasFriend-{Class:Profiles, as: customerFriend} RETURN customerFriend
  )
)
WHERE in('HasProfile').size()=0
ORDER BY Friend_Name ASC

```
![Alt text](img/odb_eg_2_7.png)
```
python profile_eg_7.py
[{"Friend_RID": "#47:0", "Friend_Name": "Emanuele", "Friend_Surname": "OrientDB"}, {"Friend_RID": "#44:0", "Friend_Name": "Enrico", "Friend_Surname": "OrientDB"}, {"Friend_RID": "#46:0", "Friend_Name": "Gabriele", "Friend_Surname": "OrientDB"}, {"Friend_RID": "#48:0", "Friend_Name": "Paolo", "Friend_Surname": "OrientDB"}, {"Friend_RID": "#43:1", "Friend_Name": "Sergey", "Friend_Surname": "OrientDB"}]
```


## Author
* **Ishafizan Ishak**

