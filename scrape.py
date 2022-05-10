import requests
import re
import json


CLEANR = re.compile('<.*?>') 

search_term = "राजनीति"

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

def delete_file_content(file_ptr) -> None:
  """Delete all the content of file"""
  file_ptr.seek(0)
  file_ptr.truncate()

def add_page_index(file_p, search_title: str, page_no: int) -> None:
    """Update the page index of the file to the last fetch page from the site"""
    file_p.seek(0)
    data = json.load(file_p)
    data[search_title] = page_no
    delete_file_content(file_p)
    json.dump(data, file_p)

def load_article(file_p, search_term: str, current_page: int) -> list:
    """Returns article list based on search_title"""
    end_page_no = 10  # fetch articles till page (end_page_no -1)
    cleaned_articles = []  # list of articles

    for page in range(
        current_page + 1, end_page_no
    ):  # each page contains 10 articles in general condition
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
            print(f"Page {page} loaded")

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
        print(index_data)
        try:
            current_page = index_data[search_term]
            with open(f"{search_term}.json", "r+") as article_f:
                previous_articles = json.load(article_f, strict=False)
                new_articles = load_article(index_f, search_term, current_page)
                previous_articles.extend(
                    new_articles
                )  # append previously loaded articles with newly fetched articles
                delete_file_content(article_f)
                json.dump(previous_articles, article_f)

        except (KeyError, FileNotFoundError):
            index_data.update({search_term: 0})
            current_page = index_data[search_term]
            delete_file_content(index_f)
            json.dump(index_data, index_f)
            with open(f"{search_term}.json", "w") as article_f:
                new_articles = load_article(index_f, search_term, current_page)
                try:
                    json.dump(new_articles, article_f)
                except:
                    print("Fetch Error!!")

print("\n--completed--")