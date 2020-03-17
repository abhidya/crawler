# crawler
The goal of this project is to build a very simple web crawler which fetches URLs and outputs crawl results to some sort of log or console as the crawl proceeds.

# Installation
 `pip install tqdm `
 
 # Usage
 
 `python crawler.py https://rescale.com `
 
  `python crawler.py https://rescale.com 100 `

 # Arguments
 
  1. `url` The URL to begin crawling from, this has [validation](https://docs.djangoproject.com/en/3.0/ref/validators/#urlvalidator) to ensure it follows http/https schema 
  2. `max_crawl` A number for the max amount of websites to visit (ex: 100)

# Output

  Visits and links are logged to console. 
  A CSV file called `data.csv` is saved with the following columns:
  
    1. "url": The URL scraped
    
    2. "html": The HTML Response
    
    3. "created_at": The time it was scrapped in [ISO format](https://www.iso.org/iso-8601-date-and-time-format.html)
    
    4. "links": The scraped links
    
    5. "success": True if no errors were raised, False if an error was raised
    
