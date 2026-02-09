import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from serpapi import GoogleSearch

API_KEY = os.getenv("SERPAPI_KEY")  # Ensure you have your SerpAPI key set in environment variables
HOME_AIRPORT = "ATL"
DESTINATION_REGION = "Asia"
MAX_PRICE = 450

def search_error_fares():
    params = {
        "api_key": API_KEY,
        "engine": "google_travel_explore",
        "departure_id": HOME_AIRPORT,
        "location": DESTINATION_REGION,
        "currency": "USD",
        "hl": "en",
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Parse the 'destinations' list from the JSON response
        destinations = results.get("destinations", [])
        
        found_deals = []

        for dest in destinations:
            # Extract price (often formatted like "$1,200", so we clean it)
            price_raw = dest.get("flight_price") 
            city_name = dest.get("name")
            
            if price_raw:
                # Remove currency symbols and commas to compare numbers
                price_val = int(str(price_raw).replace('$', '').replace(',', ''))
                
                if price_val < MAX_PRICE:
                    deal = {
                        "city": city_name,
                        "price": price_val,
                        "url": dest.get("google_flights_link") # Direct link to book
                    }
                    found_deals.append(deal)

        return found_deals
    except Exception as e:
        print(f"Error occurred: {e}")
        return []
if __name__ == "__main__":
    deals = search_error_fares()
    
    if deals:
        print(f"🚨 FOUND {len(deals)} POTENTIAL ERROR FARES FROM {HOME_AIRPORT}:")
        for deal in deals:
            print(f"- {deal['city']} for ${deal['price']} -> {deal['url']}")
    else:
        print("No error fares found today.")
