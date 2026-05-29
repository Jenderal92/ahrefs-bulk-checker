# Ahrefs Bulk Domain & URL Rating Checker

<img width="1750" height="407" alt="ahrefs-bulk-checker" src="https://github.com/user-attachments/assets/83587a62-7168-49d0-800c-34f6ad248f48" />


A Python 2 script to check **Domain Rating (DR)** and **URL Rating (UR)** of multiple domains using the official Ahrefs API. Results are filtered and saved to a file.

## Features

- Read a list of domains/URLs from a text file
- Automatically extract domain names from full URLs
- Query Ahrefs API for DR and UR metrics
- Save only domains that meet the threshold (default: **DR > 5** OR **UR > 5**)
- **You can change the number `5` for DR/UR according to your needs** (edit the condition in the script)
- Retry on server errors (500) with delay

## Prerequisites

- Python 2.7
- An active [Ahrefs API](https://ahrefs.com/api) account with a valid API token

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Jenderal92/ahrefs-bulk-checker.git
cd ahrefs-bulk-checker
```

1. (Optional) Create and activate a virtual environment:

```bash
virtualenv venv
source venv/bin/activate   # Linux/Mac
# or
venv\Scripts\activate      # Windows
```

1. Install dependencies:

```bash
pip install requests
```

Configuration

Open ahrefs.py and replace the placeholder with your actual Ahrefs API token:

```python
API_TOKEN = "your_actual_api_token_here"
```

Never share your API token publicly. Consider using environment variables or a config file for production.

Adjusting the DR/UR Threshold

By default, the script saves domains with DR > 5 or UR > 5.
You can change this value by editing the line inside main():

```python
if dr > 5 or ur > 5:   # Change the number 5 to your desired threshold
```

For example, to save only domains with DR > 20 or UR > 20, change it to:

```python
if dr > 20 or ur > 20:
```

Usage

Prepare a text file with one domain or URL per line. For example list.txt:

```
example.com
https://google.com
https://www.github.com
subdomain.example.org
```

Run the script:

```bash
python2 ahrefs.py list.txt
```

Output

· Console – shows progress, API status, and each result.
· res.txt – contains only domains that meet the criteria (default: DR > 5 or UR > 5), in this format:

```
domain: example.com | dr : 42.0 | ur : 18.5
domain: google.com | dr : 91.0 | ur : 65.0
```

How It Works

1. Input parsing – each line is cleaned, and the domain name is extracted.
2. API call – for each domain, the script sends a batch request to Ahrefs API (mode = exact, protocol = https).
3. Criteria filtering – if DR > 5 or UR > 5 (or your custom value), the result is appended to res.txt.
4. Delay – 1.5 seconds between requests to avoid rate limiting.

Error Handling

· Invalid/empty lines are skipped.
· API errors (non-200) are printed but do not stop execution.
· Server error (500) triggers up to 2 retries.
· Missing file input shows a friendly error.

Limitations

· Python 2 only (legacy). For Python 3, modify print statements and dependencies.
· Free Ahrefs API plan has limited requests per month – use responsibly.
· No multi-threading (sequential processing).


Disclaimer

This tool is for educational and legitimate SEO analysis purposes. Respect Ahrefs API terms of service and rate limits.
