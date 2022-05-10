import requests
import re
import json

search_term = "राजनीति"
page_start, page_end =  1,4 # Each page has 10 articles

try:
    with open(f"{search_term}.json") as f:
        data = json.load(f)
except:
    data = {"page": 1}


def cleanhtml(raw_html):
    CLEANR = re.compile('<.*?>') 
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext

def load_article(search_term,page_start):
    """Returns article list based on search_title"""

    cleaned_articles = []  # list of articles

    for page in range(
        page_start, page_end
    ):  # each page contains 10 articles in generally
        url = (
            "https://bg.annapurnapost.com/api/search?title="
            + search_term
            + "&page="
            + str(page)
        )
        response = requests.get(url)
        json_response = response.json()

        try:
            items = json_response["data"]["items"]
            for i, _ in enumerate(items):  # loop over the articles
                content = items[i]["content"]
                cleaned_article = cleanhtml(content)
                cleaned_articles.extend(
                    cleaned_article
                )  # append individual articles in a list
            page_start +=1 # update the page index
            print(f"Loading Page {page}")

        except KeyError:
            if cleaned_articles.__len__ == 0:
                print("No articles found")
                return None
            else:
                print("No more data availabel!!!")
                return cleaned_articles
    return cleaned_articles



if __name__ == "__main__":
    try:
        current_page = page_start
        with open(f"{search_term}.json","r+") as file:
            previous_articles = json.load(file)
            new_articles = load_article(search_term, current_page)
            previous_articles.extend(
                new_articles
            )  # append previously loaded articles with newly fetched articles
            json.dump(previous_articles, file)
    except (KeyError, FileNotFoundError):
        current_page = page_start
        with open(f"{search_term}.json", "w") as file:
            new_articles = load_article(search_term, current_page)
            try:
                json.dump(new_articles, file)
            except:
                print("Error occured while fetching!")

