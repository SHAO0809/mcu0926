import requests  # 請求工具
from bs4 import BeautifulSoup  # 解析工具
import time  # 用來暫停程式

# 要爬的股票
stock = ["1101", "2330", "1102"]

for stockid in stock:  # 迴圈依序爬股價
    url = "https://tw.stock.yahoo.com/quote/" + stockid + ".TW"
    r = requests.get(url)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        price_element = soup.find('span', class_=[
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)",
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)",
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)"
        ])
        
        if price_element:
            price = price_element.getText()
            message = f"股票 {stockid} 即時股價為 {price}"

            # 使用 Telegram Bot 回報股價
            token = "你的_token"
            chat_id = "你的_chat_id"
            url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
            response = requests.get(url)
            if response.status_code != 200:
                print(f"發送訊息失敗，狀態碼：{response.status_code}")
        else:
            print(f"無法找到股票 {stockid} 的價格")
    else:
        print(f"請求股票 {stockid} 失敗，狀態碼：{r.status_code}")

    time.sleep(3)
