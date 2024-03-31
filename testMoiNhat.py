from playwright.sync_api import sync_playwright
import pandas as pd
import re

def main():
    with sync_playwright() as p:
        # IMPORTANT: Change dates to future dates, otherwise it won't work
        checkin_date = '2024-06-20'
        checkout_date = '2024-06-21'
        
        page_url = f'https://www.trivago.vn/vi/lm/kh%C3%A1ch-s%E1%BA%A1n-%C4%90%C3%A0-n%E1%BA%B5ng-vi%E1%BB%87t-nam?search=200-68104;dr-20240405-20240406;pr-101-52338;rc-1-3'

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout=600000)  # Increase timeout duration
                    
        # Initialize variables
        num_scrolls = 200
        unique_hotels = set()
        all_hotels = []
        current_page = 1

        # Scroll the page to load all hotels
        # for _ in range(num_scrolls):
        #     page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        #     # Wait for a short duration for new content to load
        #     page.wait_for_timeout(1000)  # 1 second

        while current_page <= 15:  # Stop at page 15
            # Extract hotel data
            hotels = page.locator('//li[@data-testid="accommodation-list-element"]').all()
            print(f'There are: {len(hotels)} hotels.')

            hotels_list = []
            for hotel in hotels:
                hotel_dict = {}
                hotel_name = hotel.locator('//span[@class="name"]').first
                try:
                    hotel_dict['hotel'] = hotel.locator('//button[@data-testid="item-name"]').inner_text()  # Increase timeout duration
                    hotel_dict['price'] = hotel.locator('//span[@data-testid="recommended-price"]').nth(0).inner_text()
                    # hotel_dict['score'] = hotel.locator('//button[@data-testid="rating-section"]').inner_text()

                    rating_section_text = hotel.locator('//button[@data-testid="rating-section"]').inner_text()
                    score_match = re.search(r'(\d+\.\d+)', rating_section_text)
                    if score_match:
                        score = score_match.group(1)
                    else:
                        score = "N/A"
                    hotel_dict['score'] = score

                    hotel_dict['location'] = hotel.locator('//button[@data-testid="distance-label-section"]').inner_text()

                    review_count_match = re.search(r'\((\d+) nhận xét\)', rating_section_text)
                    if review_count_match:
                        review_count = review_count_match.group(1)
                    else:
                        review_count = "N/A"
                    hotel_dict['review counts'] = review_count

                except Exception as e:
                    print(f"Timeout occurred while extracting inner text: {e}")
                    hotel_dict['hotel'] = "N/A"
                hotels_list.append(hotel_dict)
            
            all_hotels.extend(hotels_list)

            # Click on the next page button
            try:
                page.click(f'//button[@data-testid="result-page-{current_page + 1}"]')
                print("Clicked on the next page button.")
                current_page += 1
            except Exception as e:
                print(f"Error occurred while clicking on the next page button: {e}")
                break  # Exit loop if unable to click on next page
        
        df = pd.DataFrame(all_hotels)
        df.to_excel('hotels_lists.xlsx', index=False) 
        df.to_csv('hotels_lists.csv', index=False) 
        
        browser.close()
            
if __name__ == '__main__':
    main()
