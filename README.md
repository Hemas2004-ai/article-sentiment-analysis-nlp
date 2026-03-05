Blackcoffer Data Extraction and NLP Assignment

Approach:
1. Data Extraction:
   URLs from Input.xlsx were scraped using Python with requests and BeautifulSoup.
   Article title and article content were extracted and saved as text files using URL_ID.

2. Text Analysis:
   The extracted text files were processed using NLP techniques.
   Stopwords and master dictionary were used to calculate sentiment and readability metrics.

How to Run:
1. Run the extraction script:
   python data_extraction.py

2. Run the analysis script:
   python text_analysis.py

Output:
The script generates final_output.xlsx containing all required variables.

Dependencies:
pandas
requests
beautifulsoup4
nltk
openpyxl