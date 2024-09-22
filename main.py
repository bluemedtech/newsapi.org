
import requests
import ftplib
import os
# Replace with your actual API key. for use in a live project
# it's best to keep your API key encrypted in a database 
API_KEY = 'REPLACE WITH YOUR newsapi.org API KEY'
url = 'https://newsapi.org/v2/top-headlines'


FTP_HOST = 'YOUR FTP SERVER'
FTP_USER = 'FTP LOGIN'
FTP_PASS = 'YOUR FTP PASSWORD'
HTML_FILE_PATH = '/index.html'   # to be recreated and uploaded
REMOTE_PATH = 'public_html/index.html'



def news_cruise():
    nx = 0
    filepath = "index.html"
    if os.path.exists(filepath):
        os.remove(filepath)
        
    # Parameters for the API request
    params = {
        'apiKey': API_KEY,
        'country': 'us',  # You can change this to any country code (e.g., 'us', 'gb', 'ca')
        'pageSize': 20     # Number of articles to retrieve (max is 100)
    }

    # Make the GET request to the NewsAPI
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract the articles
        articles = data.get('articles', [])
        
        # Print headlines
        for article in articles:
            print(f"title: {article['title']}\n")
            print(f"description: {article['description']}\n")
            print(f"url: {article['url']}\n")
            
            with open("index.html", "a") as file:
                if nx == 0:
                    file.write(f"<html><head></head><title>BricsNow Headlines</title><BODY>")
                    file.write("<h1>BricsNow Headlines</h1>")
                    
                file.write(f"<h3><a href='{article['url']}'>{article['title']}</a></h3>")
                file.write(f"<strong>{article['description']}</strong>")
                file.write(f"<i><a href='{article['url']}'>{article['url']}</a></i>")
            
            
            nx += 1
        
        print(f"{nx} articles found.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

        
    if nx > 0:
        ftp_upload()
        

def ftp_upload():

    try:
        ftp = ftplib.FTP_TLS(FTP_HOST, timeout=30)  # Set a timeout of 30 seconds
        ftp.login(FTP_USER, FTP_PASS)  # Log in with your credentials
        ftp.set_pasv(True)  # Enable passive mode

        # Perform FTP actions here
        print("Connected successfully!")
        
        # Open the file in binary mode for reading
        with open('index.html', 'rb') as file:
            # Use storbinar to upload the file
            ftp.storbinary('STOR index.html', file)  # Upload the file as 'index.html'

    except ftplib.all_errors as e:
        print(f"FTP error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if 'ftp' in locals():
            ftp.quit()  # Close the connection if it was established


# call functions
news_cruise()
ftp_upload()

