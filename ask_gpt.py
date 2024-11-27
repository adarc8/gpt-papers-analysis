import openai
from PyPDF2 import PdfReader
from openai import OpenAI
from tqdm import tqdm
import glob

from api_secrets import API_KEY

client = OpenAI(api_key=API_KEY)
N_PROCESSES = 1
MAX_CONTENT = 30000
#mini
MODEL = "gpt-4o-mini"


def main():
    # Example usage
    pdf_paths = glob.glob(r"C:\Users\adarc\Downloads\micai2023\papers\*.pdf")
    # pdf_paths = pdf_paths[:8]  # Limit to the first 10 papers for testing
    collector = {}
    if N_PROCESSES <= 1:
        for pdf_path in tqdm(pdf_paths):
            answer = summarize_pdf(pdf_path)
            collector[pdf_path] = answer

    else:
        from multiprocessing import Pool
        with Pool(N_PROCESSES) as p:
            p.map(summarize_pdf, pdf_paths)



def read_pdf(pdf_path):
    """
    Extract text from the PDF file.
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def summarize_pdf(pdf_path):
    """
    Read a PDF and summarize it in 4 words using ChatGPT.
    """
    try:
        # Read the content of the PDF
        pdf_content = read_pdf(pdf_path)
        pdf_content = pdf_content[:MAX_CONTENT]  # Limit to 1000 characters for faster processing

        prompt = (f"Im an AI researcher in medical field. Im intersted in Image-Text Fusion (models that receive image and text as an input)."
                  "I'm going to give u a"
                  f" lot of papers to read, and i want you to tag them yes or no if they are related to Image-Text Fusion. "
                  f"If a paper method doesnt talk about Image-Text Fusion, do not tag it."
                  f"This is automatic system, your answer should only be True or False (True if the paper is about Image-Text Fusion, False otherwise)."
                  f"DO NOT WRITE ANYTHING ELSE, JUST True or False.\n"
                  f"\n\nPhere is the first paper:\n\n"
                  f"{pdf_content}\n\n"
                  )

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content":
                    f"{prompt}",
                }
            ],
            model=MODEL,
        )

        answer = response.choices[0].message.content.strip()
        if answer != 'False':
            print(f"{answer=}__{pdf_path}")
        txt_path = pdf_path.replace(".pdf", ".txt")
        with open(txt_path, "w") as f:
            f.write(answer)
        return answer
    except Exception as e:
        print(f"Problem with: {pdf_path} - Got exception: {e}")
        return None


if __name__ == '__main__':
    main()