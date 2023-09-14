## Distinctiveness and Complexity

My Banking App project is something I'm really proud of because it brings together my passion for web development and my background in finance. Unlike other projects in the course, this app goes beyond the basics and dives into the exciting world of banking. I built it from the ground up, incorporating essential features like creating accounts, logging in, making simulated transactions, and even managing a basic stock portfolio.

What makes this project unique is its direct relevance to the finance field. Being someone who understands the importance of merging technology and finance, I saw this as an opportunity start learning how to bridge that gap. By creating this banking app, I'm taking my first steps towards leveraging technology in the financial domain, and it feels amazing.

Integrating different components was a fascinating challenge. Firstly, I had to make API calls to fetch real-time stock market data. This allowed users to experience the thrill of buying and selling stocks within their portfolio. It involved handling asynchronous requests, parsing JSON data, and presenting the information in a meaningful way.
I also implemented a nifty binary search algorithm in the transfer money feature. This clever algorithm quickly searches and validates user input as they type, minimizing the chances of errors during transactions.

I didn't incorporate secure password handling or robust authentication mechanisms. This project is more of a bare-bones implementation, focusing on the core functionalities of a banking app. It's a starting point for me, and I acknowledge that there's room for improvement in terms of security features. But hey, we all have to start somewhere, right?
Building the frontend was definitely a challenge for me since my skills in that area are a work in progress (let's just say I'm still learning the ropes!). But hey, I did my best to create a clean and intuitive user interface that anyone can navigate with ease. So, while it may not be the most polished frontend you've ever seen, I hope it gets the job done and provides a decent user experience.

Overall, the Banking App project is a testament to my journey as a developer, combining my passion for web development with my fascination for finance. Its relevance to the finance field, integration of APIs, utilization of a binary search algorithm, and my earnest attempt at frontend design make it a project that I'm truly proud of.

## File Contents

The project structure includes the following files and directories:

### Banking App

**`functions.py`** This file contains functions that are utilized in the views.py file. Two of which are searchStock to quickly search and retrieve stock information and searchAccount performs a binary search to validate and retrieve user account details.

**`models.py`**: This file defines four models: Account, Transactions, StockPortfolio, and User. These models represent the database structure and handle data storage and retrieval.

**`secrets.py`** This file is used to hold sensitive information, such as the API key, and is added to the .gitignore file to ensure it is not committed to the repository.

**`urls.py`** This file contains URL mappings that direct traffic within the website. It defines links from page to page, as well as links for API calls.

**`views.py`**: This file contains the main functions that drive the application. It includes the following functions:

- **register**: Handles the registration of new users.
- **index** Redirects the user to their account homepage and passes transaction and account data. The loading of stocks on this page is
  handled by JavaScript.
- **login** Handles the authentication of users.
- **logout** Logs out the currently logged-in user.
- **deposit** Allows users to deposit money into their account.
- **download_transactions** Enables users to download their transactions in a CSV file, similar to a bank statement.
- **tradestocks** Handles the trading of stocks, including adding or decreasing the relevant amount from the user's account.
- and more....

### Templates Folder

`investing.html` This template is used for buying and selling stocks. Everything on this page was handled with React within a script tag.
`homepage.html` This template displays the user's account information, including their account balance, stock portfolio, and options to deposit money into their account.
`landing.html` This template serves as the landing page with general information about the banking app.
`layout.html` This template is the base layout for all other pages. It includes a navigation bar that is shared across all pages and contains meta tags and links.
`login.html` This template displays the login form for users to authenticate themselves.
`register.html` This template provides a form for new users to create an account.
`transfer.html` This template is used for transferring money between accounts.

### Static:

This contains a folder for each html file, each folder contains:
` style.css` This CSS file contains styling rules for the HTML templates.
`index.js` This JavaScript file is used for any dynamic features on the HTML templates.

## How to run

To run the application, follow these steps:

1.  Open a terminal or command prompt.
2.  Navigate to the project's main directory, where the `manage.py` file is located.
3.  Run the following command: `python manage.py runserver`.
4.  The development server will start running, and you should see output similar to `Starting development server at eg. http://127.0.0.1:8000/`.
5.  Open a web browser and enter the URL `http://127.0.0.1:8000/` to access the application or cmd + click the link on mac or ctrl + click on windows.

**External API**: The banking app utilizes the [Twelve Data API](twelevedata.com) to retrieve stock information and [Marketaux](marketaux.com) for the retrieve the news. No external Python packages were installed for this project.
