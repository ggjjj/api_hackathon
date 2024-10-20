# api_hackathon

# home-grocery-management
```
sudo apt update  # Make sure your package list is up to date

sudo apt install python3-venv  # Install venv if not already installed

python3 -m venv venv

source venv/bin/activate  # Activate the virtual environment

pip install fastapi uvicorn

uvicorn main:app --reload # run the main app
```
# home-grocery-management API commands
## Get all items
curl http://127.0.0.1:8000/items 
## Get all items by category
curl "http://127.0.0.1:8000/items?category=Dairy"
## Get alerts for expiring items
curl "http://127.0.0.1:8000/alerts?days=3"
## To add new grocery item
curl -X POST "http://127.0.0.1:8000/items" -H "Content-Type: application/json" -d '{
    "name": "Bananas",
    "category": "Fruits",
    "quantity": "6",
    "expirationDate": "2024-10-25"
}'

## To batch add items 
curl -X POST "http://127.0.0.1:8000/items/batch" -H "Content-Type: application/json" -d '{
    "items": [
        {
            "name": "Tomatoes",
            "category": "Vegetables",
            "quantity": "1 kg",
            "expirationDate": "2024-10-30"
        },
        {
            "name": "Bread",
            "category": "Bakery",
            "quantity": "2 loaves",
            "expirationDate": "2024-10-20"
        }
    ]
}'

## Update existing item
curl -X PUT "http://127.0.0.1:8000/items/1" -H "Content-Type: application/json" -d '{
    "name": "Organic Milk",
    "category": "Dairy",
    "quantity": "1 liter",
    "expirationDate": "2024-10-22"
}'

## Delete an item 
curl -X DELETE "http://127.0.0.1:8000/items/1"

## Generate shopping list
curl "http://127.0.0.1:8000/shopping-list?minQuantity=2&category=Fruits"
