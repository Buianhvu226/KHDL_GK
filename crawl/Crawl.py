from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Khởi tạo trình duyệt Chrome
driver = webdriver.Chrome()

# Cấu hình URL cần crawl
url = 'https://www.trip.com/hotels/list?city=1356'

# Mở URL trong trình duyệt
driver.get(url)

# Số lần cuộn trang
num_scrolls = 110

# Tạo một set để lưu trữ các khách sạn đã thu thập
unique_hotels = set()

# Thu thập dữ liệu sau mỗi lần cuộn
all_hotels = []
for _ in range(num_scrolls):
    # Cuộn trang xuống cuối
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Đợi một khoảng thời gian để dữ liệu mới tải xuống
    time.sleep(1)
    # Lấy nội dung HTML của trang sau khi cuộn
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    # Thu thập dữ liệu từ trang hiện tại
    hotels_on_page = []
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

        # Kiểm tra xem khách sạn đã tồn tại trong set chưa
        if hotel_name not in unique_hotels:
            hotels_on_page.append({
                'name': hotel_name,
                'price': price,
            })
            # Thêm khách sạn vào set
            unique_hotels.add(hotel_name)
    all_hotels.extend(hotels_on_page)

# Đóng trình duyệt sau khi hoàn thành
driver.quit()

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
