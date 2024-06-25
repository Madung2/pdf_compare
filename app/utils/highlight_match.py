
import fitz  # PyMuPDF

def rects_overlap(rect1, rect2, threshold=3):
    """Check if two rectangles overlap, considering a threshold for x and y values."""
    return not (rect1.x1 + threshold < rect2.x0 or rect1.x0 - threshold > rect2.x1 or 
                rect1.y1 + threshold < rect2.y0 or rect1.y0 - threshold > rect2.y1)

def extract_highlighted_text(document):
    highlights = []

    for page_num in range(len(document)):
        page = document[page_num]
        annotations = page.annots()

        if annotations:
            for annot in annotations:
                if annot.type[0] == 8:  # Highlight annotation
                    rect = annot.rect
                    text = page.get_text("text", clip=rect)
                    highlight_info = {
                        'page': page_num + 1,
                        'coordinates': rect,
                        'text': text,
                        'y': rect.y0
                    }
                    highlights.append(highlight_info)

    # Merge overlapping highlights
    merged_highlights = []
    for highlight in highlights:
        merged = False
        for merged_highlight in merged_highlights:
            if rects_overlap(highlight['coordinates'], merged_highlight['coordinates']):
                merged_highlight['coordinates'] = merged_highlight['coordinates'] | highlight['coordinates']
                merged_highlight['text'] += highlight['text']
                merged = True
                break
        if not merged:
            merged_highlights.append(highlight)

    # Sort highlights by 'y' coordinate
    merged_highlights.sort(key=lambda x: x['y'])

    return merged_highlights

def highlight_coordinate(document, highlight):
    page = document[highlight['page'] - 1]
    rect = highlight['coordinates']
    annot = page.add_highlight_annot(rect)
    annot.set_colors(stroke=(1, 0.75, 0.8), fill=(0, 1, 0))
    annot.update()

def match_highlight(pdf1, pdf2, threshold=20):
    highlights1 = extract_highlighted_text(pdf1)
    highlights2 = extract_highlighted_text(pdf2)

    unmatched_highlights1 = []
    unmatched_highlights2 = []

    # Find highlights in pdf_path1 that are not in pdf_path2
    for highlight1 in highlights1:
        match_found = False
        for highlight2 in highlights2:
            if highlight1['page'] == highlight2['page'] and rects_overlap(highlight1['coordinates'], highlight2['coordinates'], threshold):
                match_found = True
                break
        if not match_found:
            unmatched_highlights1.append(highlight1)

    # Find highlights in pdf_path2 that are not in pdf_path1
    for highlight2 in highlights2:
        match_found = False
        for highlight1 in highlights1:
            if highlight2['page'] == highlight1['page'] and rects_overlap(highlight2['coordinates'], highlight1['coordinates'], threshold):
                match_found = True
                break
        if not match_found:
            unmatched_highlights2.append(highlight2)
    count = 1
    for highlight in unmatched_highlights1:
        highlight_coordinate(pdf2, highlight)
        # print(f"Unmatched Highlight {count} in file1")
        # print(f"Page: {highlight['page']}")
        # print(f"Coordinates: {highlight['coordinates']}")
        # print(f"Text: {highlight['text']}")
        # print(f"Y: {highlight['y']}")
        count += 1

    count = 1
    for highlight in unmatched_highlights2:
        # print(f"Unmatched Highlight {count} in file2")
        highlight_coordinate(pdf1, highlight)
        # print(f"Page: {highlight['page']}")
        # print(f"Coordinates: {highlight['coordinates']}")
        # print(f"Text: {highlight['text']}")
        # print(f"Y: {highlight['y']}")
        count += 1

    return unmatched_highlights1, unmatched_highlights2