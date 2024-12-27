 # $\textsf{\color{skyblue} NCAA Men's Basketball Data Scraper}$

## $\textsf{\color{lightgreen} Description}$
This Python program scrapes detailed NCAA Men’s Basketball game and player statistics from ESPN. It retrieves team schedules and player rosters, extracts game statistics such as points, assists, rebounds, and minutes, and compiles them into structured CSV files. Using the BeautifulSoup library for web scraping, the program processes data for specific games this season up until a cutoff date and stores relevant player statistics. This tool allows for customizable stat selection and any number of teams and desired statistics.

## $\textsf{\color{lightgreen} Key Features}$

### 1. **Comprehensive Data Scraping**
- Scrape team schedules and player rosters from ESPN for NCAA Men’s Basketball, extracting essential game statistics like points, assists, rebounds, and three-pointers.

### 2. **Customizable Stat Selection**
- Easily select and scrape specific player statistics such as points, assists, or three-pointers, allowing for flexible data extraction tailored to your needs.

### 3. **Multi-Team Support**
- Input any number of teams and desired statistics. The program will create a directory for each team, inside which it will generate CSV files for each requested statistic.

### 4. **Automatic Data Processing and Export**
- Automatically process scraped data into well-organized CSV files by player and stat type, ready for further analysis.

### 5. **Cutoff Date Filtering**
- Define a cutoff date to filter out game data that occurs after your specified date, ensuring that only relevant game statistics are collected.

### 6. **Efficient Web Scraping Logic**
- Utilize BeautifulSoup and Requests libraries to seamlessly navigate ESPN pages, extracting and processing data efficiently.

### 7. **Secure Data Storage and Export**
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
- pyyaml

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
     <br>
   - If you don't have it installed, head to [python.org](python.org) to install. Alternatively, if you have homebrew installed, type
     ```
     brew install python
     ```
     into the command window.
     <br>
     
   - Next, navigate to the folder where the script has been cloned
     ```
      cd ~/path/to/cloned/repo/
     ```
     <br>
     
   - Finally, open a virtual environment and install the required dependencies by using the following commands.
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

## $\textsf{\color{lightgreen} Program Walkthrough}$

3. **Program Walkthrough:**
   - **Step 1: Opening the YAML file**
     - Open the project folder and navigate to the `config.yaml` file.
    <p align="center">
   <img src="ReadMe%20Images/step1.png" height="60%" width="60%" alt="Opening the Program"/>
   </p>

   - **Step 2: Update The Configuration Variables**
     - Update the `teams_to_scrape` to the teams you would like data for. Ensure that the names match the official team names listed on the ESPN website.
     - Update the `cutoff_date` to the latest date **THIS SEASON** you would like to data for
     - Update the `stats_to_pull` to the stats you would like to scrape. Scrapeable stats are listed in the file.
   <p align="center">
   <img src="ReadMe%20Images/step2.png" height="60%" width="60%" alt="Updating Global Variables"/>
   </p>

   - **Step 3: Run the Program**
     - In the command window where you set up the virtual environment, run
       ```
       python mbb_scraper.py
       ```
   <p align="center">
   <img src="ReadMe%20Images/step3.png" height="40%" width="40%" display="inline-block" alt="Running the program"/>
   </p>

   - **Step 4: View Stats**
     - The program will create a subdirectory for each team, containing a CSV file for each requested statistic.
   <p align="center">
   <img src="ReadMe%20Images/step4.png" height="60%" width="60%" alt="Your outputted files"/>
   </p>



