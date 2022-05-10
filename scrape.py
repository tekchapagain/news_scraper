import requests
import re
import json

search_term = "राजनीति"
page_start, page_end =  1,5  # Each page has 10 articles

CLEANR = re.compile('<.*?>') 

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

def delete_file_content(file_ptr) -> None:
  """Delete all the content of file"""
  file_ptr.seek(0)
  file_ptr.truncate()

def add_page_index(file_p, search_title, page_no):
    """Update the page index of the file to the last fetch page from the site"""
    file_p.seek(0)
    data = json.load(file_p)
    data[search_title] = page_no
    delete_file_content(file_p)
    json.dump(data, file_p)

def load_article(file_p, search_term, current_page):
    """Returns article list based on search_title"""
    cleaned_articles = []  # list of articles

    for page in range(
        current_page + 1, page_end
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
                cleaned_articles.append(
                    cleaned_article
                )  # append individual articles in a list
            add_page_index(file_p, search_term, page)  # update the page index
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

    with open("index.json", "r+") as index_f:
        index_data = json.load(index_f)
        try:
            current_page = index_data[search_term]
            with open(f"{search_term}.json", "r+") as f:
                previous_articles = json.load(f, strict=False)
                new_articles = load_article(index_f, search_term, current_page)
                previous_articles.extend(
                    new_articles
                )  # append previously loaded articles with newly fetched articles
                delete_file_content(f)
                json.dump(previous_articles, f)

        except (KeyError, FileNotFoundError):
            index_data.update({search_term: 0})
            current_page = index_data[search_term]
            delete_file_content(index_f)
            json.dump(index_data, index_f)
            with open(f"{search_term}.json", "w") as f:
                new_articles = load_article(index_f, search_term, current_page)
                try:
                    json.dump(new_articles, f)
                except:
                    print("Fetch Error!!")