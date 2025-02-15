import pandas as pd
from collections import Counter
import re

# Define CSV filenames
SUCCESS_CSV = "processed_success.csv"
FAILURE_CSV = "processed_failure.csv"
SUCCESS_WORDS_FILE = "success_words.csv"
FAILURE_WORDS_FILE = "failure_words.csv"

# Function to clean and tokenize text (exclude words with numbers)
def clean_and_tokenize(text):
    if pd.isna(text):  # Handle NaN values
        return []
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())  # Only allow alphabetic words
    return words

# Function to get word frequencies from a DataFrame column
def get_word_frequencies(df, column_name, max_words=200):
    word_counter = Counter()
    if column_name in df.columns:
        for text in df[column_name].dropna():  # Remove NaN values
            word_counter.update(clean_and_tokenize(text))
    return word_counter.most_common(max_words)

# Load CSV files
success_df = pd.read_csv(SUCCESS_CSV)
failure_df = pd.read_csv(FAILURE_CSV)

# Process word frequencies
success_words = get_word_frequencies(success_df, "Reflection") + get_word_frequencies(success_df, "Research Plan")
failure_words = get_word_frequencies(failure_df, "Reflection") + get_word_frequencies(failure_df, "Research Plan")

# Convert to DataFrame for saving
success_df_words = pd.DataFrame(success_words, columns=["Word", "Count"])
failure_df_words = pd.DataFrame(failure_words, columns=["Word", "Count"])

# Save word counts to CSV
success_df_words.to_csv(SUCCESS_WORDS_FILE, index=False)
failure_df_words.to_csv(FAILURE_WORDS_FILE, index=False)

print(f"✅ Word frequency analysis saved!\n📂 Success words: {SUCCESS_WORDS_FILE}\n📂 Failure words: {FAILURE_WORDS_FILE}")
