import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Function to get user input for the season
def get_season():
    season = input("Enter the season (e.g., 2023-2024): ")
    return season

# Function to check if data has already been scraped
def check_existing_data(season):
    filename = f"{season}_ligue1_data.csv"
    return os.path.exists(filename)

# Function to scrape data from the schedule page
def scrape_schedule(season):
    url = f"https://fbref.com/en/comps/13/{season}/schedule/{season}-Ligue-1-Scores-and-Fixtures"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    match_links = []
    # Extract match URLs from the schedule page
    for link in soup.select('a[href^="/en/matches/"]'):
        match_links.append("https://fbref.com" + link['href'])
    
    return match_links

# Function to scrape match data
def scrape_match_data(match_url):
    response = requests.get(match_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    shots_data = []
    # Example: Extract match details (adjust selectors as needed)
    match_date = soup.select_one('.match_date_class').text  # Replace with actual class
    venue = soup.select_one('.venue_class').text  # Replace with actual class
    
    # Extract shot data (example, adjust as needed)
    for shot in soup.select('.shot_class'):  # Replace with actual class for shots
        minute = shot.select_one('.minute_class').text  # Replace with actual class
        squad = shot.select_one('.squad_class').text  # Replace with actual class
        xG = shot.select_one('.xG_class').text  # Replace with actual class
        PSxG = shot.select_one('.PSxG_class').text  # Replace with actual class
        outcome = shot.select_one('.outcome_class').text  # Replace with actual class
        distance = shot.select_one('.distance_class').text  # Replace with actual class
        body_part = shot.select_one('.body_part_class').text  # Replace with actual class
        
        shots_data.append([1, match_date, venue, minute, squad, xG, PSxG, outcome, distance, body_part])  # Adjust week number as needed
    
    return shots_data

# Main function
def main():
    season = get_season()
    
    if check_existing_data(season):
        print(f"Data for the season {season} has already been scraped.")
        return
    
    match_links = scrape_schedule(season)
    all_shots_data = []
    
    for match_url in match_links:
        shots_data = scrape_match_data(match_url)
        all_shots_data.extend(shots_data)
        time.sleep(1)  # Throttle requests to avoid getting blocked
    
    # Create a DataFrame and save to CSV
    df = pd.DataFrame(all_shots_data)
    df.to_csv(f"{season}_ligue1_data.csv", index=False)

if __name__ == "__main__":
    main()
