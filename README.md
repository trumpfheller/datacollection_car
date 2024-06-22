# datacollection_car

My goal is to do more data [analysis](https://trumpfheller.github.io/databasics/ev.html).
So far my database was based on existing data collections publicly available. 
Which comes with its pros and cons: 
- saving time
- not finding what I really want

In an effort to see what is possible I started to flirt with the idea, 
to collect my own data.

scraping data from 
- cargurus,
- carmax,
- craigslist,
- edmunds

using 
- python
- selenium
- request and beautifulsoup

Result:
- CAPTCHA prevented the data collection
- for craigslist, since I focused on the craigslist title which was not standarized, I had to use regular expressions to create at least two useful columns

Next Step:
- have to learn how to circumvent mechanisms that prevent automated scraping
OR
- I go back to public available datasets.
