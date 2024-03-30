from bs4 import BeautifulSoup
import requests

# URL trang Agoda cần crawl
url = "https://www.agoda.com/pages/agoda/default/DestinationSearchResult.aspx?city=16440&site_id=1759953&tag=254fead1-05c8-6c79-f224-13778875f949&msclkid=d80fe8d160a41336715e8ed6dd1e7404&ds=UzQJUl7V0AQBcyik"

# Gửi yêu cầu GET đến URL
response = requests.get(url)

# Kiểm tra trạng thái trả về
if response.status_code == 200:
    # Parse nội dung HTML
    soup = BeautifulSoup(response.content, "html.parser")

    # Tìm thẻ chứa thông tin khách sạn
    hotels = soup.find_all("ol", class_="hotel-list-container")

    # Duyệt qua từng khách sạn
    for hotel in hotels:
        # Tên khách sạn
        hotel_name = hotel.find("h3", class_="sc-jrAGrp sc-kEjbxe eDlaBj dscgss").text.strip()

        # Giá phòng
        hotel_price = hotel.find("span", class_="price-tag").text.strip()

        # Đánh giá
        hotel_rating = hotel.find("span", class_="rating-score").text.strip()

        # Số lượng đánh giá
        hotel_reviews = hotel.find("span", class_="reviews-count").text.strip()

        # In thông tin
        print(f"Tên khách sạn: {hotel_name}")
        print(f"Giá phòng: {hotel_price}")
        print(f"Đánh giá: {hotel_rating}")
        print(f"Số lượng đánh giá: {hotel_reviews}")
        print("-----------------")
else:
    print("Lỗi khi truy cập trang web")
