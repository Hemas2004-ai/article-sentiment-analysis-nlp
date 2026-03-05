import os
import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

nltk.download('punkt')

articles_folder = "articles"
stopwords_folder = "StopWords-20260302T191240Z-3-001/StopWords"
dictionary_folder = "MasterDictionary-20260302T191239Z-3-001/MasterDictionary"

df = pd.read_excel("Input.xlsx")

# -----------------------
# LOAD STOPWORDS
# -----------------------
stop_words = set()

for file in os.listdir(stopwords_folder):
    file_path = os.path.join(stopwords_folder, file)

    with open(file_path, 'r', encoding='latin-1') as f:
        for line in f:
            stop_words.add(line.strip().lower())

# -----------------------
# LOAD POSITIVE/NEGATIVE WORDS
# -----------------------
positive_words = set()
negative_words = set()

with open(os.path.join(dictionary_folder, "positive-words.txt"), encoding='latin-1') as f:
    for line in f:
        positive_words.add(line.strip().lower())

with open(os.path.join(dictionary_folder, "negative-words.txt"), encoding='latin-1') as f:
    for line in f:
        negative_words.add(line.strip().lower())

# -----------------------
# SYLLABLE FUNCTION
# -----------------------
def count_syllables(word):

    vowels = "aeiou"
    word = word.lower()
    count = 0

    for i in range(len(word)):
        if word[i] in vowels:
            if i == 0 or word[i-1] not in vowels:
                count += 1

    if word.endswith(("es", "ed")):
        count -= 1

    if count <= 0:
        count = 1

    return count

results = []

for index, row in df.iterrows():

    url_id = row["URL_ID"]
    url = row["URL"]

    file_path = os.path.join(articles_folder, f"{url_id}.txt")

    if not os.path.exists(file_path):
        print(f"{url_id} article missing")
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    words = word_tokenize(text.lower())
    sentences = sent_tokenize(text)

    clean_words = [w for w in words if w.isalpha() and w not in stop_words]

    word_count = len(clean_words)
    sentence_count = len(sentences)

    positive_score = sum(1 for w in clean_words if w in positive_words)
    negative_score = sum(1 for w in clean_words if w in negative_words)

    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

    subjectivity_score = (positive_score + negative_score) / ((word_count) + 0.000001)

    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0

    complex_words = [w for w in clean_words if count_syllables(w) > 2]
    complex_word_count = len(complex_words)

    percentage_complex_words = complex_word_count / word_count if word_count > 0 else 0

    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0

    syllable_per_word = sum(count_syllables(w) for w in clean_words) / word_count if word_count > 0 else 0

    pronouns = re.findall(r'\b(I|we|my|ours|us)\b', text, re.I)
    personal_pronouns = len(pronouns)

    avg_word_length = sum(len(w) for w in clean_words) / word_count if word_count > 0 else 0

    results.append({
        "URL_ID": url_id,
        "URL": url,
        "POSITIVE SCORE": positive_score,
        "NEGATIVE SCORE": negative_score,
        "POLARITY SCORE": polarity_score,
        "SUBJECTIVITY SCORE": subjectivity_score,
        "AVG SENTENCE LENGTH": avg_sentence_length,
        "PERCENTAGE OF COMPLEX WORDS": percentage_complex_words,
        "FOG INDEX": fog_index,
        "AVG NUMBER OF WORDS PER SENTENCE": avg_words_per_sentence,
        "COMPLEX WORD COUNT": complex_word_count,
        "WORD COUNT": word_count,
        "SYLLABLE PER WORD": syllable_per_word,
        "PERSONAL PRONOUNS": personal_pronouns,
        "AVG WORD LENGTH": avg_word_length
    })

output = pd.DataFrame(results)

output.to_excel("final_output.xlsx", index=False)

print("Final analysis completed!")