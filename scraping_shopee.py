import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import subprocess
import bs4
import pandas as pd
import tkinter as tk
from tkinter import messagebox

def start_scraping():
    # Get search keyword from the GUI input field
    key_search = search_entry.get()

    # Start the Chrome browser with remote debugging enabled
    subprocess.Popen([
        "google-chrome",
        "--remote-debugging-port=9222",
    ])
    
    time.sleep(2)

    # Set up ChromeOptions for remote debugging
    options = webdriver.ChromeOptions()
    options.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(options=options)

    # Open Shopee's website
    driver.get("https://shopee.co.th/")

    time.sleep(2)
    
    # Perform the search
    search_box = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/header/div[2]/div/div[1]/form/div/div/input')
    search_box.send_keys(key_search)
    search_box.send_keys(Keys.RETURN)

    time.sleep(1)
    driver.execute_script("document.body.style.zoom='10%'")  # Adjust zoom to load all items

    time.sleep(2)

    # Get the page source and parse with BeautifulSoup
    data = driver.page_source
    soup = bs4.BeautifulSoup(data, "html.parser")

    products = soup.find_all("div", {'class': 'line-clamp-2 break-words min-w-0 min-h-[2.5rem] text-sm'})
    product_list = [product.text.strip() for product in products]


    prices = soup.find_all("span", {'class': 'font-medium text-base/5 truncate'})
    prices_list = [price.text.strip() for price in prices]


    total_sold = soup.find_all("div", {'class': 'truncate text-shopee-black87 text-xs min-h-4'})
    total_sold_list = [total.text.strip() for total in total_sold]

    # Check if the lists have the same length, and fill missing data with None or N/A
    max_length = max(len(product_list), len(prices_list), len(total_sold_list))

    # Fill shorter lists with None (or a placeholder like "N/A")
    while len(product_list) < max_length:
        product_list.append("N/A")
    while len(prices_list) < max_length:
        prices_list.append("N/A")
    while len(total_sold_list) < max_length:
        total_sold_list.append("N/A")
    
    # Create DataFrame
    df = pd.DataFrame({
        "Product": product_list,
        "Price": prices_list,
        "Total Sold": total_sold_list
    })

    # Save the results to an Excel file
    df.to_excel(f"{key_search}_shopee.xlsx", index=False)

    # Show a message box when the scraping is done
    messagebox.showinfo("Success", f"Scraping completed. Data saved as {key_search}_shopee.xlsx")

    # Close the tkinter window
    root.quit()
    driver.close()

# Set up the tkinter GUI
root = tk.Tk()
root.title("Shopee Scraping Tool")

# Set up the GUI layout
tk.Label(root, text="Enter search keyword:").pack(pady=10)
search_entry = tk.Entry(root, width=40)
search_entry.pack(pady=10)

start_button = tk.Button(root, text="Start Scraping", command=start_scraping)
start_button.pack(pady=20)

# Start the tkinter event loop
root.mainloop()
