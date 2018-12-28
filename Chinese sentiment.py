#import thulac #for segmentation

import jieba
import snownlp
import collections
import re
import os

def extract_text(file_dir):
    with open(file_dir,  "r", encoding="utf-8") as f:
        text = f.read()
    f.close()
    return text

def write_file(text):
    text.encode("utf-8")
    with open("./txt/PBoC_Cut.txt", "w", encoding="utf-8") as f:
        f.write(text)
    f.close()

def sentiment_analysis_snownlp(text):
    text_nlp = snownlp.SnowNLP(text)
    i = 0
    while i < 100:
        line = text_nlp.sentences[i]
        print("Sentence: ", line)
        print("Sentiment: ", snownlp.SnowNLP(line).sentiments)
        i += 1

def word_frequency(text):
    words = [word for word in jieba.cut(text, cut_all=False) if len(word) >= 2]
    c = collections.Counter(words)

    return c.most_common(1)

def remove_punctuation(text):
    rule = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    text = rule.sub('',text)
    return text

    
def main():
    #define file directory
    file_dir = "txt\PBoC.txt"
    
    #extract text from file
    text = extract_text(file_dir)

    #Text Cleaning
    '''
    text_cleaned = remove_punctuation(text)
    text_cut = jieba.cut(text_cleaned, cut_all=False)
    text = " ".join(text_cut)
    write_file(text)
    '''
    #Analysis
    #text_cleaned_dir = "txt/PBoC_Cut.txt"
    #sentiment_analysis_snownlp(text)

    #Frequency Analysus
    directory = os.fsencode("pbocmonetary")

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            file_dir = "pbocmonetary\{}".format(filename)
            text = extract_text(file_dir)
            text_cleaned = remove_punctuation(text)
            text_cut = jieba.cut(text_cleaned, cut_all=False)
            text = " ".join(text_cut)
            print(filename, ":")
            print(word_frequency(text))
            print("\n")

if __name__ == "__main__":
    main()
