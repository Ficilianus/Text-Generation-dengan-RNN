import re
from nltk.tokenize import word_tokenize
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from tensorflow.keras.utils import to_categorical

def preprocess_text(xml_file_path, sequence_length=5):
    # Baca file XML
    with open(xml_file_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()

    # Ganti semua tanda baca dengan spasi
    text_with_spaces = re.sub(r'[^\w\s]', ' ', xml_content)

    # Hapus spasi yang berlebihan
    cleaned_text = re.sub(r'\s+', ' ', text_with_spaces).strip()

    # Tokenisasi
    tokens = word_tokenize(cleaned_text)

    # Membatasi ukuran data untuk efisiensi (opsional)
    tokens = tokens[:10000]

    # Membuat tokenizer
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(tokens)

    # Konversi kata menjadi indeks
    sequences = tokenizer.texts_to_sequences(tokens)
    encoded_text = [item for sublist in sequences for item in sublist]  # Flatten

    # Buat urutan pelatihan
    input_sequences = []
    for i in range(sequence_length, len(encoded_text)):
        input_sequences.append(encoded_text[i-sequence_length:i])

    # Padding untuk memastikan panjang seragam
    input_sequences = pad_sequences(input_sequences, padding='pre')

    # Konversi ke array NumPy
    input_sequences = np.array(input_sequences)

    # Pisahkan input (X) dan target (y)
    X = input_sequences[:, :-1]
    y = input_sequences[:, -1]

    # One-hot encode target (y)
    y = to_categorical(y, num_classes=len(tokenizer.word_index) + 1)

    return X, y, len(tokenizer.word_index) + 1, tokenizer

# Contoh penggunaan (jalankan hanya saat debugging)
# program di jalankan pada file rnn_model.py karena kode ini sebagi contoh saja 
if __name__ == "__main__":
    xml_path = "C:\\Users\\LEGION\\OneDrive\\Documents\\1. kuliah\\NLP\\UAS\\xml\\export-xml-2015-12-05.xml"
    X, y, vocab_size, tokenizer = preprocess_text(xml_path)
    print(f"Vocabulary size: {vocab_size}, Number of samples: {len(X)}")
