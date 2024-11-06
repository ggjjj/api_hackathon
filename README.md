
# How to try Python Home Grocery Managmenent API
Try the different endpoints of the API which is already hosted in `Render` environment by cicking [this link](https://api-hackathon-pcwp.onrender.com/docs)


# How to test the API locally

- Step 1 - Run Setup script to install all the dependencies
```
sudo ./scripts/setup.sh
```
- Step 2 - Export DATABASE_URL from the google document provided 
```
export DATABASE_URL=<insert-the-private-key>
```
- Step 3 - Run the application from the root directory
```
uvicorn src.main:app --reload
```

# Endpoint definitions and commands

#### Endpoint 1 A - Get all grocery items in the fridge
```
curl http://127.0.0.1:8000/items | jq .
```

#### Endpoint 1 B - Get all items filtered by category
```
curl 'http://127.0.0.1:8000/items?category=Dairy' -H 'accept: application/json' | jq .
```


#### Endpoint 1 C - Get all items filtered by category which are expiring
```
curl 'http://127.0.0.1:8000/items?category=Fruits&expiringSoon=true' -H 'accept: application/json' | jq .
```


#### Endpoint 2 - Add a new grocery item to the fridge
```
curl -X 'POST' \
  'http://127.0.0.1:8000/items' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Dragonfruit",
  "category": "Fruits",
  "quantity": "4",
  "expiration_date": "2024-11-16"
}' | jq .

```
#### Endpoint 3 - Get a grocery item by ID
```
curl 'http://127.0.0.1:8000/items/17' -H 'accept: application/json' | jq .
```
#### Endpoint 4 - Update a grocery item by ID
```
curl -X 'PUT' \
  'http://127.0.0.1:8000/updateItem/26' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 26,
  "name": "Paneer",
  "category": "Dairy 2",
  "quantity": "4",
  "expiration_date": "2024-11-09"
}' | jq .

```
#### Endpoint 5 - Delete a grocery item
```
curl -X 'DELETE' 'http://127.0.0.1:8000/deleteItem/3' -H 'accept: application/json' | jq .
```
#### Endpoint 6 - Search for a grocery item
```
curl -X 'GET' \
  'http://127.0.0.1:8000/searchItem?query=Paneer' \
  -H 'accept: application/json' | jq .

```
#### Endpoint 7 - Get all expired grocery items
```
curl -X 'GET' \
  'http://127.0.0.1:8000/expiredItems/' \
  -H 'accept: application/json' | jq .
```
