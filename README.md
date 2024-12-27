 # $\textsf{\color{skyblue} NCAA Men's Basketball Data Scraper}$

## $\textsf{\color{lightgreen} Description}$
This Python program scrapes detailed NCAA Men’s Basketball game and player statistics from ESPN. It retrieves team schedules and player rosters, extracts game statistics such as points, assists, rebounds, and minutes, and compiles them into structured CSV files. Using the BeautifulSoup library for web scraping, the program processes data for specific games this season up until a cutoff date and stores relevant player statistics. This tool allows for customizable stat selection and can be easily adapted to scrape data for different teams by updating the URLs and parameters. The resulting CSV files are organized by player and stat type, ready for analysis.

## $\textsf{\color{lightgreen} Key Features}$

### 1. **Comprehensive Data Scraping**
- Scrape team schedules and player rosters from ESPN for NCAA Men’s Basketball, extracting essential game statistics like points, assists, rebounds, and three-pointers.

### 2. **Customizable Stat Selection**
- Easily select and scrape specific player statistics such as points, assists, or three-pointers, allowing for flexible data extraction tailored to your needs.

### 3. **Automatic Data Processing and Export**
- Automatically process scraped data into well-organized CSV files by player and stat type, ready for further analysis.

### 4. **Cutoff Date Filtering**
- Define a cutoff date to filter out game data that occurs after your specified date, ensuring that only relevant game statistics are collected.

### 5. **Efficient Web Scraping Logic**
- Utilize BeautifulSoup and Requests libraries to seamlessly navigate ESPN pages, extracting and processing data efficiently.

### 6. **Secure Data Storage and Export**
- Automatically create organized folders and export CSV files with clear naming conventions, ensuring data integrity and easy access.

  
## $\textsf{\color{lightgreen} Languages and Libraries Used}$
- Python
- Requests
- BeautifulSoup
- CBBpy
- Pandas
- os
- datetime
- re

# $\textsf{\color{skyblue} MBB Scraper Program Walkthrough}$

## $\textsf{\color{lightgreen} Cloning the Repository}$

1. **Clone the Repository:**
   - Open your terminal or command prompt.
   - Navigate to the directory where you want to clone the repository.
   - Run the following command:
     ```
     git clone <repository_url>
     ```
     Replace `<repository_url>` with the actual URL of the GitHub repository.

## $\textsf{\color{lightgreen} Setting Up the Environment}$

2. **Environment Setup:**
   - Ensure you have Python installed on your system. You can check by running:
     ```
     python --version
     ```
   - If you don't have it installed, head to [python.org](python.org) to install. Alternatively, if you have homebrew installed, type
     ```
     brew install python
     ```
     into the command window.
   - Next, open a virtual environment and install the required dependencies by using the following commands.
     <br/>
       - MacOS:
         ```
         python -m venv venv
         source venv/bin/activate
         pip install -r requirements.txt  
         ```
       - Windows:
         ```
         python -m venv venv
         venv\Scripts\activate
         pip install -r requirements.txt  
         ```
       - Linux:
         ```
         python -m venv venv
         source venv/bin/activate
         pip install -r requirements.txt 
         ```
   - Finally, navigate to the folder where the script has been cloned
     ```
      cd ~/path/to/cloned/repo/
     ```

## $\textsf{\color{lightgreen} Program Walkthrough}$

3. **Program Walkthrough:**
   - **Step 1: Opening the Program**
     - Open the project folder and navigate to the `single_team_scraper.py` file.
    <p align="center">
   <img src="ReadMe%20Images/step1.png" height="60%" width="60%" alt="Opening the Program"/>
   </p>

   - **Step 2: Update The Global Variables**
     - Update the `team_url`, `player_url`, and `team_name` if you want to change the team to scrape
     - Update the `cutoff_date` to the latest date **THIS SEASON** you would like to scrape
     - Update the `stats_to_pull` to the stats you would like to scrape. Scrapeable stats are listed in the file.
   <p align="center">
   <img src="ReadMe%20Images/step2.png" height="60%" width="60%" alt="Updating Global Variables"/>
   </p>

   - **Step 3: Run the Program**
     - In the command window where you set up the virtual environment, run
       ```
       python single_team_scraper.py
       ```
   <p align="center">
   <img src="ReadMe%20Images/step3.png" height="40%" width="40%" display="inline-block" alt="Running the program"/>
   </p>

   - **Step 4: View Stats**
     - The program will generate a subdirectory containing CSV files with all your scraped statistics.
   <p align="center">
   <img src="ReadMe%20Images/step4.png" height="60%" width="60%" alt="Your outputted files"/>
   </p>



