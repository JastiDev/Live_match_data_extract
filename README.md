# Live Match Data Scraper

## Project Overview

The Live Match Data Scraper is a sophisticated Python-based application designed to extract real-time match data from betting websites. Built with a focus on reliability and user experience, this tool combines modern web scraping techniques with a user-friendly graphical interface, making it accessible to both technical and non-technical users.

### Purpose

This application serves several key purposes:

- Automated collection of live sports betting data
- Real-time monitoring of match odds and market movements
- Systematic data extraction for sports analytics
- Efficient storage of betting market information in structured JSON format

### Technical Architecture

The project is built on three main components:

1. **Web Scraping Engine**:

   - Utilizes Selenium WebDriver for dynamic content interaction
   - Implements undetected-chromedriver for bot detection bypass
   - Handles Cloudflare protection and other security measures
   - Manages browser sessions and page navigation

2. **Data Processing Layer**:

   - Extracts structured data from HTML elements
   - Processes odds and betting information
   - Handles multiple market types and betting formats
   - Implements error handling and data validation

3. **Graphical User Interface**:
   - Built with tkinter for cross-platform compatibility
   - Features a modern, intuitive design
   - Provides real-time logging and status updates
   - Includes customizable save location functionality

### Key Features

- **Advanced Web Scraping**:

  - Automated navigation through betting platforms
  - Real-time data extraction from live matches
  - Support for multiple sports and competitions
  - Robust error handling and recovery mechanisms

- **Comprehensive Data Collection**:

  - Team and competition information
  - Live match odds (back/lay)
  - Detailed market data
  - Minimum and maximum bet limits
  - Stake information

- **User-Friendly Interface**:

  - Simple configuration options
  - Real-time progress monitoring
  - Customizable save locations
  - Headless mode support

- **Data Management**:
  - Structured JSON output
  - Organized file naming
  - Customizable save locations
  - Efficient data storage format

### Implementation Details

The scraper employs several sophisticated techniques:

1. **Browser Automation**:

   - Chrome WebDriver integration
   - Headless browsing capability
   - Automated page navigation
   - Dynamic content handling

2. **Data Extraction**:

   - CSS selector-based element location
   - Dynamic wait mechanisms
   - Structured data parsing
   - Error-resistant extraction methods

3. **Security Features**:

   - Bot detection bypass mechanisms
   - Cloudflare protection handling
   - Session management
   - Secure login handling

4. **Error Handling**:
   - Comprehensive exception management
   - Automatic recovery mechanisms
   - Detailed error logging
   - User-friendly error messages

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
