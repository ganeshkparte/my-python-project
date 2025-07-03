import os                          # For interacting with the operating system
import requests                    # For sending HTTP requests to API
from pathlib import Path           # For handling file/folder paths easily
import re                          # For cleaning text using regular expressions

# URL to fetch all game data (as JSON)
API_URL = "https://partner-auth.dev-lab.uk/api/providers/1/games"

# Clean file/folder names by removing invalid characters (like /, \, :, *, etc.)
def clean_name(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

# Download image from URL and save it to the specified file path
def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)  # Send GET request to download image
        if response.status_code == 200:            # Check if download is successful
            with open(save_path, "wb") as f:       # Open file in binary write mode
                for chunk in response.iter_content(1024):  # Read image in chunks
                    f.write(chunk)                 # Write chunks to file
            print(f"[✓] Downloaded: {save_path}")  # Print success message
        else:
            print(f"[!] Failed to download image: {url}")  # Print failure
    except Exception as e:
        print(f"[!] Error downloading image: {e}")  # Catch and show any unexpected error

# Main function to run the entire process
def main():
    try:
        response = requests.get(API_URL)           # Send GET request to API
        response.raise_for_status()                # Raise error for bad responses (like 404/500)
        games = response.json()                    # Convert JSON response to Python list

        for game in games:                         # Loop over each game in the list
            name = clean_name(game.get("name", "unknown"))          # Get game name
            game_code = str(game.get("game_code", "0000"))          # Get game code
            category = clean_name(game.get("category", "uncategorized"))  # Get game category
            image_url = game.get("image_square")                   # Get image URL

            if not image_url:                        # Skip games with no image
                print(f"[!] Skipping {name}, no image URL")
                continue

            folder_path = Path(category)             # Create folder path based on category
            folder_path.mkdir(parents=True, exist_ok=True)  # Create folder if not exists

            image_name = f"{name}_{game_code}.jpg"   # Create image file name
            image_path = folder_path / image_name    # Create full image path

            download_image(image_url, image_path)    # Download and save image

    except requests.RequestException as e:
        print(f"[!] Failed to fetch game data: {e}")  # Handle API errors

# Run main function when this script is run directly
if __name__ == "__main__":
    main()
