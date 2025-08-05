from amazon import get_amazon_price
from gsheets import connect_sheet
from emailalert import send_alert
from datetime import datetime

def main():
    url = 'https://www.amazon.eg/dp/B0DGJBY734'
    sheet_name = 'Product Tracker'
    email = 'recipient@gmail.com'

    print("Fetching price data...")
    price_data = get_amazon_price(url)
    print(f"Price data: {price_data}")
    
    print("Connecting to sheet...")
    sheet = connect_sheet(sheet_name)
    print("Connected successfully!")

    if not price_data['price']:
        send_alert(email, 'Price Alert', 'Price data not available or failed to retrieve.')
        return

    # قراءة آخر سعر محفوظ في الشيت
    rows = sheet.get_all_values()
    is_first_run = len(rows) == 0  # Empty sheet
    
    # إضافة headers في أول مرة
    if is_first_run:
        sheet.append_row(['Date', 'Product', 'Price', 'URL'])
        print("Headers added to sheet.")
        last_price = None
    elif len(rows) > 1:
        last_row = rows[-1]
        try:
            last_price = float(last_row[2])
        except:
            last_price = None
    else:
        last_price = None

    # السعر الحالي
    current_price = price_data['price']

    # مقارنة السعر وإضافة إذا تغيّر
    if last_price is None or current_price != last_price:
        today = datetime.now().strftime("%Y-%m-%d %H:%M")
        sheet.append_row([today, price_data['title'], current_price, url])
        
        if is_first_run:
            send_alert(email, 'Price Tracker Started!', f"Started tracking: {price_data['title']}\nInitial price: {current_price} EGP")
            print("First run! Initial price logged and email sent.")
        else:
            send_alert(email, 'Price Change Detected!', f"New price: {current_price} EGP\nProduct: {price_data['title']}")
            print("Price changed! Logged and email sent.")
    else:
        print("Price is the same. No action taken.")

if __name__ == "__main__":
    main()
