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
    if N_PROCESSES <= 1:
        for pdf_path in tqdm(pdf_paths):
            summarize_pdf(pdf_path)
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

        prompt = (f"This is a paper publish in MICCAI 2023. We are giving each paper some AI technology tags, if its relevent."
                  f" (For example a paper that solve segmentation problem will have the tag 'segmentation')\n"
                  f"I will give u the list of tags to choose from, you can (and should) select more than one tag for the paper. Here are the tags:\n"
                  f"1. Segmentation\n"
                  f"2. Registration\n"
                  f"3. Generative AI\n"
                  f"4. Explainable AI\n"
                  f"5. Diffusion Models\n"
                  f"6. Unique Architecture\n"
                  f"7. Text-Image Fusion\n"
                  f"8. Multimodality\n"
                  f"9. Self-Supervised Learning\n"
                  f"10. Few-Shot Learning\n"
                  f"11. Zero-Shot Learning\n"
                  f"12. Transfer Learning\n"
                  f"13. Domain Adaptation\n"
                  f"14. Federated Learning\n"
                  f"15. Contrastive Learning\n"
                  f"16. Reinforcement Learning\n"
                  f"17. Graph Neural Networks\n"
                  f"18. Transformers\n"
                  f"19. Vision Transformers (ViT)\n"
                  f"20. Large Language Models(LLMs)\n"
                  f"21. Prompt Engineering\n"
                  f"22. Neural Architecture Search\n"
                  f"23. Optimization Techniques\n"
                  f"24. Neural Style Transfer\n"
                  f"25. Knowledge Distillation\n"
                  f"26. Edge AI\n"
                  f"27. Tiny ML\n"
                  f"28. Autonomous Agents\n"
                  f"29. Active Learning\n"
                  f"30. Semi-Supervised Learning\n"
                  f"31. Clustering Algorithms\n"
                  f"32. Metric Learning\n"
                  f"33. Anomaly Detection\n"
                  f"34. Synthetic Data Generation\n"
                  f"35. Unsupervised Learning\n"
                  f"36. Contrastive Divergence\n"
                  f"37. Adversarial Robustness\n"
                  f"38. Hybrid Models(e.g., Neural + Symbolic)\n"
                  f"39. Bayesian Neural Networks\n"
                  f"40. Probabilistic Models\n"
                  f"41. Sparse Representations\n"
                  f"42. Attention Mechanisms\n"
                  f"43. Temporal Sequence Modeling\n"
                  f"44. Recurrent Neural Networks(RNNs)\n"
                  f"45. Long Short-Term Memory Networks(LSTMs)\n"
                  f"46. Graph Embeddings\n"
                  f"47. Multi-Agent Systems\n"
                  f"48. Evolutionary Algorithms\n"
                  f"49. Generative Adversarial Networks(GANs)\n"
                  f"50. Diffusion Probabilistic Models\n"
                  f"51. Hyperparameter Tuning\n"
                  f"52. AI for Edge Devices\n"
                  f"53. RLHF (Reinforcement Learning with Human Feedback)\n"
                  f"54. Optimization-based Meta-Learning\n"
                  f"55. Continual Learning\n"
                  f"56. Catastrophic Forgetting\n"
                  f"57. Neural ODEs (Ordinary Differential Equations)\n"
                  f"58. Energy-Based Models\n"
                  f"59. Sparse Neural Networks\n"
                  f"60. AI Interpretability\n"
                  f"\n\n"
                  f"This is automatic system, your answer should be in this format tag_tag_tag. for example: 4_15_37."
                  f"DO NOT WRITE ANYTHING ELSE, JUST THE TAGS SEPARATED BY UNDERSCORES.\n"
                  f"\n\nPlease select the tags that best describe the paper, here is the paper:\n\n"
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
        txt_path = pdf_path.replace(".pdf", ".txt")
        with open(txt_path, "w") as f:
            f.write(answer)
    except Exception as e:
        print(f"Problem with: {pdf_path} - Got exception: {e}")
        return


if __name__ == '__main__':
    main()