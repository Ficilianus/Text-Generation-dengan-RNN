import re
import nltk
from collections import Counter, defaultdict
import pandas as pd
from nltk.util import bigrams
from nltk.tokenize import word_tokenize
import math
nltk.download('punkt')

# Path ke file XML
xml_file_path = r"C:\\Users\\LEGION\\OneDrive\\Documents\\1. kuliah\\NLP\\UAS\\xml\\export-xml-2015-12-19.xml"

# Baca file XML sebagai string
with open(xml_file_path, 'r', encoding='utf-8') as file:
    xml_content = file.read()

# Ganti semua tanda baca dengan spasi
text_with_spaces = re.sub(r'[^\w\s]', ' ', xml_content)

# Hapus spasi yang berlebihan
cleaned_text = re.sub(r'\s+', ' ', text_with_spaces).strip()

# Tokenisasi
tokens = word_tokenize(cleaned_text)

# Total kata
total_words = len(tokens)

# Hitung frekuensi Unigram
unigram_counts = Counter(tokens)

# Probabilitas Unigram
unigram_prob = {word: count / total_words for word, count in unigram_counts.items()}

# Bigram
bigram_counts = Counter(bigrams(tokens))

# Probabilitas Bigram
bigram_prob = defaultdict(float)
for (w1, w2), count in bigram_counts.items():
    bigram_prob[(w1, w2)] = count / unigram_counts[w1]

# Fungsi menghitung perplexity untuk unigram
def calculate_unigram_perplexity(tokens, unigram_prob):
    N = len(tokens)
    log_prob_sum = 0

    for word in tokens:
        prob = unigram_prob.get(word, 1e-10)  # Gunakan probabilitas kecil jika kata tidak ada
        log_prob_sum += math.log2(prob)

    perplexity = 2 ** (-log_prob_sum / N)
    return perplexity

# Fungsi menghitung perplexity untuk bigram
def calculate_bigram_perplexity(tokens, bigram_prob, unigram_counts):
    N = len(tokens)
    log_prob_sum = 0

    for i in range(1, N):  # Mulai dari token kedua karena bigram
        w1, w2 = tokens[i - 1], tokens[i]
        prob = bigram_prob.get((w1, w2), 1e-10)  # Gunakan probabilitas kecil jika bigram tidak ada
        log_prob_sum += math.log2(prob)

    perplexity = 2 ** (-log_prob_sum / N)
    return perplexity

# Perhitungan perplexity untuk data saat ini
unigram_perplexity = calculate_unigram_perplexity(tokens, unigram_prob)
bigram_perplexity = calculate_bigram_perplexity(tokens, bigram_prob, unigram_counts)

# Siapkan data untuk file Excel
max_len = max(len(unigram_prob), len(bigram_prob))  # Panjang maksimum
unigram_keys = list(unigram_prob.keys())
unigram_values = list(unigram_prob.values())
bigram_keys = [f"{w1} {w2}" for w1, w2 in bigram_prob.keys()]
bigram_values = list(bigram_prob.values())

# Tambahkan padding untuk menyamakan panjang
unigram_keys += [''] * (max_len - len(unigram_keys))
unigram_values += [None] * (max_len - len(unigram_values))
bigram_keys += [''] * (max_len - len(bigram_keys))
bigram_values += [None] * (max_len - len(bigram_values))
perplexity_unigram_col = [unigram_perplexity] + [None] * (max_len - 1)
perplexity_bigram_col = [bigram_perplexity] + [None] * (max_len - 1)

# Gabungkan ke dalam satu DataFrame
combined_df = pd.DataFrame({
    'Unigram': unigram_keys,
    'Unigram Probability': unigram_values,
    'Bigram': bigram_keys,
    'Bigram Probability': bigram_values,
    'Unigram Perplexity': perplexity_unigram_col,
    'Bigram Perplexity': perplexity_bigram_col
})

# Simpan ke Excel
output_file = r"hasil.xlsx"
combined_df.to_excel(output_file, sheet_name='Results', index=False)

# Cetak sebagian hasil untuk unigram dan bigram
print("Unigram dan Probabilitas (50 data):")
print(list(unigram_prob.items())[:50])

print("\nBigram dan Probabilitas (50 data):")
print(list(bigram_prob.items())[:50])

# Cetak perplexity
print("\nPerplexity Unigram:", unigram_perplexity)
print("Perplexity Bigram:", bigram_perplexity)

print(f"\nHasil probabilitas dan perplexity disimpan ke file {output_file}")
