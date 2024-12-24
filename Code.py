
import re
import nltk

from nltk.tokenize import word_tokenize 
nltk.download('punkt')
nltk.download('punkt_tab')


# Path ke file XML
xml_file_path = r"C:\Users\LEGION\OneDrive\Documents\1. kuliah\NLP\UAS\xml\export-xml-2015-12-19.xml"

# Baca file XML sebagai string
with open(xml_file_path, 'r', encoding='utf-8') as file:
    xml_content = file.read()

# Ganti semua tanda baca dengan spasi
text_with_spaces = re.sub(r'[^\w\s]', ' ', xml_content)

# Hapus spasi yang berlebihan (spasi yang berlebih di maksdkan adalah spasi yang lebih dari satu)
cleaned_text = re.sub(r'\s+', ' ', text_with_spaces).strip()

 


# Tokenisasi menggunakan NLTK
tokens = word_tokenize(cleaned_text)

# Cetak hasil tokenisasi
print(tokens)
