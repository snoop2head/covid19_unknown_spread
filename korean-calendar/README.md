# korean-calendar
![GitHub](https://img.shields.io/github/license/gnokoheat/korean-calendar) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/gnokoheat/korean-calendar) ![GitHub last commit](https://img.shields.io/github/last-commit/gnokoheat/korean-calendar)

- MongoDB BSON and JSON data of Korean calendar 🇰🇷
- 2000y ~ 2100y Korean calendar with Solar calendar, Lunar calendar, Day of week and Holiday

## Detail
**1. BSON and JSON keys (Column)**
- sc : string, Solar calendar 양력
- lc : string, Lunar calendar 음력
- w : int, Day of week 요일 (1 : Sun, 2 : Mon, 3 : Tue, 4 : Wed, 5 : Thu, 6 : Fri, 7 : Sat)
- h : bool, Holiday 휴일
- ht : string, Holiday detail 휴일 내용
  
**2. Data example**
```
{
    "_id" : ObjectId("5dca1e4990837450133db3f6"),
    "sc" : "2000-01-01",
    "lc" : "1999-11-25",
    "w" : 7,
    "h" : true,
    "ht" : "신정"
}
```

## Usage
- Insert BSON or JSON data to MongoDB Collection
```
mongorestore -h 127.0.0.1:27017 -d mydb -c mycollection ./korean-calendar.bson
```
OR
```
mongoimport -h 127.0.0.1:27017 -d mydb -c mycollection --file ./korean-calendar.json
```
