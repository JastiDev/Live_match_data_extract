# Live Match Data Scraper

A Python application with a graphical user interface for scraping live match data from betting websites. The application features headless mode support, customizable save locations, and comprehensive match data extraction.

## Features

- Modern graphical user interface
- Headless mode for background operation
- Customizable save location for JSON data
- Comprehensive match data extraction including:
  - Team names
  - Competition names
  - Match odds
  - Detailed market information
- Automatic JSON file generation
- Real-time logging
- Cloudflare detection bypass capabilities

## Requirements

- Python 3.8 or higher
- Google Chrome browser
- Windows/Linux/MacOS

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd Live_match_data_extract
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:

```bash
python scraper_ui.py
```

2. Configure the scraping parameters:

   - Website URL
   - Username
   - Password
   - Sport Name
   - Save Location
   - Headless Mode (optional)

3. Click "Start Scraping" to begin the data collection process

4. Monitor progress in the log window

## Output Format

The scraped data is saved in JSON format with the following structure:

```json
{
    "name": "Team Names",
    "competition": "Competition Name",
    "url": "Match URL",
    "main_odds": [
        [back_odds, lay_odds],
        ...
    ],
    "markets": [
        {
            "title": "Market Title",
            "rows": [
                {
                    "name": "Selection Name",
                    "odds": [
                        {
                            "type": "back/lay",
                            "odds": "odds_value",
                            "stake": "stake_value"
                        }
                    ],
                    "min_bet": "minimum_bet",
                    "max_bet": "maximum_bet"
                }
            ]
        }
    ]
}
```

## Troubleshooting

1. **Cloudflare Detection**:

   - If running in non-headless mode, you may need to complete manual verification
   - Wait for the verification prompt and follow the instructions

2. **ChromeDriver Issues**:

   - Ensure Google Chrome is installed
   - The application will automatically download the correct ChromeDriver version

3. **UI Issues**:
   - Make sure tkinter is properly installed with your Python distribution
   - On Linux, you might need to install python3-tk package

## Notes

- The application uses undetected-chromedriver to bypass bot detection
- Headless mode may not work with some websites due to anti-bot measures
- Always ensure you have permission to scrape data from the target website

## License

This project is licensed under the MIT License - see the LICENSE file for details
