import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from tempfile import mkdtemp
import time
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service

# Load environment variables
load_dotenv()


class UserImporter:
    def __init__(self):
        # Initialize WebDriver (assuming Chrome)
        options = webdriver.ChromeOptions()
        chrome_binary_path = os.getenv("CHROME_BINARY_PATH")
        webdriver_path = os.getenv("CHROME_DRIVER_PATH")
        print(f"Chrome Binary Path: {chrome_binary_path}")
        print(f"Chrome Driver Path: {webdriver_path}")
        options = webdriver.ChromeOptions()
        options.binary_location = chrome_binary_path
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--incognito")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--enable-javascript")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9222")
        self.driver = webdriver.Chrome(
            service=Service(executable_path=webdriver_path), options=options
        )  # Replace with your ChromeDriver path

    def wp_login(
        self,
        base_site_url: str = "https://multisite.com",
        username: str = "myusername",
        password: str = "mypassword",
    ):
        print(f"Attempting to login to {base_site_url}/wp-login.php as {username}...")
        self.driver.get(f"{base_site_url}/wp-login.php")
        self.driver.find_element(By.ID, "user_login").send_keys(username)
        self.driver.find_element(By.ID, "user_pass").send_keys(password)
        self.driver.find_element(By.ID, "wp-submit").click()

    def import_users(
        self,
        base_site_url: str = "https://multisite.com",
        subsite_path: str = "mysite",
        user_file: str = "./users.csv",
    ):
        # remove null bytes from file
        clean_file_path = "cleaned-user-export.csv"
        fi = open(user_file, "rb")
        data = fi.read()
        fi.close()
        fo = open(clean_file_path, "wb")
        fo.write(data.replace(b"\x00", b""))
        fo.close()
        with open(clean_file_path, "r") as csvfile:
            dictreader = csv.DictReader(csvfile, delimiter=",")
            # Navigate to Add New User page
            self.driver.get(f"{base_site_url}/{subsite_path}/wp-admin/user-new.php")
            time.sleep(3)
            for row in dictreader:
                user_email = row["user_email"]
                user_role = row["role"]
                print(f"Adding user {user_email} with role {user_role}")
                # Fill in user details
                self.driver.find_element(By.ID, "adduser-email").send_keys(
                    row["user_email"]
                )
                select_role = self.driver.find_element(By.ID, "adduser-role")
                select_role.click()
                all_options = select_role.find_elements(By.TAG_NAME, "option")
                for option in all_options:
                    if option.get_attribute("value") == user_role:
                        option.click()
                        break
                time.sleep(0.25)
                self.driver.find_element(By.ID, "adduser-noconfirmation").click()
                time.sleep(0.25)
                # Click the Add New User button
                self.driver.find_element(By.ID, "addusersub").click()

                # Wait for the user creation to complete
                time.sleep(1.5)

        print("All users added! Closing driver")
        self.driver.quit()


def main():
    load_dotenv()

    importer = UserImporter()
    importer.wp_login(
        base_site_url=os.getenv("WP_MULTISITE_BASE_URL"),
        username=os.getenv("WP_ADMIN_USERNAME"),
        password=os.getenv("WP_ADMIN_PASSWORD"),
    )
    time.sleep(1.5)

    importer.import_users(
        base_site_url=os.getenv("WP_MULTISITE_BASE_URL"),
        subsite_path=os.getenv("WP_SUBSITE_PATH"),
        user_file=os.getenv("USER_CSV_PATH"),
    )
    print("Done!")


if __name__ == "__main__":
    main()
