import os

import requests
import csv
from datetime import datetime
import re
import matplotlib.pyplot as plt


"""A script that uses the NewsAPI to obtain data about news articles mentioning the European Union, counts the most common words in those articles, and visualizes the results in a bar chart.

Learning outcomes:
- use `re.split(r"[^a-zA-Z]+", text)` to split a string by anything that is not a letter and remove empty strings
- use `plt.barh()` to create a horizontal bar chart
- use `plt.gca().invert_yaxis()` to invert the y-axis of a bar
- use os module to create a data directory and avoid directory issues when running the script in different environments (virtual environment vs notebook)"""

#######################################################################################
######################## Functions used in the main script ############################
#######################################################################################

# Obtain an API key from https://newsapi.org/ and save data about news articles mentioning the European Union to a CSV file.

def get_news_newsapi(key_word, language, API_KEY,from_date="2026-03-25", to_date="2026-03-27", 
                     sort_by="publishedAt", page=1):
    """Return a list of dictionaries containing information about news articles mentioning the key word in the specified language.
    Each dictionary contains the title, source, and publication date of an article.
    Also return the publication date of the first and last articles in the list.
    Articles are saved to a CSV file named news.csv in the data directory.
    """
    
    # Loop through pages of results until there are no more articles to retrieve
    articles = []
    while True:
        url = f"https://newsapi.org/v2/everything?q={key_word}&from={from_date}&to={to_date}&page={page}&sortBy={sort_by}&language={language}&apiKey={API_KEY}"
        
        response = requests.get(url)
        data = response.json()

        # Error handling for API requests
        if response.status_code != 200: # Check if the request was successful
            print(f"\nError: {response.status_code} {response.reason}") 
            if response.status_code == 426: # Check if the error is due to too many requests
                print(f"For the free plan we have a speed limit about 5 requests per minute. ")
            else:
                print("Only allow date upto one month ago.")
                print("Only allow 50 request per 12 hours.")
            
            return articles, len(articles), sort_by
            
        else:
            articles_page = data["articles"]    
            articles.extend(articles_page)
            page += 1
            print(f"Total {len(articles_page)} articles saved from page {page-1}...")

            if len(articles_page) == 0  or page > 100: # Check if there are less than 30 articles in the current page or if we have retrieved more than 100 pages (to avoid infinite loop)
                print(f"\n{data['totalResults']} articles found.") 
                print(f"The most {len(articles)} {sort_by} articles are downloaded.")
                return articles, len(articles), sort_by

def save_news_articles_to_csv(articles, file_name):
    """Save a list of article dictionaries to a CSV file."""
    # Save the information about each article to a CSV file
    # Create a CSV file and write the header row
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # script
    except NameError:
        BASE_DIR = os.getcwd()  # notebook

    DATA_DIR = os.path.join(BASE_DIR, "..", "data")
    os.makedirs(DATA_DIR, exist_ok=True)
    file_path = os.path.join(DATA_DIR, f"news_{file_name}.csv")

    with open(f"{file_path}", "w", newline="", encoding="utf-8") as file: # use "w" to overwrite the file each time, instead of "a" to append to the file
        writer = csv.writer(file)
        
        for article in articles:
            title = article["title"]
            source = article["source"]["name"]
            date = datetime.strptime(article["publishedAt"] , "%Y-%m-%dT%H:%M:%SZ")
            url = article["url"]
            writer.writerow([date, source, title, url])
    print(f"\nSaved {len(articles)} articles to ../data/news_{file_name}.csv")

def get_dates(articles):
    """Return the publication date of the first and last articles in the list."""
    try:
        dates = [datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ") for article in articles]
    except ValueError as e:
        print(f"Error parsing dates: {e}")
        return None, None

    first_date = min(dates) if dates else None
    last_date = max(dates) if dates else None
    print(f"First article published at: {first_date}")
    print(f"Last article published at: {last_date}")
    return first_date.strftime("%Y-%m-%dT%H:%M:%SZ"), last_date.strftime("%Y-%m-%dT%H:%M:%SZ"),


# Some data cleaning and visualization functions
def remove_grammatical_words(article):
    """Return a list of words with common grammatical words removed from article."""
    words_to_remove = ["the", "is", "and", "of", "to", "in", "a", "that", "it","its",
                       "your","his","her","their","our","my","you","he","she","they",
                       "with","says","for","on","as","was","by","at","from","be",
                       "are","this","which","an","has","have","but","not","or",
                       "s","a","w","i","n","t","l","m","d","u","r","c","e","f","g",
                       "h","j","k","q","v","x","y","z",
                       "how", "what", "who", "when", "where", "why", "all", "any", "some", "no",
                       "can", "could", "should", "would", "may", "might", "must", "will", "shall",
                       "do", "does", "did", "have", "has", "had", "be", "am", "is", "are", "was", 
                       "were", "been", "being", "i", "you", "he", "she", "it", "we", "they", "me", "him", "her",
                       "just","one","into","up","out","about","over","after","before","between","under","then","once","here","there","when","where","why","how","all","any"]
    for word in article[:]:
        if word in words_to_remove:
            article.remove(word)

    return article

def dict_counting(article, dict={}):
    """Return a dictionary that adds new keys to be words in article and values to be counts of those words."""
    for word in article[:]:
        if word in dict.keys():
            dict[word] += 1
        else:
            dict[word] = 1

    return dict

def sort_truncate_dict(count_dict, threshold=3):
    """Return a sorted dictionary with keys as words and values as counts, truncated to only include words with counts above the threshold."""
    sorted_counts = dict(
        sorted(count_dict.items(), key=lambda item: item[1], reverse=True)
    )
    sorted_counts_truncated = {}
    for word, count in sorted_counts.items():
        if count >= threshold:
            sorted_counts_truncated[word] = count

    return sorted_counts_truncated

def bar_chart(count_dict, key_word="key word", first_date="first date", last_date="last date",total_articles=None,sort_by=None,figure_size=(12,12), dpi_number=120,x_int_step=1):
    """Return a bar chart of a given dictionary with keys as words and values as counts."""

    words = list(count_dict.keys())
    counts = list(count_dict.values())

    figure = plt.figure(figsize=figure_size,dpi=dpi_number)
    plt.barh(words,counts, 
            color='skyblue',
            edgecolor='black')
    if total_articles and sort_by:
        plt.title(f"Counts of Words in the Most {total_articles} {sort_by} News Articles Mentioning the {key_word} "
                f"\nfrom {first_date} to {last_date}")
    else:
        plt.title(f"Counts of Words in News Articles Mentioning {key_word} "
                  f"\nfrom {first_date} to {last_date}")
    plt.xlabel("Counts")
    plt.ylabel("Words")

    # Invert y-axis to have the highest counts at the top
    plt.gca().invert_yaxis()
    # set x-axis short ticks to be integers
    plt.xticks(range(0, max(counts)+1, x_int_step))
    
    # plt.xticks(rotation=-90, ha='left') # Rotate x-axis labels by -45 degrees and align them to the left
    plt.grid(axis='x', linestyle='--', alpha=0.3)

    plt.tight_layout()

    return figure


#######################################################################################
########################### Main function to run the script ###########################
#######################################################################################

def main():

    key_word_user=input("Please enter the key word you want to search for in news articles (type help for options): ")
    if key_word_user.lower() == "help":
        print("You can enter any key word you want to search for in news articles.")
        print("use keyword* to search any word that starts with the keyword.")
        print("use keyword1 OR keyword2 to search for articles mentioning either keyword.")
        print("use keyword1 AND keyword2 to search for articles mentioning both keywords.")
        print("For example, to find articles mentioning about Europ, we recommed you to enter: Euro* OR eu")
        key_word=input("Please enter the key word you want to search for in news articles: ")
    from_date_user=input("Please enter the start date for searching news articles (format: YYYY-MM-DD) upto one month: ") 
    to_date_user=input("Please enter the end date for searching news articles (format: YYYY-MM-DD) we don't recommend more than 20 days period: ")
    sort_by_user=input("Please enter the sorting method for news articles from (publishedAt, relevancy, popularity): ")
    api_key=input("Please enter your API key from https://newsapi.org/register: ")

    articles, total_articles, sort_by = get_news_newsapi(key_word=key_word_user, from_date=from_date_user, to_date=to_date_user, language='en',sort_by=sort_by_user, API_KEY=api_key)
    first_date, last_date  = get_dates(articles)
    save_news_articles_to_csv(articles, file_name=f"{first_date[:10]}_{last_date[:10]}")

    if not articles:
        print("No articles found. Exiting.")
    else:
        count_dict= {}
        for article in articles:
            source =  [
            w for w in re.split(r"[^a-z]+", article["title"].lower())
            if w
            ] #split by anything that is not a letter and remove empty strings
            article = remove_grammatical_words(source)
            count_dict = dict_counting(article, count_dict)
        print(f"\nTotal {len(count_dict)} unique words found in the articles. Now we can continue to the nexxt step of visualizing ...")

    sorted_counts_limited = sort_truncate_dict(count_dict, threshold=8)
    figure = bar_chart(sorted_counts_limited, key_word=key_word_user, first_date=first_date[:10], total_articles=total_articles, sort_by=sort_by_user, last_date=last_date[:10], figure_size=(12,10),x_int_step=5)

    plt.show()
    
    figure_vertical_size = 10
    threshold_new = 8

    while True:
        stop = input("Do you want to adjust the figure? (yes/no): ")
        if stop.lower() != "yes":
            figure.savefig(f"../data/figure_{first_date[:10]}_{last_date[:10]}_threshold{threshold_new}_size{figure_vertical_size}.png", dpi=300)
            print(f"Figure saved as figure_{first_date[:10]}_{last_date[:10]}_threshold{threshold_new}_size{figure_vertical_size}.png in the data directory.")
            print("Exiting the program. Thank you!")
            break
        figure_vertical_size = input(f"Is the vertical size of the figure acceptable? If yes, press Enter. If not, please enter a new value (current size is {figure_vertical_size}): ") or figure_vertical_size
        threshold_new = input(f"Currently we only show words with counts greater than {threshold_new}. Please enter a new threshold or press Enter to keep the current one: ") or threshold_new

        figure_vertical_size = int(figure_vertical_size)
        threshold_new = int(threshold_new)
        sorted_counts_limited = sort_truncate_dict(count_dict, threshold=threshold_new)
        figure = bar_chart(sorted_counts_limited, key_word=key_word_user, first_date=first_date[:10], total_articles=total_articles, sort_by=sort_by_user, last_date=last_date[:10], figure_size=(12, figure_vertical_size),x_int_step=5)
        plt.show()
        

if __name__ == "__main__":
    main()