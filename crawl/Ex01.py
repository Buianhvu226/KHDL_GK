import requests
from bs4 import BeautifulSoup

# Hàm để crawl dữ liệu từ một trang
def crawl_page(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    hotels = []
    for hotel_element in soup.find_all('div', class_='hotel-info'):
        hotel_name_element = hotel_element.find('span', class_='name')
        if hotel_name_element:
            hotel_name = hotel_name_element.text.strip()
        else:
            hotel_name = 'Không tìm thấy tên'

        price_element = hotel_element.find('span', class_='not-break')
        if price_element:
            price = price_element.text.strip().replace('₫', '')
        else:
            price = 'Liên hệ'

        hotels.append({
            'name': hotel_name,
            'price': price,
        })
    
    return hotels

# Hàm để crawl dữ liệu từ nhiều trang
def crawl_multiple_pages(base_url, num_pages):
    all_hotels = []
    for page_num in range(1, num_pages + 1):
        url = f'{base_url}&pageno={page_num}'
        hotels_on_page = crawl_page(url)
        all_hotels.extend(hotels_on_page)
    return all_hotels

# Cấu hình URL và tham số
base_url = 'https://www.trip.com/hotels/list?city=1356'
num_pages_to_crawl = 5  # Số trang bạn muốn crawl

# Crawl dữ liệu từ nhiều trang
all_hotels = crawl_multiple_pages(base_url, num_pages_to_crawl)

# In thông tin khách sạn
if all_hotels:
    i = 0
    for hotel in all_hotels:
        print(f"Tên khách sạn: {hotel['name']}")
        print(f"Giá phòng: {hotel['price']}")
        print('---')
        i += 1
        print(f"Đã tìm thấy {i} khách sạn.")
else:
    print("Không tìm thấy khách sạn nào.")
