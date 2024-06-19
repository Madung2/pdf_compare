# from dict_data import json1, json2
import difflib
def split_ele_by_text_num(input_data):
    output_data = []

    for item in input_data:
        text = item['text']
        for char in text:
            new_item = item.copy()
            new_item['text'] = char
            output_data.append(new_item)
    return output_data

def merge_texts(line):
    merged_text = ''.join([item['text'] for item in line])
    return merged_text

def highlight_differences(json_data, diffs, tag):
    index = 0
    collected_items = []
    
    for diff in diffs:
        if diff.startswith(' '):
            index += len(diff[2:])
        elif diff.startswith('-') or diff.startswith('+'):
            length = len(diff[2:])
            for line in json_data:
                for item in line:
                    # item이 문자열인지 확인
                    if isinstance(item, dict) and 'text' in item:
                        item_len = len(item['text'])
                        if index < item_len:
                            item['diff'] = tag
                            collected_items.append(item)
                            break
                        index -= item_len
                    else:
                        # item이 문자열인 경우
                        item_len = len(item)
                        if index < item_len:
                            collected_items.append({'text': item, 'diff': tag})
                            break
                        index -= item_len
    
    return collected_items


def compare_json(line1, line2):
    line1_text = [d['text'] for d in line1]
    line2_text = [d['text'] for d in line2]
    matcher = difflib.SequenceMatcher(None, line1_text, line2_text)
    added = []
    deleted = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            deleted.extend(line1[i1:i2])
            added.extend(line2[j1:j2])
        elif tag == 'delete':
            deleted.extend(line1[i1:i2])
        elif tag == 'insert':
            added.extend(line2[j1:j2])
    return deleted, added



def remove_space_element(line):
    new_line = [] 
    for ele in line:
        if ele['text'].strip() != '':
            new_line.append(ele)

    return new_line
