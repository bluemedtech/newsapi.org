
import requests
import ftplib
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import os

FTP_HOST = 'IP_ADDRESS'
FTP_USER = 'USR'
FTP_PASS = 'YOUR_PW'
HTML_FILE_PATH = 'bootstrap_template/index.html'
REMOTE_PATH = 'public_html/index.html'

def get_tvbrics(url):
    full_url = ""
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    news_string = ""
    repeater = '<h3>'     
    repeater += '<a href="<!--url-->" class="text-primary"><!--title--></a>'
    repeater += '</h3>' 
    repeater += '<strong><!--author--></strong>'
    
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Parse the content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all div tags with the specified class
        news_items = soup.find_all('div', class_='news-item__name')
        
        for item in news_items:
            # Extract the text
            text = item.get_text(strip=True)
            # Find the anchor tag within the div
            link = item.find('a', href=True)
            if link:
                # Extract the URL
                url = link['href']
                
                if "en/news/" in url and len(text.split()) > 3:
                    print(f"Text: {text}")
                    print(f"URL: {url}")
                    print()
                    
                    full_url = base_url + url
                    this_item = repeater
                    
                    this_item = this_item.replace("<!--url-->", full_url if full_url is not None else "")
                    this_item = this_item.replace("<!--title-->", text if text is not None else "")
                    this_item = this_item.replace("<!--author-->", base_url if base_url is not None else "")
                    
                    news_string += f"<p>{this_item}</p>\n" 
            else:
                print(f"Text: {text}, URL: No link found")
                
        return(news_string)
                
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")

# Example usage
# get_news("YOUR_URL_HERE")

        
    
    
def get_aljazeera(url, keyword = "*"):
    found = False
    full_url = ""
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    news_string = ""
    nx = 0 
    
    # Get the current date and time
    now = datetime.now()

    # Format the date and time
    formatted_date_time = now.strftime("%d") + ("th" if 4 <= now.day % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(now.day % 10, "th")) + " - " + now.strftime("%b - %Y, %H:%M GMT")

    print(formatted_date_time)

    
    repeater = '<h3>'     
    repeater += '<a href="<!--url-->" class="text-primary"><!--title--></a>'
    repeater += '</h3>' 
    repeater += '<strong><!--author--></strong>'
    
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Parse the content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all anchor tags
        links = soup.find_all('a', href=True)
        
        short_list = ["/newsfeed/", "/the_stream/", "/the-big-picture/", "/news/"]
        avoid = "video duration"
        
        for link in links:
            for url_part in short_list:
                if url_part in link['href']:
                    if len(link.text.split()) > 3 and avoid.lower() not in link.text.lower():
                        if keyword == '*':
                            found = True
                        else:
                            if keyword in link.text:
                                found = True
                            else:
                                found = False
                
            if found:
                nx += 1
                this_item = repeater

                print(link.text)
                full_url = base_url + link['href']
                print(full_url)
                
                this_item = this_item.replace("<!--url-->", full_url if full_url is not None else "")
                this_item = this_item.replace("<!--title-->", link.text if link.text is not None else "")
                this_item = this_item.replace("<!--author-->", base_url if base_url is not None else "")
                
                news_string += f"<p>{this_item}</p>\n" 
                
                print()
                found = False

        return(news_string)
        
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []


def write_template(brics_news, world_news):
    now = datetime.now()

    # Format the date and time
    formatted_date_time = now.strftime("%d") + ("th" if 4 <= now.day % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(now.day % 10, "th")) + " - " + now.strftime("%b - %Y, %H:%M GMT")

    with open("bootstrap_template/index_bts.html", "r") as template_file:
            template = template_file.read()
            template = template.replace("<!--world_news_items-->", world_news)
            template = template.replace("<!--brics_news_items-->", brics_news)
            template = template.replace("<!--DATE-->", formatted_date_time)
        
    filepath = "bootstrap_template/index.html"
    if os.path.exists(filepath):
        os.remove(filepath)
    
    with open("bootstrap_template/index.html", "a") as file:    
        file.write(template)   
        
def ftp_upload():

    try:
        ftp = ftplib.FTP_TLS(FTP_HOST, timeout=10)  # Set a timeout of 30 seconds
        ftp.login(FTP_USER, FTP_PASS)  # Log in with your credentials
        ftp.set_pasv(True)  # Enable passive mode

        # Perform FTP actions here
        print("Connected successfully!")
        
        # Open the file in binary mode for reading
        with open(HTML_FILE_PATH, 'rb') as file:
            # Use storbinar to upload the file
            ftp.storbinary('STOR index.html', file)  # Upload the file as 'index.html'

    except ftplib.all_errors as e:
        print(f"FTP error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if 'ftp' in locals():
            ftp.quit()  # Close the connection if it was established

        

world_news = get_aljazeera("https://www.aljazeera.com/middle-east")
brics_news = get_tvbrics("https://tvbrics.com/en/news/")


write_template(brics_news, world_news)
ftp_upload()
# Example usage
# print(get_links_with_keyword("https://www.aljazeera.com/middle-east", "*"))

# short_list = ["/newsfeed/", "the_stream", "the-big-picture"]
# link = {'href': 'https://example.com/the_stream'}

# # Check if any item in short_list is in link['href']
# found = any(item in link['href'] for item in short_list)

# print("Found:", found)
