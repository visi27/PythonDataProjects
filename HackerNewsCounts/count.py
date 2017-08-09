from read import load_data
import operator

data = load_data()

final_joined_headlines = ""
for headline in data["headline"]:
    final_joined_headlines += str(headline).lower()
    final_joined_headlines == " "
    
words = final_joined_headlines.split(" ")

word_counts = {}

for word in words:
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1
        
sorted_d = sorted(word_counts.items(), key=operator.itemgetter(1), reverse=True)
print(sorted_d[:100
]) 