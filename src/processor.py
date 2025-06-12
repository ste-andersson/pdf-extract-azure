def process_blocks(blocks, document_id):
    result = []
    counter = 1
    for block in blocks:
        page_str = f"{block['page']:03d}"
        count_str = f"{counter:04d}"
        if block['type'] == 'header':
            id_str = f"{document_id}-H{block['level']}-{page_str}-{count_str}"
        else:
            id_str = f"{document_id}-P-{page_str}-{count_str}"
        result.append({
            "id": id_str,
            "type": block['type'],
            "level": block.get('level'),
            "page": block['page'],
            "text": block['text']
        })
        counter += 1
    return result
