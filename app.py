
import cv2, numpy as np, textwrap, os
import requests, PyPDF2, string
import tkinter as tk
from tkinter import messagebox

def extract_text_from_pdf(pdf_file='documents/TKMFullText.pdf', url="https://www.raio.org/TKMFullText.pdf"):
    # check if the pdf file exists otherwise download it
    
    if not os.path.exists(pdf_file):
        # from here https://realpython.com/python-requests/
        pdf = requests.get(url)
        
        # from here https://www.geeksforgeeks.org/working-with-pdf-files-in-python/
        with open(pdf_file, 'wb') as f:
            f.write(pdf.content)

    pdfFileObj = open(pdf_file, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    pageObj = pdfReader.pages[3]
    paragraphs = pageObj.extract_text().split('\n')
    print(len(paragraphs))

    print(string.punctuation)
    def is_punctuation(c): return c in string.punctuation
    def is_capital(c): return c.isupper()

    formatted = []

    paragraph = ""
    add_next = False
    for choice in paragraphs:
        print(choice)
        if add_next:
            formatted[-1] += " " + choice
            formatted[-1] = formatted[-1].replace("  ", " ")
            add_next = False
            print("<<< fixed >>>")
            continue
        
        add_next = False
        if not is_capital(choice[0]):
            print("<<< Merge with before >>>")
            formatted[-1] += " " + choice
        elif not is_punctuation(choice[-1]):
            print("<<< Merge with next >>>")
            formatted.append(choice)
            add_next = True
        else:
            formatted.append(choice)
            print("<<< Good choice >>>")
        print("_"*20)


    for paragraph in formatted:
        print(paragraph)
        print("_"*50)

    pdfFileObj.close()

    return formatted


def display_text_on_image(text):
    image_height = 800
    image_width = 1200

    # Create a blank white image
    image = np.ones((image_height, image_width, 3), dtype=np.uint8) * 255

    # Define font properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    font_thickness = 1
    font_color = (0, 0, 0)
    line_type = cv2.LINE_AA

    # Wrap the text to no more than 50 characters per line
    wrapped_text = textwrap.fill(text[0], width=90)

    # Split the wrapped text into lines
    lines = wrapped_text.split('\n')

    # Display each line of wrapped text on the image
    y_offset = 50
    for line in lines:
        cv2.putText(image, line, (50, y_offset), font, font_scale, font_color, font_thickness, line_type)
        y_offset += 40  # Adjust line spacing

    # Display the image
    cv2.imshow('PDF Text Display', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

class PDFViewer:
    def __init__(self, root, pdf_text):
        self.root = root
        self.pdf_text = pdf_text
        self.current_page = 2
        self.lines_per_page = 40

    def display_page(self):
        page_text = self.pdf_text[self.current_page * self.lines_per_page:
                                  (self.current_page + 1) * self.lines_per_page]
        wrapped_text = "\n".join(page_text)

        page_label = tk.Label(self.root, text=wrapped_text, font=("Arial", 12))
        page_label.pack(pady=20)

        if self.current_page < len(self.pdf_text) // self.lines_per_page:
            next_button = tk.Button(self.root, text="Next Page", command=self.next_page)
            next_button.pack(pady=10)

    def next_page(self):
        self.current_page += 1
        for widget in self.root.winfo_children():
            widget.destroy()
        self.display_page()

if __name__ == "__main__":
    pdf_file = 'documents/TKMFullText.pdf'  # Change to your PDF file path
    text = extract_text_from_pdf(pdf_file)

    root = tk.Tk()
    root.title("PDF Viewer")
    viewer = PDFViewer(root, text)
    viewer.display_page()
    root.mainloop()