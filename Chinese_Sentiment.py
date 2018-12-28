import jieba
import requests
import bs4
import wordcloud
import matplotlib.pyplot as plt
import snownlp


def extract_text(url):
	page_source = requests.get(url).content
	bs_source = bs4.BeautifulSoup(page_source, features="lxml")
	report_text = bs_source.find_all("p")

	text = ""

	for p in report_text:
		text += p.get_text()
		text += "\n"

	return text

def word_frequency(text):
	import collections

	words = [word for word in jieba.cut(text, cut_all=True) if len(word) >= 2]

	c = collections.Counter(words)
	for word_freq in c.most_common(30):
		word, freq = word_freq
		print(word, freq)

	return c

def word_cloud(text):
	font = "C:\Windows\Fonts\mingliu.ttc"
	word_image = wordcloud.WordCloud(background_color="white", width=1000, height=860, margin=2, font_path=font).\
		generate_from_frequencies(text)
	plt.imshow(word_image)
	plt.axis("off")
	plt.show()

url = 'http://www.gov.cn/guowuyuan/2016-04/13/content_5063747.htm'

#text = extract_text(url)
with open("PBoC.txt","r",encoding="utf-8") as f:
	text = f.read()
	text_nlp = snownlp.SnowNLP(text)

sum = 0
for i in range(0, 570):
	temp = text_nlp.sentences[i]
	print("Sentence: {} ; Sentiment: {}".format(temp, snownlp.SnowNLP(temp).sentiments))
	sum += snownlp.SnowNLP(temp).sentiments

print("The overall sentiment of this text is {}".format(text_nlp.sentiments))
print("The averaged overall sentiment of this text is {}".format(sum/570))
word_cloud(word_frequency(text))