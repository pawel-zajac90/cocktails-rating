# Cocktails rating system
# Documentation
It's back-end application to rate cocktails in pubs. You can check ranking in few diffrent ways, add new pubs and cocktails.

## Error codes:

```bash
FAILED:
{'Status': 'Failed', 'Description': "Element doesn't exist."}
or
{'Status': 'Failed', 'Description': "Element does already exist."}
When you try to add object which is existing in database or call non-existent.

SUCCESS:
{'Status': 'Success'}
```

# Pubs
Management of pubs.

## GET
```bash
 /cocktails-rating/v1.0/pubs
```
By typing this URL adress, You will've access to list of Pubs.

## POST
```bash
/cocktails-rating/v1.0/pubs/<string:pub_name>
```
You can add new pub to database by typing new pub name as last word.

## DELETE
```bash
/cocktails-rating/v1.0/pubs/<int:id>
```
By typing int number on last word position you can delete some resources.


# Cocktails
Management of Cocktails.

## GET
```bash
/cocktails-rating/v1.0/cocktails/<int:pub_id>
```
By typing int number on last position you can get list of all values of cocktails from choosed pub.

## POST
```bash
/cocktails-rating/v1.0/cocktails/<string:drink_name>/<int:pub_id>
```
Type name of new drink and id of the pub to see add new cocktail into database.

## DELETE
```bash
/cocktails-rating/v1.0/cocktails/<int:drink_id>
```
You can type ID of drink do delete on last position.

# Rating system
With this methods you can rate your favorite cocktails.

## GET
```bash
/cocktails-rating/v1.0/rating
/cocktails-rating/v1.0/rating/<int:pub_id>
/cocktails-rating/v1.0/rating/<string:drink_name>
```
This GET methods can give You three answers:
First possibility (without any parameters) shows all cocktails and pubs 
Second possipility is an oportunity to check rates of all cocktails in choosed pub (by id).
Third option shows rate in all pubs for specified by id cocktail.


## PATCH
```bash
/cocktails-rating/v1.0/rating/<int:drink_id>/<int:ratea>
```
The most importannt part of app. By giving drink_id and value berween 1 and 5 we can rate cocktail existing in database.
