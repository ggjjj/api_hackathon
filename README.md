
# Python Home Grocery Managmenent

## Setup

```
sudo apt update # Make sure your package list is up to date
sudo apt install python3-venv # Install venv if not already installed
python3 -m venv venv
source venv/bin/activate # Activate the virtual environment

pip install fastapi uvicorn
pip install SQLAlchemy
pip install python-decouple
pip install psycopg2
pip install python-dotenv
pip install pytest httpx pytest-asyncio
export DATABASE_URL=XXXX
uvicorn main:app --reload # run the main app
```

  

## Endpoint definitions and commands

#### Endpoint 1 - Get all grocery items in the fridge
```
curl http://127.0.0.1:8000/items
```

#### Endpoint 2 - Add a new grocery item to the fridge
```
curl -X POST “[http://127.0.0.1:8000/items](http://127.0.0.1:8000/items)” -H “Content-Type: application/json” -d '{
“name”: “Bananas”,
“category”: “Fruits”,
“quantity”: “6”,
“expirationDate”: “2024-10-25”
}
```
#### Endpoint 3 - Get a grocery item by ID
```
curl --request GET \
--url https://default-blackbird-viveks-organization-865b3-0.blackbird-relay.a8r.io/grocery-management/items/3 \
--header 'Accept: application/json'
```
#### Endpoint 4 - Update a grocery item by ID
```
curl --request PUT \
--url https://default-blackbird-viveks-organization-865b3-0.blackbird-relay.a8r.io/grocery-management/items/3 \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data '{ "id": 3, "name": "Coke", "category": "Beverages", "quantity": "2 litre", "expiration_date": "2025-08-21T00:00:00Z" }'
```
#### Endpoint 5 - Delete a grocery item
```
curl -X DELETE "http://127.0.0.1:8000/items/1"
```
#### Endpoint 6 - Search for a grocery item
```
curl --request GET \
--url 'https://default-blackbird-viveks-organization-865b3-0.blackbird-relay.a8r.io/grocery-management/items/search?query=Burger' \
--header 'Accept: application/json'
```
#### Endpoint 7 - Get all expired grocery items
```
curl "http://127.0.0.1:8000/items?category=Dairy"
```