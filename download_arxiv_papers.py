import arxiv
import os
import warnings
import pandas as pd
from tqdm import tqdm

DOWNLOAD_DIR = r"C:\Users\adarc\Downloads\micai2023\papers"
CSV_PATH = r"C:\Users\adarc\Downloads\micai2023\miccai2023.csv"
N_PROCESSES = 4
# ignore DeprecationWarning

warnings.filterwarnings("ignore", category=DeprecationWarning)

def main():
    # Example usage
    df = pd.read_csv(CSV_PATH)

    if N_PROCESSES <= 1:
        for paper_name in tqdm(df['paper_name']):
            download_arxiv_paper(paper_name)
    else:
        from multiprocessing import Pool
        with Pool(N_PROCESSES) as p:
            p.map(download_arxiv_paper, df['paper_name'])


def download_arxiv_paper(paper_name, download_dir=DOWNLOAD_DIR):
    """
    Searches for a paper on arXiv by its name and downloads it.

    Args:
        paper_name (str): The name of the paper to search for.
        download_dir (str): The directory to save the downloaded paper. Defaults to "downloads".

    Returns:
        str: The path to the downloaded paper or an error message.
    """
    paper_name = paper_name.replace("_", " ")  # Replace underscores with spaces
    try:
        # Search for the paper on arXiv
        search = arxiv.Search(
            query=paper_name,
            max_results=500,
            sort_by=arxiv.SortCriterion.Relevance
        )

        # Get the first result
        paper = next(search.results(), None)
        found_paper = None
        for paper in tqdm(search.results()):
            if paper is not None:
                paper_title = paper.title.lower()
                if paper_name.lower() == paper_title:
                    found_paper = paper
                    break

        if found_paper is None:
            print(f"Problem with: {paper_name} - No paper found matching the name")
            return

        # Create download directory if it doesn't exist
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Download the paper
        paper_title = paper.title.replace(" ", "_").replace("/", "-")  # Sanitize title for filename
        paper_title = paper_title.replace(":", "---")
        file_path = os.path.join(download_dir, f"{paper_title}.pdf")
        paper.download_pdf(filename=file_path)

        return
    except Exception as e:
        print(f"Problem with: {paper_name} - Got exception: {e}")
        return

if __name__ == '__main__':
    main()



