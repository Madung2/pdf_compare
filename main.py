import fitz  # PyMuPDF
from run_compare import *
from match_line import get_matched_pairs
from treat_matched_pair import *
# def split_by_line(text_positions):
#     lines = {}
    
#     for item in text_positions:
        
#         text = item["text"]
#         bbox = item["bbox"]
#         page_num = item["page_num"]
#         y_position = bbox[1]
        
#         if page_num not in lines:
#             lines[page_num] = {}

#         if y_position not in lines[page_num]:
#             lines[page_num][y_position] = []

#         lines[page_num][y_position].append(item)
    
#     # Flatten the dictionary into a list of lists
#     line_list = []
#     for page_num in sorted(lines.keys()):
#         for y_position in sorted(lines[page_num].keys()):
#             line_list.append(lines[page_num][y_position])
    
#     return line_list
def split_by_line(text_positions):
    lines = {}
    y_positions = {}

    for item in text_positions:
        
        text = item["text"]
        bbox = item["bbox"]
        page_num = item["page_num"]
        y_position = bbox[1]
        
        if page_num not in lines:
            lines[page_num] = {}
            y_positions[page_num] = set()

        # Find the closest y_position within a tolerance of 3
        matched_y = None
        for y in y_positions[page_num]:
            if abs(y - y_position) <= 4:
                matched_y = y
                break
        
        if matched_y is None:
            y_positions[page_num].add(y_position)
            matched_y = y_position
        
        if matched_y not in lines[page_num]:
            lines[page_num][matched_y] = []

        lines[page_num][matched_y].append(item)
    
    # Flatten the dictionary into a list of lists
    line_list = []
    for page_num in sorted(lines.keys()):
        for y_position in sorted(lines[page_num].keys()):
            line_list.append(lines[page_num][y_position])
    
    return line_list
def merge_texts_on_same_line(text_positions):
    lines = {}
    
    for item in text_positions:
        text = item["text"]
        bbox = item["bbox"]
        page_num = item["page_num"]
        y_position = bbox[1]
        
        if page_num not in lines:
            lines[page_num] = {}

        if y_position not in lines[page_num]:
            lines[page_num][y_position] = []

        lines[page_num][y_position].append(item)
    
    # Merge texts on the same line
    merged_lines = []
    for page_num in sorted(lines.keys()):
        for y_position in sorted(lines[page_num].keys()):
            line_items = lines[page_num][y_position]
            merged_text = ""
            merged_bbox = [None, y_position, None, line_items[0]["bbox"][3]]
            
            for i, item in enumerate(line_items):
                if merged_bbox[0] is None or item["bbox"][0] < merged_bbox[0]:
                    merged_bbox[0] = item["bbox"][0]
                if merged_bbox[2] is None or item["bbox"][2] > merged_bbox[2]:
                    merged_bbox[2] = item["bbox"][2]
                
                if i == 0:
                    merged_text += item["text"]
                else:
                    previous_item = line_items[i-1]
                    if item["bbox"][0] <= previous_item["bbox"][2]:
                        merged_text += item["text"]
                    else:
                        merged_lines.append({
                            "text": merged_text,
                            "bbox": merged_bbox,
                            "page_num": page_num
                        })
                        merged_text = item["text"]
                        merged_bbox = [item["bbox"][0], y_position, item["bbox"][2], item["bbox"][3]]
            
            merged_lines.append({
                "text": merged_text,
                "bbox": merged_bbox,
                "page_num": page_num
            })
    
    return merged_lines    
def extract_text_with_positions(pdf_path):
    doc = fitz.open(pdf_path)
    text_positions = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] == 0:  # block type 0 is text
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["text"].strip() =='':
                        # if span["text"] ==' ' or span["text"].strip() =='':
                            continue
                        
                        text_positions.append({
                            "text": span["text"],
                            "bbox": span["bbox"],
                            "page_num": page_num
                        })
    text_positions = split_by_line(text_positions)
    # text_positions = [ merge_texts_on_same_line(line) for line in text_positions ] 
    return text_positions

def compare_texts_with_positions(text_positions1, text_positions2):
    diffs = []
    for pos1, pos2 in zip(text_positions1, text_positions2):
        if pos1["text"] != pos2["text"]:
            diffs.append({
                "text1": pos1["text"],
                "text2": pos2["text"],
                "bbox1": pos1["bbox"],
                "bbox2": pos2["bbox"],
                "page_num": pos1["page_num"]
            })
    return diffs

def highlight_text_in_pdf_red(pdf_path, highlights, output_path):
    # PDF 열기
    doc = fitz.open(pdf_path)

    for highlight in highlights:
        page_num = highlight['page_num']
        bbox = highlight['bbox']

        # 페이지 선택
        page = doc[page_num]

        # 하이라이트 추가
        highlight_annot = page.add_highlight_annot(bbox)

        # 하이라이트 색상 설정 (빨간색)
        highlight_annot.set_colors(stroke=(1, 0.75, 0.8), fill=(1, 0.75, 0.8))
        highlight_annot.update()

    # 수정된 PDF 저장
    doc.save(output_path)

def highlight_text_in_pdf_green(pdf_path, highlights, output_path):
    # PDF 열기
    doc = fitz.open(pdf_path)

    for highlight in highlights:
        page_num = highlight['page_num']
        bbox = highlight['bbox']

        # 페이지 선택
        page = doc[page_num]

        # 하이라이트 추가
        highlight_annot = page.add_highlight_annot(bbox)

        # 하이라이트 색상 설정 (빨간색)
        highlight_annot.set_colors(stroke=(0, 1, 0), fill=(0, 1, 0))
        highlight_annot.update()

    # 수정된 PDF 저장
    doc.save(output_path)

def process_line_element(text_positions):
    new_text_positions = {}
    for line in text_positions:
        line_text = ''.join([ ele['text'] for ele in line])
        
        rest_element = line
        new_text_positions[line_text] = rest_element
    return new_text_positions


def make_output_json(pdf_file1, pdf_file2):
    ####file1
    text_positions1 = extract_text_with_positions(pdf_file1)
    text_positions1 = process_line_element(text_positions1)

    #####file2
    text_positions2 = extract_text_with_positions(pdf_file2)
    text_positions2 = process_line_element(text_positions2)

    # match by line
    matched_pairs, unmatched_left, unmatched_right = get_matched_pairs(text_positions1,text_positions2)
    for (a,a_, b,b_) in matched_pairs:
        print(a)
        print(b)
        print('########')
    # Treat match by line
    new_matched_pairs = return_only_diffs(matched_pairs)

    return new_matched_pairs, unmatched_left, unmatched_right


def highlight_text_in_bbox(page, bbox, target_text=None, color=(1, 1, 0)):
    rect = fitz.Rect(bbox)
    words = page.get_text("words", clip=rect)
    for word in words:
        if target_text is None or word[4] == target_text:
            highlight_rect = fitz.Rect(word[:4])
            highlight = page.add_highlight_annot(highlight_rect)
            highlight.set_colors({"stroke": color, "fill": color})
            highlight.update()

def make_output_pdf(pdf_file1, pdf_file2):
    output_file1 = 'output1.pdf'
    output_file2 = 'output2.pdf'
    match_pairs, unmatched_left, unmatched_right = make_output_json(pdf_file1, pdf_file2)

    try:
        pdf1 = fitz.open(pdf_file1)
    except:
        print(f'Failed to open {pdf_file1}')
        return False, False

    try:
        pdf2 = fitz.open(pdf_file2)
    except:
        print(f'Failed to open {pdf_file2}')
        return False, False

    ###############highlight match pairs #####################
    for [diffs, left, right] in match_pairs:
        for (left_target_text, right_target_text) in diffs:
            if left_target_text:
                for ele in left:
                    txt = ele['text']
                    bbox = ele['bbox']
                    page = pdf1[ele['page_num']]
                    if left_target_text in txt:
                        highlight_text_in_bbox(page, bbox, left_target_text, (1, 0.75, 0.8))
            if right_target_text:
                for ele in right:
                    txt = ele['text']
                    bbox = ele['bbox']
                    page = pdf2[ele['page_num']]
                    if right_target_text in txt:
                        highlight_text_in_bbox(page, bbox, right_target_text, (0, 1, 0))
    ###################highlight right################################
    print('###############')
    print(unmatched_right, len(unmatched_right))
    for text, right_lines in unmatched_right:
        for ele in right_lines:
            txt = ele['text']
            bbox = ele['bbox']
            page = pdf2[ele['page_num']]
            highlight_text_in_bbox(page, bbox, None, (0, 1, 0))
    ###################highlight left################################
    for text, left_lines in unmatched_left:
        for ele in left_lines:
            txt = ele['text']
            bbox = ele['bbox']
            page = pdf2[ele['page_num']]
            highlight_text_in_bbox(page, bbox, None, (1, 0.75, 0.8))

    try:
        pdf1.save(output_file1)
    except:
        print(f'Failed to save {output_file1}')
        return False, False

    try:
        pdf2.save(output_file2)
    except:
        print(f'Failed to save {output_file2}')
        return False, False

    return output_file1, output_file2


if __name__ == "__main__":
    print(111111)
    pdf_file1 = '5-4. 표준임대차계약서_한국공인중개사협회_검토대상1.pdf'  # 실제 파일 경로로 변경하세요.
    pdf_file2 = '5-5. 표준임대차계약서_한국공인중개사협회_검토생략2.pdf' # 실제 파일 경로로 변경하세요.
    # pdf_file1 = 'Non-Use-Warrenty_No1.pdf'  # 실제 파일 경로로 변경하세요.
    # pdf_file2 = 'Non-Use-Warrenty_No2.pdf' # 실제 파일 경로로 변경하세요.
    make_output_pdf(pdf_file1, pdf_file2)


        # print('##############')
        # # print(res1, res2)
        # input()

    # diffs = compare_texts_with_positions(text_positions1, text_positions2)
    
    # for diff in diffs:
    #     print(f"Difference on page {diff['page_num'] + 1}:")
    #     print(f"PDF 1: {diff['text1']} at {diff['bbox1']}")
    #     print(f"PDF 2: {diff['text2']} at {diff['bbox2']}")
    #     print()
