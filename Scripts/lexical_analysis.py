import pandas as pd
import spacy
from collections import Counter
import textstat
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('words')

# Load spaCy's small English model
nlp = spacy.load('en_core_web_sm')

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')

# Function to calculate average sentence length
def avg_sentence_length(text):
    sentences = sent_tokenize(text)
    if len(sentences) == 0:
        return 0
    total_words = sum(len(word_tokenize(sentence)) for sentence in sentences)
    return total_words / len(sentences)

# Function to calculate type-token ratio (TTR)
def type_token_ratio(text):
    tokens = word_tokenize(text)
    if len(tokens) == 0:
        return 0
    return len(set(tokens)) / len(tokens)

# Function to calculate lexical sophistication using word frequency
def lexical_sophistication(text):
    tokens = word_tokenize(text)
    if len(tokens) == 0:
        return 0
    freq_dist = nltk.FreqDist(tokens)
    common_words = set(nltk.corpus.words.words())
    rare_words = [word for word in tokens if word not in common_words]
    if len(tokens) == 0:
        return 0
    return len(rare_words) / len(tokens)

# Function to calculate readability scores
def readability_scores(text):
    return {
        'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
        'gunning_fog_index': textstat.gunning_fog(text),
        'smog_index': textstat.smog_index(text),
        'automated_readability_index': textstat.automated_readability_index(text)
    }

# Sample DataFrame
data = {
    'label': [0, 1],  # 0 for human, 1 for LLM
    'text': [
        "This is a sample text written by a human. It has multiple sentences.",
        "This text is generated by a language model. It also has multiple sentences."
    ]
}

df = pd.read_csv("/Users/thorkildkappel/Desktop/4. sem/Soc cult-paper/archive/train_v4_drcat_03.csv")

# Perform the analysis


results = []

counter = 0

for index, row in df.iterrows():
    text = row['text']
    result = {
        'label': row['label'],
        'avg_sentence_length': avg_sentence_length(text),
        'type_token_ratio': type_token_ratio(text)#,
        #'lexical_sophistication': lexical_sophistication(text),
    }
    result.update(readability_scores(text))
    results.append(result)
    counter += 1
    print(round(counter/len(df["text"]), 4), end='\r')

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Display the results
print(results_df)

results_df.to_csv('/Users/thorkildkappel/Desktop/4. sem/Soc cult-paper/archive/results_df.csv')