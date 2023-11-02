# WP Multisite User Importer

This script was written to handle a very specific problem, and I figured others may need to solve the same problem at some point.

## The Problem

I'm building out a WP Multisite. I want to add all users from one of the sites to another site with the exact same roles. In my case, this is because the two sites in the multisite are different "versions" of the same site, as a byproduct of a website redesign.

Unfortunately, WP offers no inherent bulk user addition feature within a given site on the network. I did install the [Import and export users and customers](https://wordpress.org/plugins/import-users-from-csv-with-meta/) plugin, hoping I could simply export the users from site A and import them into site B. This plugin failed to do this, however, since that plugin assumes that the users being imported into the Wordpress site do not already exist as WP users. In the case of the Multisite, where we are "assigning" EXISTING users to site B, that plugin does not work.

I thought about writing some simple JS to just paste into the console on the add user page in order to loop over a list of user emails and roles and add them as existing users (ensuring to also check the "skip email notification" checkbox). However, adding a user triggers a page refresh, which means iterative logic in the console would not have worked.

## Solution

Generally speaking, when that page refresh issue pops up and prevents JS automation, Selenium with Python is my go-to solution. So, that's what this project is. A Selenium-driven script configurable with [environment variables](.env.sample) that will:

1. auto-open a browser,
2. log in to your multisite admin dashboard,
3. open the Add User page on the **specific site on your network** to which you are attempting to add **existing users ("existing" is key)**,
4. iterate over a CSV file you specify containing the fields `user_email,role`, and add each of those users to the site with the specified roles without sending email notifications

## Running it

1. You will need to download executables for the Selenium webdriver to work. You need a `chromedriver` and a `chrome` executable. You can download them from here:
   [https://googlechromelabs.github.io/chrome-for-testing/](https://googlechromelabs.github.io/chrome-for-testing/). Be sure to update your `CHROME_BINARY_PATH` and `CHROME_DRIVER_PATH` environment variables to point at the paths to your `chrome.exe` and `chromedriver.exe` files, respectively.
2. Clone the repo (`git clone https://github.com/austinjhunt/wp-multisite-existing-user-importer.git`)
3. CD into the repo (`cd wp-multisite-existing-user-importer`)
4. Optionally create a Python virtual environment: `python3.x -m venv venv && source venv/Scripts/activate`
5. Install Python requirements (`pip install -r requirements.txt`)
6. Copy [.env.sample](.env.sample) to your own file called `.env`, and change the values to match your own environment.
7. Run the script: `python add-users.py`
