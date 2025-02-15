import pandas as pd
from scipy.stats import chisquare

# Define input file names
RAW_SUCCESS_WORDS_FILE = "success_words.csv"
RAW_FAILURE_WORDS_FILE = "failure_words.csv"

# Define cleaned file names
SUCCESS_WORDS_FILE = "cleaned_success_words.csv"
FAILURE_WORDS_FILE = "cleaned_failure_words.csv"

# Define stopwords (common words we want to ignore)
STOPWORDS = set([
    "the", "and", "to", "of", "a", "in", "for", "on", "is", "with", "that", "this",
    "be", "an", "from", "which", "or", "not", "but", "can", "if", "are", "then", "so",
    "did", "has", "have", "had", "will", "shall", "would", "should", "may", "might",
    "she", "they", "them", "his", "her", "their", "its", "our", "you", "your", "i",
    "theirs", "who", "whom", "whose", "how", "when", "where", "why", "what", "which",
    "therefore", "however", "moreover", "hence", "nevertheless", "yet", "also", "either",
    "very", "just", "still", "even", "only", "own", "all", "some", "many", "most",
    "no", "none", "each", "one", "two", "three", "first", "second", "third", "other"
])

### **STEP 1: Load raw word frequency data**
try:
    success_df = pd.read_csv(RAW_SUCCESS_WORDS_FILE)
    failure_df = pd.read_csv(RAW_FAILURE_WORDS_FILE)
except FileNotFoundError:
    print(f"❌ Error: One or both input files are missing. Ensure {RAW_SUCCESS_WORDS_FILE} and {RAW_FAILURE_WORDS_FILE} exist.")
    exit()

### **STEP 2: Remove stopwords from both datasets**
success_df = success_df[~success_df["Word"].str.lower().isin(STOPWORDS)]
failure_df = failure_df[~failure_df["Word"].str.lower().isin(STOPWORDS)]

### **STEP 3: Save cleaned word frequency data**
success_df.to_csv(SUCCESS_WORDS_FILE, index=False)
failure_df.to_csv(FAILURE_WORDS_FILE, index=False)
print(f"✅ Cleaned word lists saved as {SUCCESS_WORDS_FILE} and {FAILURE_WORDS_FILE}")

### **STEP 4: Merge datasets, filling missing words with count 0**
merged_df = pd.merge(success_df, failure_df, on="Word", how="outer", suffixes=("_success", "_failure")).fillna(0)

# Convert counts to integers
merged_df["Count_success"] = merged_df["Count_success"].astype(int)
merged_df["Count_failure"] = merged_df["Count_failure"].astype(int)

# Compute probabilities (normalize word frequencies)
merged_df["Prob_success"] = merged_df["Count_success"] / merged_df["Count_success"].sum()
merged_df["Prob_failure"] = merged_df["Count_failure"] / merged_df["Count_failure"].sum()

# Compute Chi-Square test for significant differences
observed = merged_df[["Count_success", "Count_failure"]].to_numpy()
# Convert raw counts to proportions (normalize so sums match)
observed[:, 0] = observed[:, 0] / observed[:, 0].sum()
observed[:, 1] = observed[:, 1] / observed[:, 1].sum()

# Perform the chi-square test
chisq_stat, p_value = chisquare(observed[:, 0], observed[:, 1])

# Sort by largest difference in probability
merged_df["Diff"] = abs(merged_df["Prob_success"] - merged_df["Prob_failure"])
merged_df_sorted = merged_df.sort_values(by="Diff", ascending=False)

# Print top 150 differing words
print("\n🔍 **Top 150 Words with the Largest Differences** between Success & Failure:")
print(merged_df_sorted[["Word", "Prob_success", "Prob_failure", "Diff"]].head(150))

print(f"\n📊 **Chi-Square Test Result**:")
print(f"- Statistic = {chisq_stat:.4f}")
print(f"- p-value = {p_value:.4f}")

# Save to CSV for deeper analysis
OUTPUT_FILE = "word_comparison_filtered.csv"
merged_df_sorted.to_csv(OUTPUT_FILE, index=False)
print(f"\n✅ Comparison saved to {OUTPUT_FILE}")
