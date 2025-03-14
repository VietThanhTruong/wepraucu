from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

# Cấu hình options để chạy trình duyệt không cần GUI
options = Options()
# options.headless = True  # Chạy không có giao diện

# Tạo một instance của ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

connection = mysql.connector.connect(host='localhost',
                                         database='baitap1',
                                         user='root',
                                         password='')

# Mở trang web
url = "https://organicmart.com.vn/rau-cu-qua-huu-co"
driver.get(url)

# Chờ một chút để trang tải xong
time.sleep(3)

# Lấy danh sách các sản phẩm
products = driver.find_elements(By.CSS_SELECTOR, ".product-box")

# Lặp qua từng sản phẩm và lấy tên và giá bán
product_data = []

for product in products:
    try:
        # Lấy tên sản phẩm
        name = product.find_element(By.CSS_SELECTOR, ".product-name").text
        
        # Lấy giá bán
        price = product.find_element(By.CSS_SELECTOR, ".price.product-price").text
        
        # Thêm vào danh sách kết quả
        product_data.append({
            "name": name,
            "price": price
        })
    except Exception as e:
        print(f"Error extracting data: {e}")

# In ra kết quả
for item in product_data:
    print(f"Tên: {item['name']}, Giá: {item['price']}")
    
    mySql_insert_query = """INSERT INTO weprausach ( name, price) 
                            VALUES 
                            (%s, %s) """

    insert_tuple_ = (item['name'], item['price'])

    cursor = connection.cursor()
    cursor.execute(mySql_insert_query, insert_tuple_)

    connection.commit()
    print(cursor.rowcount, "Record inserted successfully into Laptop table")

# Đóng trình duyệt
driver.quit()
