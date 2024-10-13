import pandas as pd
import requests

def decoding_a_secret_message(url):
    # retrieve content from web page
    response = requests.get(url)
   
    if response.status_code != 200:
        print("Error fetching the webpage.")
        return None

    tables = pd.read_html(response.text)

    if not tables:
        print("No tables found on the webpage.")
        return None
   
    # Provided the document will always have the same format, the data is in 1st table found
    web_data = tables[0]

    # Promote the 1st row to column headers
    web_data.columns = web_data.iloc[0]  # Set the 1st row as the header
    web_data = web_data[1:]  # Remove the 1st row from the data
    web_data.reset_index(drop=True, inplace=True)  # Reset index

    # Extract x-coordinates, y-coordinates, and characters from the DataFrame
    x_coordinates = web_data['x-coordinate'].astype(int)  # Ensure the coordinates are integers
    y_coordinates = web_data['y-coordinate'].astype(int)
    characters = web_data['Character']

    # With the minimum possible value of these coordinates is 0, determine the maximum size of the grid
    maximum_x = x_coordinates.max()
    maximum_y = y_coordinates.max()

    # Initialize the grid with spaces
    grid = [[' ' for _ in range(maximum_x + 1)] for _ in range(maximum_y + 1)]

    # Populate the grid with the provided characters
    for x, y, char_value in zip(x_coordinates, y_coordinates, characters):
        grid[y][x] = char_value

    # Print the grid
    for row in grid:
        print(''.join(row))

if __name__ == "__main__":
    url = 'https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub'
    decoding_a_secret_message(url)