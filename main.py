import json
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class LiveMatchScraper:
    def __init__(self, url, headless=True):
        self.driver = None
        self.wait_time = 10
        self.base_url = url
        self.headless = headless
        
    def initialize_driver(self):
        """Initialize Chrome WebDriver with options"""
        options = webdriver.ChromeOptions()
        
        if self.headless:
            options.add_argument("--headless")
            
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=options)
        # self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.get(self.base_url)
        
    def manual_bot_detection_bypass(self):
        """Wait for manual Cloudflare check completion"""
        print("Please complete the Cloudflare verification manually...")
        input("Press Enter when you've completed the verification...")
        
    def login(self, username, password):
        """Login to the website with provided credentials"""
        try:            

            # Wait for login elements to be present
            username_field = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Enter Username']"))
            )
            password_field = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Enter Password']")
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button.btn-primary")
            
            # Enter credentials and click login
            username_field.send_keys(username)
            password_field.send_keys(password)
            login_button.click()
            
            # Wait for login to complete
            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.ID, "home_sports_list")))
            print("Login successful!")
            
        except Exception as e:
            print(f"Login failed: {str(e)}")
            raise
            
    def select_sport(self, sport_name):
        """Select sport from the sports list"""
        try:
            pyautogui.press('esc')
            time.sleep(5)
            pyautogui.press('esc')

            sport_element = WebDriverWait(self.driver, self.wait_time).until(
                EC.element_to_be_clickable((
                    By.XPATH, 
                    f"//ul[@id='home_sports_list']//span[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{sport_name.lower()}')]"
                ))
            )
            sport_element.click()
            print(f"Selected sport: {sport_name}")
            
            # Wait for matches to load
            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.bet-table-box"))
            )
            
        except Exception as e:
            print(f"Failed to select sport {sport_name}: {str(e)}")
            raise
            
    def get_live_matches(self):
                    
        try:
            matches = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_all_elements_located((
                    By.XPATH,
                    '//div[contains(@class, "bet-table-box")]'
                    '[.//div[contains(@class, "inplay") and contains(., "Live")]]'
                ))
            )
            
            print("Found", len(matches), "live matches")
            match_data = []
            
            for i, match in enumerate(matches, 1):
                try:
                    # First find the bet-table-row that contains the game info
                    row = match.find_element(By.CSS_SELECTOR, '.bet-table-row')
                    
                    # Get structured odds with positions
                    structured_odds = []
                    point_titles = row.find_elements(By.CSS_SELECTOR, '.point-title')
                    has_valid_odds = False
                    
                    for point in point_titles:
                        # Get both back and lay odds for this position
                        odds_elements = point.find_elements(By.CSS_SELECTOR, '.bl-box .odds')
                        position_odds = []
                        
                        for odds_el in odds_elements:
                            odds_text = odds_el.text.strip()
                            if odds_text and odds_text != "—" and odds_text.replace('.', '').isdigit():
                                position_odds.append(float(odds_text))
                                has_valid_odds = True
                            else:
                                position_odds.append("-")
                        
                        # If no odds found for this position, add "-"
                        if not position_odds:
                            position_odds = ["-", "-"]  # For both back and lay
                        elif len(position_odds) == 1:
                            position_odds.append("-")  # If only one odds found
                            
                        structured_odds.append(position_odds)
                    
                    # Only process matches that have at least one valid odds
                    if has_valid_odds:
                        # Find game-name div inside the row
                        game_div = row.find_element(By.CSS_SELECTOR, '.game-title .game-name')
                        
                        # Get team name - first p element
                        team_name = game_div.find_element(By.CSS_SELECTOR, 'p.team-name.text-left:not(.team-event)').text.strip()
                        print(f"Found team name: {team_name}")
                        
                        # Get event name - second p element with team-event class
                        event_name = game_div.find_element(By.CSS_SELECTOR, 'p.team-name.text-left.team-event').text.strip(' ()').strip()
                        print(f"Found event: {event_name}")
                        
                        # Get match link
                        link = game_div.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                        
                        match_info = {
                            'name': team_name,
                            'competition': event_name,
                            'url': link,
                            'odds': structured_odds
                        }
                        print(f"Match info with structured odds: {match_info}")
                        match_data.append(match_info)
                    else:
                        print(f"Skipping match {i} - no valid odds found")
                    
                except Exception as e:
                    print(f"Error analyzing match {i}: {str(e)}")
                    continue
            
            print(f"\nFinal match data ({len(match_data)} matches with odds):")
            print(match_data)
                    
            return match_data
            
        except Exception as e:
            print(f"Failed to find live matches: {str(e)}")
            return []
            
    def click_match(self, match_element):
        """Click on a match element to view details"""
        try:
            match_element.click()
            # Wait for match details to load
            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".market-4, .market-6, .market-9"))
            )
            return True
        except Exception as e:
            print(f"Failed to click match: {str(e)}")
            return False
            
    def scrape_match_details(self):
        """Scrape all betting markets for the current match"""
        try:
            # Wait for bet-table to load
            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'bet-table'))
            )
            
            markets_data = []
            # Find all bet-table elements
            bet_tables = self.driver.find_elements(By.CLASS_NAME, 'bet-table')
            
            for table in bet_tables:
                try:
                    # Get market title from the header
                    try:
                        header = table.find_element(By.CLASS_NAME, 'bet-table-header')
                        title = header.text.strip()
                    except:
                        title = "Unknown Market"
                    
                    market_data = {
                        'title': title,
                        'rows': []
                    }
                    
                    # Get all active rows in this table
                    rows = table.find_elements(By.CSS_SELECTOR, '.bet-table-row:not(.suspended)')
                    for row in rows:
                        try:
                            # Get selection name
                            try:
                                name_element = row.find_element(By.CSS_SELECTOR, '.nation-name')
                                name = name_element.text.strip()
                            except:
                                name = "Unknown Selection"
                            
                            # Get back and lay odds
                            odds_data = []
                            odds_boxes = row.find_elements(By.CSS_SELECTOR, '.bl-box')
                            for box in odds_boxes:
                                try:
                                    odds_element = box.find_element(By.CSS_SELECTOR, '.odds')
                                    odds = odds_element.text.strip()
                                    
                                    stake_element = box.find_element(By.CSS_SELECTOR, '.d-block:not(.odds)')
                                    stake = stake_element.text.strip()
                                    
                                    box_type = 'back' if 'back' in box.get_attribute('class') else 'lay'
                                    
                                    if odds and odds != "—":
                                        odds_data.append({
                                            'type': box_type,
                                            'odds': float(odds) if odds.replace('.', '').isdigit() else "-",
                                            'stake': stake
                                        })
                                    else:
                                        odds_data.append({
                                            'type': box_type,
                                            'odds': "-",
                                            'stake': "-"
                                        })
                                except:
                                    continue
                            
                            # Get min/max if available
                            try:
                                min_max = row.find_element(By.CSS_SELECTOR, '.fancy-min-max').text
                                min_bet = min_max.split('Min:')[1].split('Max:')[0].strip()
                                max_bet = min_max.split('Max:')[1].strip()
                            except:
                                min_bet = "-"
                                max_bet = "-"
                            
                            row_data = {
                                'name': name,
                                'odds': odds_data,
                                'min_bet': min_bet,
                                'max_bet': max_bet
                            }
                            
                            market_data['rows'].append(row_data)
                            
                        except Exception as e:
                            print(f"Error parsing row: {str(e)}")
                            continue
                    
                    # Only add markets that have data
                    if market_data['rows']:
                        markets_data.append(market_data)
                    
                except Exception as e:
                    print(f"Error parsing bet table: {str(e)}")
                    continue
            
            return markets_data
            
        except Exception as e:
            print(f"Error scraping match details: {str(e)}")
            return None
            
    def scrape_all_live_matches(self, sport_name):
        """Main function to scrape all live matches for a given sport"""
        try:
            self.initialize_driver()
            
            if not self.headless:
                self.manual_bot_detection_bypass()
            else:
                print("Running in headless mode - attempting automatic navigation...")
                
            self.driver.get(self.base_url)
            self.login("Demo258", "Asdf@1122")
            self.select_sport(sport_name)
            
            live_matches = self.get_live_matches()
            if not live_matches:
                print("No live matches found")
                return []
                
            all_matches_data = []
            
            for i, match in enumerate(live_matches):
                print(f"Processing match {i+1}/{len(live_matches)}")
                
                try:
                    # Navigate to match details using the URL
                    self.driver.get(match['url'])
                    
                    # Wait for the page to load
                    WebDriverWait(self.driver, self.wait_time).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[class^="market-"]'))
                    )
                    
                    match_details = self.scrape_match_details()
                    if match_details:
                        # Combine basic match info with detailed market data
                        full_match_data = {
                            'name': match['name'],
                            'competition': match['competition'],
                            'url': match['url'],
                            'main_odds': match['odds'],
                            'markets': match_details
                        }
                        all_matches_data.append(full_match_data)
                        print(f"Successfully scraped details for match {i+1}")
                    
                    # Go back to matches list
                    self.driver.get(self.base_url)
                    self.select_sport(sport_name)  # Reselect sport to get back to matches list
                    
                except Exception as e:
                    print(f"Error processing match {i+1}: {str(e)}")
                    # Try to recover by going back to matches list
                    self.driver.get(self.base_url)
                    self.select_sport(sport_name)
                    continue
            
            return all_matches_data
            
        except Exception as e:
            print(f"Error in main scraping process: {e}")
            return None
        finally:
            if self.driver:
                self.driver.quit()
                
    def save_to_json(self, data, filename):
        """Save scraped data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {filename}")

# Example usage
if __name__ == "__main__":
    target_url = "https://taj777.now"
    scraper = LiveMatchScraper(url=target_url)
    sport_name = "cricket"  # Change to your desired sport
    live_data = scraper.scrape_all_live_matches(sport_name)
    
    if live_data:
        scraper.save_to_json(live_data, f"live_{sport_name.lower()}_data.json")
    else:
        print("No data was scraped")