from googlesearch import search
import googlesearch
googlesearch.url_search()
for url in search('"Breaking Code" WordPress blog', 'no',country=, stop=20):
    print(url)