import os
import xml.etree.ElementTree as ET

# Path file XML
xml_file_path = r"C:\Users\LEGION\OneDrive\Documents\1. kuliah\NLP\UAS\xml\export-xml-2015-12-19.xml"

# Cek apakah file XML ada
if os.path.exists(xml_file_path):
    try:
        # Parse file XML
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Menampilkan isi file XML
        print("Isi file XML:")
        for elem in root.iter():
            print(f"{elem.tag}: {elem.text.strip() if elem.text else 'N/A'}")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
else:
    print(f"File {xml_file_path} tidak ditemukan.")
