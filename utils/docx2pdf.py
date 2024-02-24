import os
import win32com.client

def convert_to_pdf(file_path):
    wdFormatPDF = 17

    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return

    file_name, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension in [".doc", ".odt", ".rtf", ".docx", ".dotm", ".docm"]:
        try:
            print(file_name)
            word = win32com.client.Dispatch('Word.Application')
            word.Visible = False
            doc = word.Documents.Open(file_path)
            doc.SaveAs(file_name, FileFormat=wdFormatPDF)
            doc.Close()
            word.Quit()
            word.Visible = True
            print ('done')
            os.remove(file_path)
        except Exception as e:
            print(f'Could not open file {file_path}. Error: {e}')
    else:
        print(f"File {file_path} is not a Word document.")

# Usage
convert_to_pdf('../data/Robinson_Advisory.docx')