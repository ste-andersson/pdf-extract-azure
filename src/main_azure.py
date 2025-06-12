import sys
from extractor_azure import extract_pdf_azure
from processor import process_blocks

def main():
    pdf_file = sys.argv[1]
    document_id = sys.argv[2]
    blocks = extract_pdf_azure(pdf_file)
    structured = process_blocks(blocks, document_id)
    with open("output_azure.json", "w", encoding="utf-8") as f:
        import json
        json.dump(structured, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
