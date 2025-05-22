from scrapping_lib import fetch_offers_by_category, filter_offers_by_date, load_categories_from_csv, save_to_csv
import pandas as pd
import argparse
from datetime import datetime
import os

def parsing_file():
    # Define paths for the config files
    config_folder = os.path.join(os.getcwd(), 'config')
    ticket_file = os.path.join(config_folder, 'ticket.txt')
    categories_file = os.path.join(config_folder, 'categories.csv')

    # Check if the config folder and files exist
    if not os.path.exists(config_folder):
        print(f"Error: Config folder not found at {config_folder}.")
        return
    if not os.path.exists(ticket_file):
        print(f"Error: Ticket file not found at {ticket_file}.")
        return
    if not os.path.exists(categories_file):
        print(f"Error: Categories file not found at {categories_file}.")
        return

    # Read the API ticket from ticket.txt
    with open(ticket_file, 'r') as file:
        api_ticket = file.read().strip()

    # Load categories from categories.csv
    categories = load_categories_from_csv(categories_file)
    return api_ticket, categories
    

def main():
    """
    Main function to orchestrate the workflow.
    """
    api_ticket, categories = parsing_file()
    if not categories:
        print("No categories found in the categories file. Exiting.")
        return

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Ingresar los datos para la búsqueda de información')
    parser.add_argument('--sdt', metavar='Start Date', type=str, required=True, help='Fecha de inicio en formato YYYY-MM-DD')
    parser.add_argument('--edt', metavar='End Date', type=str, required=True, help='Fecha de término en formato YYYY-MM-DD')
    args = parser.parse_args()

    # Validate and parse dates
    try:
        start_date = datetime.fromisoformat(args.sdt)
        end_date = datetime.fromisoformat(args.edt)
        if start_date > end_date:
            print("Error: Start date must be earlier than end date.")
            return
    except ValueError:
        print("Error: Invalid date format. Use YYYY-MM-DD.")
        return

    # Fetch and filter offers
    all_offers = []
    current_date = datetime.now()

    for category in categories:
        print(f"Fetching offers for category {category}...")
        offers = fetch_offers_by_category(category, api_ticket)
        filtered_offers = filter_offers_by_date(offers, current_date)
        all_offers.extend(filtered_offers)

    # Save the filtered offers to a CSV file
    if all_offers:
        save_to_csv(all_offers, 'filtered_offers.csv')
    else:
        print("No offers found matching the criteria.")

    # Optionally push to Google Sheets
    # push_to_google_sheets(all_offers, 'your_spreadsheet_id', 'Sheet1!A1', 'credentials.json')

if __name__=='__main__':
    main()