import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Menyembunyikan pesan info dan warning
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from preprocessing import preprocess_text  # Import dari file pertama

# Bangun model RNN
def build_rnn(vocab_size, sequence_length):
    model = Sequential([
        Embedding(input_dim=vocab_size, output_dim=50, input_length=sequence_length-1),
        SimpleRNN(150, return_sequences=False),
        Dense(vocab_size, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Fungsi untuk menghasilkan teks
def generate_text(seed_text, num_words, model, tokenizer, sequence_length):
    for _ in range(num_words):
        # Tokenisasi seed text
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=sequence_length-1, padding='pre')
        
        # Prediksi kata berikutnya
        predicted_probs = model.predict(token_list, verbose=0)
        predicted = np.argmax(predicted_probs, axis=-1)
        
        # Cari kata berdasarkan indeks
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        
        # Tambahkan kata ke seed text
        seed_text += " " + output_word
    return seed_text

# Main training dan text generation
if __name__ == "__main__":
    xml_path = "C:\\Users\\LEGION\\OneDrive\\Documents\\1. kuliah\\NLP\\UAS\\xml\\export-xml-2015-12-05.xml"
    sequence_length = 5

    # Preprocess data
    X, y, vocab_size, tokenizer = preprocess_text(xml_path, sequence_length)

    # Build and train model
    model = build_rnn(vocab_size, sequence_length)
    model.summary()
    model.fit(X, y, epochs=20, batch_size=64)

    # Generate text
    seed_text = "hasil\n"
    
    generated_text = generate_text(seed_text, 20, model, tokenizer, sequence_length)
    print(generated_text)
