import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize Chrome driver
driver = webdriver.Chrome()

# Initialize counter for the number of vehicle details retrieved and create a CSV file
count = 0
csv_file = 'vehicle_details.csv'

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['VIN', 'Make', 'Model', 'Year', 'Trim', 'Drive Train', 'Engine'])  # Write headers

    while count < 1:
        try:
            driver.get('https://randomvin.com/')
            time.sleep(2)

            e = driver.find_element(By.TAG_NAME, 'h2')
            vin = e.text

            # Open a new tab and switch to it
            driver.execute_script("window.open('https://driving-tests.org/vin-decoder/');")
            driver.switch_to.window(driver.window_handles[1])

            time.sleep(3)
            vin_input = driver.find_element(By.ID, "vin_input")
            vin_input.send_keys(vin)

            search_button = driver.find_element(By.XPATH, '/html/body/div[1]/section[1]/div/form/input[2]')
            search_button.click()
            time.sleep(5)

            # Check if vehicle details are present on the page
            if driver.find_elements(By.CLASS_NAME, "panel-content"):
                make = driver.find_element(By.ID, "nhtsa-26").text
                model = driver.find_element(By.ID, "nhtsa-28").text
                year = driver.find_element(By.ID, "nhtsa-29").text
                trim = driver.find_element(By.ID, "nhtsa-96").text
                drive = driver.find_element(By.ID, "nhtsa-15").text
                engine = driver.find_element(By.ID, "nhtsa-13").text

                # Write retrieved vehicle details to the CSV file
                writer.writerow([vin, make, model, year, trim, drive, engine])

                # Increment the counter for successful retrieval
                count += 1
                print(f"Total count of vehicle details retrieved: {count}")
                print(f"Vehicle details have been saved in '{csv_file}'.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        finally:
            driver.close()  # Close the tab
            driver.switch_to.window(driver.window_handles[0])  # Switch back to the first tab

print(f"Total count of vehicle details retrieved: {count}")
print(f"Vehicle details have been saved in '{csv_file}'.")
