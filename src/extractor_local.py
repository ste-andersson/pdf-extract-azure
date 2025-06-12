import fitz

def extract_pdf_local(pdf_file):
    doc = fitz.open(pdf_file)
    raw_lines = []
    for page_num, page in enumerate(doc, start=1):
        blocks_dict = page.get_text("dict")
        for block in blocks_dict["blocks"]:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                text = " ".join([span["text"] for span in line["spans"] if span["text"].strip() != ""])
                if not text.strip():
                    continue
                font_size = line["spans"][0]["size"]
                top = block["bbox"][1]
                raw_lines.append({
                    "text": text,
                    "font_size": font_size,
                    "top": top,
                    "page": page_num
                })

    font_sizes = sorted({line["font_size"] for line in raw_lines}, reverse=True)
    font_size_to_level = {size: idx+1 for idx, size in enumerate(font_sizes)}

    paragraphs = []
    current_para = ""
    current_page = None

    for line in raw_lines:
        if current_para and abs(line["top"] - prev_top) > 15:
            paragraphs.append({"type": "paragraph", "page": current_page, "text": current_para.strip()})
            current_para = ""
        if not current_para:
            current_page = line["page"]
        current_para += " " + line["text"]
        prev_top = line["top"]

    if current_para:
        paragraphs.append({"type": "paragraph", "page": current_page, "text": current_para.strip()})

    result = []
    for para in paragraphs:
        words = para['text'].split()
        if len(words) <= 8:
            matching_font = max(font_sizes)
            level = font_size_to_level[matching_font]
            result.append({"type": "header", "level": level, "page": para['page'], "text": para['text']})
        else:
            result.append(para)
    return result
