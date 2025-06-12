import os
from dotenv import load_dotenv
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_KEY")

client = DocumentIntelligenceClient(endpoint=AZURE_ENDPOINT, credential=AzureKeyCredential(AZURE_KEY))

def extract_pdf_azure(pdf_file):
    with open(pdf_file, "rb") as f:
        poller = client.begin_analyze_document(model_id="prebuilt-layout", body=f)
        result = poller.result()

    blocks = []
    for page_num, page in enumerate(result.pages, start=1):
        sorted_lines = sorted(page.lines, key=lambda l: l.bounding_regions[0].polygon[0].y)
        current_para = ""
        prev_y = None

        for line in sorted_lines:
            text = line.content.strip()
            if not text:
                continue
            y = line.bounding_regions[0].polygon[0].y

            if prev_y is not None and abs(y - prev_y) > 0.02:
                blocks.append({"type": "paragraph", "page": page_num, "text": current_para.strip()})
                current_para = ""
            current_para += " " + text
            prev_y = y

        if current_para:
            blocks.append({"type": "paragraph", "page": page_num, "text": current_para.strip()})

    result_blocks = []
    for block in blocks:
        words = block['text'].split()
        if len(words) <= 5:
            result_blocks.append({"type": "header", "level": 1, "page": block['page'], "text": block['text']})
        else:
            result_blocks.append(block)
    return result_blocks
