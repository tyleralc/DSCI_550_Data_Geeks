from tika import parser as p
import pandas as pd
import requests
    
#function pdf -> text extraction
def get_data_from_web(url):
    response = requests.get(url)
    results = p.from_buffer(response.content)
    return results

def extract_text():
    #extract text from any pdf
    pdf_url = "https://www.bl.uk/learning/resources/pdf/makeanimpact/sw-transcripts.pdf"
    results = get_data_from_web(pdf_url)
    print("\nFile Content: \n{}".format(results["content"].strip()))
    
if __name__=="__main__":
    df = pd.read_csv("Final_bik_dataset.tsv", sep='\t', encoding = "ISO-8859-1")
    doi= df["DOI"].tolist()
    extract_text()
