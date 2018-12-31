#import thulac #for segmentation

#Natural Lanugage Processing
import jieba
import snownlp

#Data Processing
import numpy as np
from sklearn.linear_model import LinearRegression

#File extracting
import os
import re

#Graph plotting
import matplotlib.pyplot as plt

#Others
import collections


def extract_text(file_dir):
    with open(file_dir,  "r", encoding="utf-8") as f:
        text = f.read()
        f.close()
    return text

def extract_csv(file_dir):
    with open(file_dir, newline="") as f:
        data = np.genfromtxt(file_dir, delimiter=",", names=["Date", "Values"])
        f.close()
    return data

def write_file(text, filename):
    text.encode("utf-8")
    with open("./txt/{}_2.txt".format(filename.replace(".txt", "")), "w", encoding="utf-8") as f:
        f.write(text)
    f.close()

def sentiment_analysis_snownlp(filename):
    return None

def word_frequency(text):
    words = [word for word in jieba.cut(text, cut_all=False) if len(word) >= 2]
    c = collections.Counter(words)

    return c.most_common(10)

def remove_punctuation(text):
    rule = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    text = rule.sub('',text)
    return text

    
def main():

    #Frequency Analysis
    #return the most common 10 words' sentiment
    '''
    directory = os.fsencode("pbocmonetary")
    avg_sent = []
    for file in sorted(os.listdir(directory)):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            file_dir = "pbocmonetary\{}".format(filename)
            text = extract_text(file_dir)
            text_cleaned = remove_punctuation(text)
            text_cut = jieba.cut(text_cleaned, cut_all=False)
            text = " ".join(text_cut)
            write_file(text, filename)
            word_freq = word_frequency(text)
            total_word_sent = 0
            n = 0
            for word in word_freq:
                word_sent = snownlp.SnowNLP(word[0]).sentiments
                total_word_sent += word_sent
                n += 1
            avg_sentiment = total_word_sent / n
            avg_sent.append(avg_sentiment)

    avg_sent = np.array(avg_sent)
    avg_sent.tofile("avg_sent.csv", sep=",", format="%0.5f")
    '''
    #Read avg_sent
    avg_sent = np.genfromtxt("avg_sent.csv", delimiter=",")

    #Regression
    #avg_sent = avg_sent[-2:]
    directory = os.fsencode("csv")
    for file in sorted(os.listdir(directory)):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            file_dir = "csv\{}".format(filename)
            datas = extract_csv(file_dir)

            data_2 = datas["Values"]
            data_2 = data_2[1:]

            avg_sent = avg_sent.reshape(-1,1)
            data_2 = data_2.reshape(-1,1)
            reg = LinearRegression()
            reg.fit(avg_sent, data_2)

    #plot graph
    plt.style.use("ggplot")
    plt.scatter(avg_sent, data_2, color="b")
    plt.plot(avg_sent, reg.predict(avg_sent), color="red", linewidth=3)
    plt.ylabel("GDP")
    plt.xlabel("Sentiment")
    print(reg.intercept_)
    print(reg.coef_)
    print(reg.score(avg_sent, data_2))
    plt.show()

if __name__ == "__main__":
    main()
