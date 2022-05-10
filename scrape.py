import requests
import json
import re


search_title = "राजनीति"  #Change search Term here
page_end = 3       #Change Page number here

try:
    with open(f"{search_title}.json") as f:
        data = json.load(f)
except:
    data = {"page": 1, "items": []}

update = data["page"]

def cleanhtml(raw_html):
    CLEANR = re.compile('<.*?>') 
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext

def load_article():
    url = (
        "https://bg.annapurnapost.com/api/search?title="
        + search_title
        + "&page="
        + str(page)
    )
    response = requests.get(url)
    response = response.json()
    cleaned_articles = []
    try:
        items = response["data"]["items"]
        for i, _ in enumerate(items):  # loop over the articles
            content = items[i]["content"]
            cleaned_article = cleanhtml(content)
            cleaned_articles.extend(
                cleaned_article
            )  # append individual articles in a list
    except KeyError:
        if cleaned_articles.__len__ == 0:
            print("No articles found")
            return None
        else:
            print("No more data availabel!!!")
            return cleaned_articles
    return cleaned_articles
        

if __name__ == "__main__":
    for page in range( data["page"], page_end): 
        items = load_article()
        data["items"].extend(items)
        data["page"] += 1  # update the page index
        print(f"Loading Page {page}")
        with open(f"{search_title}.json", "w") as f:
            json.dump(data, f)

if update != page_end:
    print("Completed!")
else:
    print("Already updated!")