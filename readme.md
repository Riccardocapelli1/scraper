# LinkedIn Job Scraper

This Python script uses Selenium and BeautifulSoup to scrape job postings from LinkedIn. The script searches for job postings based on a given job title and location, and extracts job information such as job title, company name, location, date posted, job description, seniority level, employment type, job function, and industry.

## Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/Riccardocapelli1/scraper
```

Navigate to the project directory:

```bash
cd https://github.com/Riccardocapelli1/scraper
```
Install the required Python packages:
``` python
pip install -r requirements.txt
```
Download the appropriate web driver for your browser and operating system, and place it in the project directory. You can download the latest version of the Firefox driver here.

## Usage

Open the main.py file in a text editor and modify the jobs_prompt and locations lists to search for job postings that match your criteria. For example:

```python
jobs_prompt = ['Analisi dei Dati','Vendite']
locations = ['Reggio','Verona']
```
Run the script:

```python
python scraper2.py
```
The script will scrape job postings from LinkedIn and save the results in a CSV file with a filename based on the job title, location, and current date. The CSV file will be saved in the project directory.

## License

This project is licensed under the MIT License - see the LICENSE file for details.