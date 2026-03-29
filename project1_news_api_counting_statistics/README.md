# News API Word Frequency Analyzer

This project fetches news articles using the News API, analyzes the frequency of words in article titles, and visualizes the results with a horizontal bar chart.

It combines API usage, text processing, and data visualization in a simple end-to-end workflow.


## Features

- Fetch news articles based on custom keywords
- Save article data to CSV
- Clean and process text using regular expressions
- Count word frequencies in article titles
- Visualize results with a customizable bar chart


## Project Structure

-   The project is structured as follows:
    - `src/`: Contains the main Python script `newsapi_words_counting.py` that implements the functionality of fetching news articles, counting words, and visualizing results.
    - `notebooks/`: Contains Jupyter Notebooks for exploration and analysis of the data.
    - `data/`: This directory will be created to store the CSV files containing the news articles data. The figure is also saved in this directory.
    - `README.md`: This file provides an overview of the project, its structure, and instructions on how to run it.
-   The main script `newsapi_words_counting.py` includes functions to:
    - Fetch news articles from the News API based on user-defined parameters (keyword, date range, sorting method).
    - Save the fetched articles to a CSV file.
    - Count the occurrences of words in the article titles.
    - Visualize the word counts using a bar chart.
---

## Parameters

The script allows flexible input:

- **keyword**
  - Use `*` for wildcard searches  
    e.g. `eur*` matches "euro", "eurusd", etc.
  - Use `OR` for multiple keywords  
    e.g. `euro OR dollar`
  - Use `AND` for combined conditions  
    e.g. `euro AND dollar`

- **from_date**  
  Format: `YYYY-MM-DD`

- **to_date**  
  Format: `YYYY-MM-DD`

- **sort_by**  
  Options: `relevancy`, `popularity`, `publishedAt`

- **threshold**  
  Minimum word frequency displayed in the chart

- **figure_size**  
    Define the vertical size of the figure. The horizontal size is fixed at 12.


## Quick Start

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-name>
### 2. Install dependencies
```bash
pip install requests matplotlib
```
### 3. Obtain API Key
- Sign up at [News API](https://newsapi.org/register) to get your API key.
### 4. Run the script
```bash
python src/newsapi_words_counting.py
```
- Follow the prompts to enter your parameters.


## The python packages used are the following:
    - `requests`: For making HTTP requests to the News API.
    - `os`: For handling file paths and directories in different operating systems.
    - `csv`: For reading and writing CSV files.
    - `matplotlib`: For visualizing the word counts in a bar chart.
    - `datetime`: For handling date and time operations.
    - `re`: For regular expressions to clean and process the article titles.

## Example Usage
1. Run the script and follow the prompts to enter your parameters:
   - Keyword: `happy`
   - from_date: `2026-03-01`
   - to_date: `2026-03-27`
   - sort_by: `relevancy`
   - threshold: `10`
   - figure_size: `6` this will create a figure of size (12, 6)
![Example Bar Chart](data/example_bar_chart.png)

## License
Free for personal use and educational purposes. Not for commercial use without permission. 
