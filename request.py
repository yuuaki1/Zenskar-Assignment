import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API')
organisation = os.getenv('ORGANISATION')

headers = {
    "accept": "application/json",
    "organisation": organisation,
    "x-api-key": api_key,
    "content-type": "application/json"
}

#1 Creating a customer
customer = "https://api.zenskar.com/customers"
customer_payload = {
    "address": {
        "line1": "123 Frost Street",
        "city": "New York",
        "state": "New York",
        "zipCode": "10001",
        "country": "USA"
    },
    "communications_enabled": True,
    "auto_charge_enabled": True,
    "customer_name": "Example Customer",
}

customer_response = json.loads(requests.post(customer, json = customer_payload, headers= headers).text)
print("CUSTOMER JSON OBJECT: ")
print(customer_response) #throws error because invalid phone number ???

#2 Creating Products
products = "https://api.zenskar.com/products"
def create_products(name, type, description): 
    payload = {
        "type": type,
        "name": name,
        "description": description
    }

    response = requests.post(products, json = payload, headers= headers)
    return response.text

#converting JSON Response to python dictionary for easy access
one_time = json.loads(create_products("One time Fee", "product", "One time Subscription Fee"))
monthly_platform = json.loads(create_products("Monthly Platform Fee", "product", "Monthly Subscription Fee"))
monthly_user = json.loads(create_products("Monthly User Fee", "product", "Monthly User Usage Fee"))
print("PRODUCTS JSON OBJECT")
print(one_time)

#2.1 One time fee pricing

def create_pricing(product_id, pricing_type, unit_amount, offset, cadence, scheme_name, quantity = None, ):
    url = f'https://api.zenskar.com/products/{product_id}/pricing'
    if pricing_type == "per_unit":
        quantity = int(input('Enter the quantity: '))

    payload = {
        "pricing_data" : {
            "pricing_type" : pricing_type,
            "currency" : "USD",
            "unit_amount" : unit_amount,
        },
        "billing_period" : {
            "offset" : offset,
            "cadence": cadence
        },
        "add_to_catalog" : True,
        "is_recurring" : False,
        "name": scheme_name
    }
    
    if quantity: 
        payload[quantity] = {
            "type" : "metered",
            "quantity" : quantity
        }

    response = requests.post(url=url, json=payload, headers=headers)
    return response.text

one_time_pricing = json.loads(create_pricing(one_time['id'], "flat_fee", 5000, "prepaid", "P1D", "Subscription Fee"))
montly_platform_pricing = json.loads(create_pricing(monthly_platform['id'], "flat_fee", 10000, "postpaid", "P1M", "Subscription Fee"))
monthly_user_pricing = json.loads(create_pricing(monthly_user['id'], "per_unit", 60, "postpaid", "P1M", "Usage Fee"))


#3 Creating Contract
#Really sorry for the mishmash i could not figure out the contract's structure for the love of my life
contract = "https://api.zenskar.com/contract_v2"
contract_payload = {
    "status": "draft",
    "phases": [
        {
            "name": "Example Contract",
            "start_date": "2024-01-01T00:00:00",
            "end_date": "2024-12-31T23:59:59",
            "pricings": [
                {
                    "start_date": "2024-01-01T00:00:00",
                    "end_date": "2024-01-01T00:00:01",
                    "pricing_id": one_time_pricing['id'],
                    "product_id": one_time['id'],
                    "pricing": {
                        "pricing_data": {
                            "currency": "USD",

                            "pricing_period": { "cadence": "P1D" },
                            "unit_amount": 5000,
                            "pricing_type": "flat_fee"
                        },
                        "is_recurring": False,
                        "billing_period": {
                            "cadence": "P1D",
                            "offset": "prepaid"
                        },
                        "add_to_catalog": True
                    },
                    "product": one_time
                }, 
                {
                    "start_date": "2024-01-01T00:00:00",
                    "end_date": "2024-03-31T23:59:59",
                    "pricing_id": montly_platform_pricing['id'],
                    "product_id": monthly_platform['id'],
                    "pricing": {
                        "pricing_data": {
                            "currency": "USD",
                            "pricing_period": { "cadence": "P1M" },
                            "unit_amount": 10000,
                            "pricing_type": "flat_fee"
                        },
                        "is_recurring": False,
                        "billing_period": {
                            "cadence": "P1M",
                            "offset": "postpaid"
                        },
                        "add_to_catalog": True
                    },
                    "product": monthly_platform
                },
                {
                    "start_date": "2024-01-01T00:00:00",
                    "end_date": "2024-12-31T23:59:59",
                    "pricing_id": monthly_user_pricing['id'],
                    "product_id": monthly_user['id'],
                    "pricing": {
                        "pricing_data": {
                            "currency": "USD",
                            "unit": "user",
                            "unit_amount": 60,
                            "pricing_type": "per_unit"
                        },
                        "is_recurring": False,
                        "billing_period": {
                            "cadence": "P1M",
                            "offset": "postpaid"
                        },
                        "add_to_catalog": True
                    },
                    "product": monthly_user
                }
            ],
            "phase_type": "active"
        }, 
    ],
    "bill_parent_customer": False,
    "name": "Example Contract",
    "currency": "USD",
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-12-31T23:59:59",
    "customer_id": customer_response['id'],
    "renewal_policy": "do_not_renew"
}

contract_response = requests.post(contract, json = contract_payload, headers= headers)
print("CONTRACTS JSON OBJECT: ")
print(contract_response.text)