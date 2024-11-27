import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


"""we want to find citations from """
def main():
    paper_list_url = 'https://conferences.miccai.org/2023/papers/'
    response = requests.get(paper_list_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paper_to_cite = {}
    for a_tag in tqdm(soup.find_all('a', href=True)):
        if 'paper' in a_tag['href']:
            paper_to_cite[a_tag.contents[0]] = a_tag['href']
    # paper_links = [h for h in paper_links if 'html' in h]
    paper_to_cite = {k: v for k, v in paper_to_cite.items() if 'html' in v}
    # sort by paper name
    paper_to_cite = dict(sorted(paper_to_cite.items()))
    paper_to_cite = dict(list(paper_to_cite.items())[200:])


    for paper_name, paper_link in tqdm(paper_to_cite.items()):
        try:
            paper_html = paper_link.split('/papers/')[-1]
            paper_url = f"{paper_list_url}{paper_html}"
            response = requests.get(paper_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            # search for <a href="https://doi.org/10.1007/978-3-031-43907-0_14">https://doi.org/10.1007/978-3-031-43907-0_14</a>
            paper_to_cite[paper_name] = None
            for a_tag in soup.find_all('a', href=True):
                if 'doi.org' in a_tag['href']:
                    paper_to_cite[paper_name] = a_tag.contents[0]
                    break
        except Exception as e:

            paper_to_cite[paper_name] = None
    for paper_name, doi_link in tqdm(paper_to_cite.items()):
        try:
            if doi_link is None:
                print(f"Could not find doi for {paper_name}")
                continue
            response = requests.get(doi_link)
            soup = BeautifulSoup(response.content, 'html.parser')
            if len(soup.find_all('svg', class_='u-icon app-article-metrics-bar__icon')) != 2:
                citations = None
            citations = int(soup.find_all('svg', class_='u-icon app-article-metrics-bar__icon')[-1].nextSibling)
        except Exception as e:
            citations = None

        paper_to_cite[paper_name] = citations
    # save to csv with col name paper_name, citations
    import pandas as pd
    df = pd.DataFrame(paper_to_cite.items(), columns=['paper_name', 'citations'])
    df.to_csv(r'C:\Users\adarc\Downloads\output23.csv', index=False)





if __name__ == '__main__':
    main()