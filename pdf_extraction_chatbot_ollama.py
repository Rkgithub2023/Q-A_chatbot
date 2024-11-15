# -*- coding: utf-8 -*-
"""Pdf_extraction_chatbot.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TKsvDe4TGQXqo7u_U4cnFUQWPNzq6ynT
"""

!pip install pdfplumber

import pdfplumber
import pandas as pd
from pdfplumber.utils import extract_text, get_bbox_overlap, obj_to_bbox

def process_pdf(pdf_path):
    pdf = pdfplumber.open(pdf_path)
    all_text = []
    df_list = []
    for page in pdf.pages:
        filtered_page = page
        chars = filtered_page.chars

        for table in page.find_tables():
            first_table_char = page.crop(table.bbox).chars[0]
            filtered_page = filtered_page.filter(lambda obj:
                get_bbox_overlap(obj_to_bbox(obj), table.bbox) is None
            )
            chars = filtered_page.chars

            df = pd.DataFrame(table.extract())
            df.columns = df.iloc[0]
            markdown = df.drop(0).to_markdown(index=False)
            df_list.append(df)
            chars.append(first_table_char | {"text": markdown})

        page_text = extract_text(chars, layout=True)
        all_text.append(page_text)

    pdf.close()
    return "\n".join(all_text)
    # return df_list

# Path to your PDF file
pdf_path = r"Paper18_Set1_Sol.pdf"
extracted_text = process_pdf(pdf_path)
print(extracted_text)

with open("extracted_file.txt", 'w') as file:
    file.write(extracted_text)

from langchain.text_splitter import RecursiveCharacterTextSplitter

# Step 1: Read text from a .txt file
file_path = '/content/extracted_file.txt'  # Specify the path to your text file

with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()  # Read the entire content of the file

# Step 2: Initialize the RecursiveCharacterTextSplitter from LangChain
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Maximum number of characters per chunk
    chunk_overlap=200,
    add_start_index=True,
)

# Step 3: Split the text using the splitter
chunks = text_splitter.split_text(text)

pip install langchain-community faiss-gpu

from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

from langchain.embeddings import HuggingFaceEmbeddings
!pip install sentence-transformers

!pip install tiktoken

embedding_modelname = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'auto'}  # Use 'cpu' if you don't have a GPU

# Create the embeddings model

embeddings = HuggingFaceEmbeddings(model_name=embedding_modelname, model_kwargs=model_kwargs)

from langchain.schema import Document

documents = [Document(page_content=chunk) for chunk in chunks]

vectorstore=FAISS.from_documents(documents,embeddings)

vectorstore.save_local("faiss_index")

persist_vectorstore=FAISS.load_local("faiss_index",embeddings,allow_dangerous_deserialization=True)

retriever=persist_vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})



pip install langchain_ollama

# Commented out IPython magic to ensure Python compatibility.

!pip install colab-xterm
# %load_ext colabxterm

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %xterm

from langchain_community.llms import Ollama
llm=Ollama(model="llama3.1")

response=llm.invoke("tell me a good book to read about rockets")
print(response)

qa=RetrievalQA.from_chain_type(llm=llm,chain_type="stuff",retriever=retriever)

query="Total tax liability of Kareena Ltd. "
result=qa.run(query)
print(result)

query="Describe the power and duties of Anti-profiteering committee. "
  result=qa.run(query)
  print(result)

query="what is the Total CIF value/ Assessable Value"
result=qa.run(query)
print(result)

query="what is the value in for this 'Input tax credit which are used to supply taxable as well as exempted output supplies'"
result=qa.run(query)
print(result)

query="""crown Beers India Pvt. Ltd., supplies raw material to a job worker
Kareena Ltd. for manufacture of alcoholic liquor for human consumption.
After completing the job-work, the finished product of 5,000 beer bottles
are returned to Crown Beers India Pvt. Ltd., putting the retail sale price as
`200 on each bottle (inclusive of duties and taxes). Kareena Ltd., charged
100 per bottle as job work charges of carrying out of intermediate
production process of alcoholic liquor for human consumption from Crown
Beers India Pvt. Ltd. Find the GST liability if rate is 18% (CGST 9% and
SGST 9%) in the hands of Kareena Ltd.  """
result=qa.run(query)
print(result)
#correct

query="""Bharat Gas sells cooking gas cylinders. Subsidy directly transferred to the
account of the customer. Selling price per cylinder is ` 800. Customer
received subsidy ` 200 directly from Government to his bank account. Net
outflow of the buyer is ` 600. Find the value of supply of goods (per
cylinder) in the hands of Bharat Gas.  """
result=qa.run(query)
print(result)
#correct

query="""
Raman Hotels supplying only accommodation services in Chennai. Turnover of
Raman Hotels is less than 20 Lakhs. Raman Hotels listed hotel on online platform
namely Makemytrip.
The following categories of rooms get booked by the Makemytrip company who
pay to Raman Hotels after deducting their commission.
(A)  Declared value per room (category 1), Non AC Room `950 per Night.
(B)
Declared value per room (category 2), AC Room `1,800 per Night.
(C)  Declared value per room (category 3), AC Room `7,000 per Night, where
additional bed `1,800 per Night.
(D)  Declare value per room (category 4), AC Room `10,000 per Night, but
amount charged is `7000.
You are required to answer:
(1)
Who is liable to pay GST and
(2)
Net GST liability.
"""
result=qa.run(query)

print(result)

query="what is the Value of taxable services for a tamil movie"
result=qa.run(query)
print(result)
#correct

query="what is the abbreviation of RoDTEP"
result=qa.run(query)
print(result)
#correct

query="what is the mode of issue for RoDTEP"
result=qa.run(query)
print(result)
#correct

query="is RoDTEP transferable"
result=qa.run(query)
print(result)
#correct

query="what is the freight amount for the imported goods"
result=qa.run(query)
print(result)
#correct

query="what is the total Assessable Value for the imported goods "
result=qa.run(query)
print(result)
#incorrect

query="what is the value for taxable supply of goods"
result=qa.run(query)
print(result)
#correct