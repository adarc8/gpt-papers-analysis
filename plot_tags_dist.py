import glob
from collections import defaultdict

from matplotlib import pyplot as plt

from constants import TAG_TO_STR


txt_files = glob.glob(r"C:\Users\adarc\Downloads\micai2023\papers\*.txt")
copy_txt_files = glob.glob(r"C:\Users\adarc\Downloads\micai2023\papers_copy\*.txt")

def main():
    tag_counter = defaultdict(int)
    for idx, (txt_file, copy_txt_file) in enumerate(zip(txt_files, copy_txt_files)):
        pred1 = sorted([int(tag) for tag in read_gpt_answer(txt_file).split('_')])
        pred2 = sorted([int(tag) for tag in read_gpt_answer(copy_txt_file).split('_')])
        pred = sorted(list(set(pred1) & set(pred2)))
        for tag in pred:
            tag_counter[tag] += 1

    # sort from most common to least common
    tag_counter = dict(sorted(tag_counter.items(), key=lambda x: x[1], reverse=True))
    tag_counter = {TAG_TO_STR[tag]: count for tag, count in tag_counter.items()}
    # Extract keys and values for plotting
    tags = list(tag_counter.keys())
    counts = list(tag_counter.values())

    # Create the bar plot
    plt.figure(figsize=(14, 10))  # Adjust figure size
    plt.barh(tags, counts, color='skyblue')
    plt.xlabel('Count', fontsize=14)  # Larger font size
    plt.ylabel('Tags', fontsize=14)  # Larger font size
    plt.title('Tag Counter Plot', fontsize=18)  # Larger font size
    plt.tick_params(axis='y', labelsize=12)  # Adjust y-axis label font size
    plt.tick_params(axis='x', labelsize=12)  # Adjust x-axis label font size
    plt.gca().invert_yaxis()  # To display the highest count at the top
    plt.tight_layout()

    # Display the plot
    plt.show()

    print(tags)






def read_gpt_answer(txt_file):
    with open(txt_file, "r") as f:
        text = f.read()
    # remove chars that are not numnber or _
    text = "".join([c for c in text if c.isdigit() or c == "_"])
    return text

if __name__ == '__main__':
    main()
