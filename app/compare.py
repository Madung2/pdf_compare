
import fitz  # PyMuPDF
from typing import Tuple
from utils.run_compare import *
from utils.match_line import get_matched_pairs
from utils.treat_matched_pair import *
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
def extract_text_with_positions(doc):
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
        highlight_annot.set_colors(stroke=(1, 0.75, 0.8), fill=(0, 1, 0))
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
        print('a:', a)
        print('b:', b)
        print('########')
    # Treat match by line
    new_matched_pairs = return_only_diffs(matched_pairs)

    return new_matched_pairs, unmatched_left, unmatched_right


def highlight_text_in_bbox(page, bbox, target_text=None, color=[(1, 1, 0), (1, 1, 0)]):

    rect = fitz.Rect(bbox)
    words = page.get_text("words", clip=rect)
    for word in words:
        if target_text is None or word[4] == target_text:
            highlight_rect = fitz.Rect(word[:4])
            highlight = page.add_highlight_annot(highlight_rect)
            highlight.set_colors({"stroke": color[0], "fill": color[1]})
            highlight.update()
            
def is_background_white(page, bbox):
    pix = page.get_pixmap(clip=bbox, alpha=False)
    samples = pix.samples
    num_pixels = len(samples) // 3  # RGB 샘플 수
    avg_r = sum(samples[0::3]) / num_pixels
    avg_g = sum(samples[1::3]) / num_pixels
    avg_b = sum(samples[2::3]) / num_pixels
    # 흰색에 가까운 값의 임계값 설정
    threshold = 240
    return avg_r > threshold and avg_g > threshold and avg_b > threshold

def highlight_nth_char_in_bbox(page, bbox, target_char, n, color=[(1, 1, 0),(1, 1, 0)]):
    rect = fitz.Rect(bbox)
    words = page.get_text("words", clip=rect)
    char_count = 0

    for word in words:
        word_text = word[4]
        word_rect = fitz.Rect(word[:4])
        
        for i, char in enumerate(word_text):
            if char == target_char:
                if char_count == n:
                    # Calculate the bounding box for the specific character
                    char_width = word_rect.width / len(word_text)
                    highlight_rect = fitz.Rect(
                        word_rect.x0 + i * char_width,
                        word_rect.y0,
                        word_rect.x0 + (i + 1) * char_width,
                        word_rect.y1
                    )
                    highlight = page.add_highlight_annot(highlight_rect)
                    highlight.set_colors({"stroke": color[0], "fill": color[1]})
                    highlight.update()
                    return
                char_count += 1

def highlight_differences(elements, diffs, pdf, file_type):
    color = [(1, 0.75, 0.8), (1, 0, 0)] if file_type == 'left' else [(0, 1, 0), (0, 1, 0)]
    diff_index = 0
    for ele in elements:
        txt = ele['text']
        bbox = ele['bbox']
        page = pdf[ele['page_num']]
        current_char_index = 0
        for char in txt:
            if diff_index < len(diffs) and char == diffs[diff_index]:
                highlight_nth_char_in_bbox(page, bbox, char, txt[:current_char_index+1].count(char)-1, color)
                diff_index += 1
            current_char_index += 1

def highlight_word_char_in_bbox(page, bbox,txt, start_index, end_index, color):
    """
    Highlights text in bbox on the given page from start_index to end_index with the specified color.
    
    Arguments:
    page -- the PDF page object
    bbox -- the bounding box of the text element
    start_index -- the starting character index for highlighting
    end_index -- the ending character index for highlighting
    color -- the color to use for highlighting
    """
    # Calculate the width of each character to accurately highlight the text
    text_width = bbox[2] - bbox[0]
    total_chars = len(txt)
    char_width = text_width / total_chars

    # Calculate the bounding box coordinates for the highlight
    highlight_start_x = bbox[0] + (char_width * start_index)
    highlight_end_x = bbox[0] + (char_width * end_index)
    
    highlight_bbox = [highlight_start_x, bbox[1], highlight_end_x, bbox[3]]

    # Add highlight to the page
    highlight = page.add_highlight_annot(highlight_bbox)
    highlight.set_colors({"stroke": color[0], "fill": color[1]})
    highlight.update()

def hightlight_chunk_differences(elements, diffs, pdf, file_type):
    color = [(1, 0.75, 0.8), (1, 0, 0)] if file_type == 'left' else [(0, 1, 0), (0, 1, 0)]
    for ele in elements:
        txt = ele['text']
        bbox = ele['bbox']
        page = pdf[ele['page_num']]
        masked_txt = txt
        for target in diffs:
            for match in re.finditer(re.escape(target), masked_txt):
                start, end = match.span()
                highlight_word_char_in_bbox(page, bbox, txt, start, end, color)
                # Mask the matched part in the original text
                masked_txt = masked_txt[:start] + (' ' * (end - start)) + masked_txt[end:]
                break  # Only highlight the first occurrence in this loop


def split_diffs(diffs):
    number_diffs = []
    text_diffs = []

    for diff in diffs:
        if diff.isdigit():
            number_diffs.append(diff)
        else:
            text_diffs.append(diff)

    return number_diffs, text_diffs

def make_output_pdf(pdf1, pdf2, output_file1, output_file2):

    match_pairs, unmatched_left, unmatched_right = make_output_json(pdf1, pdf2)


    ###############highlight match pairs #####################
    for [l_diff, r_diff, left, right] in match_pairs:

        l_num_diffs, l_text_diffs = split_diffs(l_diff)
        highlight_differences(left, l_text_diffs, pdf1, 'left')
        hightlight_chunk_differences(left, l_num_diffs, pdf1, 'left')

        r_num_diffs, r_text_diffs = split_diffs(r_diff)
        highlight_differences(right, r_text_diffs, pdf2, 'right')
        hightlight_chunk_differences(right, r_num_diffs, pdf2, 'right')
   ###################highlight right################################

    # print('unmatched', unmatched_right, len(unmatched_right))
    
    for text, right_lines in unmatched_right:
        for ele in right_lines:
            txt = ele['text']
            bbox = ele['bbox']
            page = pdf2[ele['page_num']]
            highlight_text_in_bbox(page, bbox, None, [(0, 1, 0), (0, 1, 0)])
    ###################highlight left################################

    # print('unmatched left', unmatched_left, len(unmatched_left))
    for text, left_lines in unmatched_left:
        for ele in left_lines:
            txt = ele['text']
            bbox = ele['bbox']
            page = pdf1[ele['page_num']]
            highlight_text_in_bbox(page, bbox, None, [(1, 0.75, 0.8), (1, 0, 0)])

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
