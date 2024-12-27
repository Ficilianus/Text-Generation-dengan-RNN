import re
import numpy as np
from nltk.tokenize import word_tokenize
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

# === Preprocessing Data ===
# Baca file XML sebagai string
xml_file_path = r"C:\\Users\\LEGION\\OneDrive\\Documents\\1. kuliah\\NLP\\UAS\\xml\\export-xml-2015-12-19.xml"
with open(xml_file_path, 'r', encoding='utf-8') as file:
    xml_content = file.read()

# Ganti semua tanda baca dengan spasi
text_with_spaces = re.sub(r'[^\w\s]', ' ', xml_content)

# Hapus spasi yang berlebihan
cleaned_text = re.sub(r'\s+', ' ', text_with_spaces).strip()

# Tokenisasi
teks = word_tokenize(cleaned_text)

# Gabungkan kembali menjadi string
processed_text = ' '.join(teks)

# Tokenizer untuk memetakan kata menjadi angka
tokenizer = Tokenizer()
tokenizer.fit_on_texts([processed_text])
total_words = len(tokenizer.word_index) + 1

# Buat data pelatihan
input_sequences = []
for line in processed_text.split('. '):  # Pisahkan berdasarkan kalimat (opsional)
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

# Padding sequences
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre')

# Pisahkan fitur (X) dan label (y)
X, y = input_sequences[:, :-1], input_sequences[:, -1]
y = to_categorical(y, num_classes=total_words)

# === Bangun Arsitektur RNN ===
model = Sequential()
model.add(Embedding(total_words, 100, input_length=max_sequence_len-1))  # Embedding Layer
model.add(LSTM(150, return_sequences=True))  # LSTM Layer 1
model.add(LSTM(100))  # LSTM Layer 2
model.add(Dense(total_words, activation='softmax'))  # Output Layer

# Kompilasi model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# === Latih Model ===
print("Training model...")
history = model.fit(X, y, epochs=50, verbose=1)

# === Menghasilkan Teks Baru ===
def generate_text(seed_text, next_words, max_sequence_len):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
        predicted = model.predict(token_list, verbose=0)
        output_word = tokenizer.index_word[np.argmax(predicted)]
        seed_text += " " + output_word
    return seed_text

# Contoh penggunaan
seed_text = "Ini adalah"
next_words = 20  # Jumlah kata yang ingin dihasilkan
print("Generated Text:")
print(generate_text(seed_text, next_words, max_sequence_len))
