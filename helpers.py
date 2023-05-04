from googlesearch import search



# General functions
def google_search(self, search_term, num_results):
    for url in search(search_term, num_results=num_results):
        return url
