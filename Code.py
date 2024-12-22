
# baca 1 file xml dan tampilkam 
# import os
# import xml.etree.ElementTree as ET

# # Path file XML
# xml_file_path = r"C:\Users\LEGION\OneDrive\Documents\1. kuliah\NLP\UAS\xml\export-xml-2015-12-19.xml"

# # Cek apakah file XML ada
# if os.path.exists(xml_file_path):
#     try:
#         # Parse file XML
#         tree = ET.parse(xml_file_path)
#         root = tree.getroot()

#         # Menampilkan isi file XML
#         print("Isi file XML:")
#         for elem in root.iter():
#             print(f"{elem.tag}: {elem.text.strip() if elem.text else 'N/A'}")
#     except ET.ParseError as e:
#         print(f"Error parsing XML: {e}")
# else:
#     print(f"File {xml_file_path} tidak ditemukan.")


# baca semua file dan disimpn kedalam sebuah varibel
import os
import xml.etree.ElementTree as ET

# Folder tempat file XML disimpan
folder_path = r"C:\Users\LEGION\OneDrive\Documents\1. kuliah\NLP\UAS\xml"

# Variabel untuk menyimpan semua data
all_xml_data = {}

# Baca semua file di folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".xml"):  # Filter file XML saja
        file_path = os.path.join(folder_path, file_name)
        try:
            # Parse file XML
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Simpan isi file dalam dictionary
            file_data = {}
            for elem in root.iter():
                file_data[elem.tag] = elem.text.strip() if elem.text else None

            # Tambahkan ke all_xml_data dengan nama file sebagai kunci
            all_xml_data[file_name] = file_data
        except ET.ParseError as e:
            print(f"Error parsing {file_name}: {e}")

# Menampilkan hasil
print("Semua data XML:")
for file_name, data in all_xml_data.items():
    print(f"\nFile: {file_name}")
    print(data)
