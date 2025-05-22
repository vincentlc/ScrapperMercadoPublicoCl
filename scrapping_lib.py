import pandas as pd
import requests
from datetime import datetime


def load_categories_from_csv(filepath):
    """
    Load categories from a CSV file.

    Args:
        filepath (str): Path to the CSV file containing categories.

    Returns:
        list: A list of category IDs.
    """
    try:
        # Assuming the CSV has a column named 'category_id'
        categories_df = pd.read_csv(filepath)
        return categories_df['category_id'].tolist()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return []
    except KeyError:
        print("Error: The CSV file must contain a 'category_id' column.")
        return []
    



def fetch_offers_by_category(category_id, api_ticket):
    """
    Fetch offers from Mercado Público API for a specific category.

    Args:
        category_id (str): The category ID to search for.
        api_ticket (str): The API ticket for authentication.

    Returns:
        list: A list of offers for the given category.
    """
    url = f"https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json?ticket={api_ticket}&CodigoCategoria={category_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('Listado', [])
        else:
            print(f"Error fetching category {category_id}: HTTP {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching category {category_id}: {e}")
        return []
    

def filter_offers_by_date(offers, current_date):
    """
    Filter offers to include only those with a date later than the current date.

    Args:
        offers (list): A list of offers (each offer is a dictionary).
        current_date (datetime): The current date for filtering.

    Returns:
        list: A list of filtered offers.
    """
    filtered_offers = []
    for offer in offers:
        try:
            # Assuming 'FechaCierre' is the key for the offer's closing date
            offer_date = datetime.fromisoformat(offer['FechaCierre'])
            if offer_date > current_date:
                filtered_offers.append(offer)
        except KeyError:
            print("Error: Offer does not contain 'FechaCierre' key.")
        except ValueError:
            print("Error: Invalid date format in 'FechaCierre'.")
    return filtered_offers



def save_to_csv(data, filename):
    """
    Save the data to a CSV file.

    Args:
        data (list): The data to save.
        filename (str): The name of the output CSV file.
    """
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}.")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")