# Nimar PDF  and Merger Software
## An open source software to convert documents to pdf and merge them.
## निमाड़ पीडीएफ कंवर्टल एवं मर्ज साॅफ़टवेयर 

<div align="center">

  <img width="350 " alt="image" src="https://github.com/user-attachments/assets/1b18bdb8-9d8e-4f09-bd67-a7a166361a97" />

</div>

A simple utility to converts documents, spreadsheet, text and images into pdf individual or merged in single file. Supports devanagari hindi script. This is inspired by A-Pdf Merger software of old times with increased supported file formats.\

यह एक आसान यूटिलिटी है जो डॉक्यूमेंट, स्प्रेडशीट, टेक्स्ट और इमेज को अलग-अलग या एक ही फ़ाइल में मर्ज करके PDF में बदलती है। यह देवनागरी हिंदी स्क्रिप्ट को सपोर्ट करती है।

## Features
- No nonsense converter and merger software runs locally on your machine
- Convert multiple document formats to PDF
- Support for Office documents, text files, images and web formats
- Merge multiple PDF files into single document or create individual pdf
- Devanagari font support for Hindi text
- Cross-platform support (Windows, macOS, Linux)
- 
## विशेषताएं
- बिना किसी झंझट वाला कन्वर्टर और मर्जर सॉफ्टवेयर जो आपके कंप्यूटर पर लोकल रूप से चलता है
- कई डॉक्यूमेंट फॉर्मेट को PDF में कन्वर्ट करें
- ऑफिस डॉक्यूमेंट, टेक्स्ट फ़ाइल, इमेज और वेब फॉर्मेट के लिए सपोर्ट है
- कई PDF फ़ाइलों को एक डॉक्यूमेंट में मर्ज करें या अलग-अलग PDF बनाएं
- हिंदी टेक्स्ट के लिए देवनागरी फॉन्ट सपोर्ट करता है
- क्रॉस-प्लेटफ़ॉर्म सपोर्ट (Windows, macOS, Linux) पर चलता है

## Supported Formats
- Office: .doc, .docx, .xls, .xlsx, .ppt, .pptx, .odt, .ods, .odp
- Documents: .txt, .csv, .xml, .md, .html
- PDF: .pdf (for merging)
## How to run
### Executable
Executable files for Windows and Linux are supplied in Releases. To use them download it and run the software.

### Build from source :
The software is created in Python so you can easily build it from source. 
1. First create a local copy using
  `git clone https://github.com/danishdtp/nimarPDFConverter.git `
2. Build Requirements
- Python 3.8+
- LibreOffice (for Office document conversion)
- See requirements.txt for Python dependencies

3. Run main file 
```bash
pip install -r requirements.txt
python main.py
```

## Usage
1. Run the application
2. Upload files using the file browser
3. Arrange files using up/down buttons
4. Choose conversion option (individual/merged)
5. Click convert and save location
## Screenshots
### Supports multiple file uploads of any extension.
You can convert a word document alongwith excel document and even merge them in one go.
<div align="center">
  <img width="350"  alt="image" src="https://github.com/user-attachments/assets/ff1a7760-d946-4325-9dc8-5ab8cd0fc85b" />
</div>

### Arrange files and convert individual or merge
Arrange files with up down arrow keys. You can either convert each file individually or merge it in one pdf file.\
<div align="center">
  <img width="350" alt="image" src="https://github.com/user-attachments/assets/a8c75bb3-e5a2-413b-8507-63ed54eecb0e" />
</div>

### Save with overwriting check
It checks if files overwrite and shows overwritten files. Use carefully when saving.\
<div align="center">

<img width="350" alt="image" src="https://github.com/user-attachments/assets/82440a4e-420f-4ae0-abe1-7bf1276e7bbc" />
</div>

## Project Status
The projects is created as a hobby and out of need to convert various documents into pdf.\
There were no good open source pdf converter merger available which ran locally on computer.\
The project is in early stage with barebones structure, however it works completely within it's domain. Future contributions are welcome. \
Needless to say this software comes with no warranty to work. 

## Created by 
Danish Khan,\
Junior Supply Officer, Khandwa\
The name is an homage to Nimar region of Madhya Pradesh, my workplace.
