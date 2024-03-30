import requests
from bs4 import BeautifulSoup

# Cấu hình URL và tham số
url = 'https://www.trip.com/hotels/da-nang-hotels-list-1356/?locale=en_xx&curr=vnd&allianceid=14894&sid=17852204&ppcid=ckid-5079584290_adid-82395018810470_akid-kwd-82395675608524:loc-166_adgid-1318316090541621&utm_source=bing&utm_medium=cpc&utm_campaign=686900320&msclkid=fdad9ce69d5e1dc76d05fae153f00886'


# Gửi yêu cầu và lấy dữ liệu HTML
response = requests.get(url)
html_content = response.text  # Get the HTML content as a string

# Tạo BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Khởi tạo danh sách khách sạn trống
hotels = []

# Duyệt qua các thẻ chứa thông tin khách sạn (cân nhắc thay đổi)
hotel_name_elements = soup.find_all('div', class_='sc-jrAGrp sc-kEjbxe eDlaBj dscgss')
# Lặp qua từng phần tử trong danh sách tên khách sạn
for hotel_name_element in hotel_name_elements:
    # Lấy tên khách sạn từ phần tử hiện tại
    hotel_name = hotel_name_element.text.strip()
    # Thêm tên khách sạn vào danh sách
    hotels.append({
        'name': hotel_name
    })

# In thông tin khách sạn
if hotels:
    for hotel in hotels:
        print(f"Tên khách sạn: {hotel['name']}")
        print('---')
else:
    print("Không tìm thấy khách sạn nào.")
