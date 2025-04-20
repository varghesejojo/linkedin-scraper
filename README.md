# LinkedIn Scraper

This project is a LinkedIn connection scraper built with Python. It logs into a LinkedIn account, navigates through the connections page, and saves the connection data to a JSON file.

> ⚠️ This tool is for educational purposes only. Automating interactions with LinkedIn may violate their terms of service.

---

## 🚀 Features

- Logs into LinkedIn using Selenium
- Navigates and scrolls through all your connections
- Scrapes full names, profile URLs, and other connection details
- Saves data in `linkedin_connections.json`
- Uses cookies to maintain session and avoid repeated logins
- Includes basic test cases with Django TestCase

---

## 📦 Technologies Used

- Python 3.10+
- Selenium
- Undetected ChromeDriver
- Django (for running test cases)

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash[
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/varghesejojo/linkedin-scraper.git)
cd linkedin-scraper

### 2. Activate the Existing Virtual Environment

This project already includes a virtual environment setup. Simply activate it:

- On **Windows**:

```bash
linkedin\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4 Environment Variables
change the valid  email id and password linkedin
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password

🗝️ LinkedIn Session Management (Cookies)
The script saves LinkedIn cookies in a file named linkedin_cookies.json to maintain an active session and avoid logging in repeatedly.

On the first run, the script logs in with the credentials you provide and saves the cookies in linkedin_cookies.json.

On subsequent runs, the script will attempt to use the saved cookies to maintain the session. If the cookies have expired (older than 1 day), it will log in again and refresh the cookies.

📝 File Structure
linkedin_cookies.json: Stores the cookies to maintain the session.

🧪 Running Tests
python manage.py test

🕵️‍♂️ How It Works
The script uses undetected_chromedriver to bypass LinkedIn's bot detection.

It logs in using the provided credentials and stores the session cookies.

It visits the connections page and continuously scrolls to load all contacts.

It scrapes and stores the data in a structured JSON format.

📁 Output
The connections will be saved in a file called:
linkedin_connections.json

Additionally, the session cookies will be stored in:
linkedin_cookies.json

❗ Disclaimer
This project is intended for personal and educational use only. Scraping LinkedIn may violate their Terms of Service, and your account could be restricted or banned. Use responsibly.

🧑‍💻 Author
Developed by Varghese Jojo
