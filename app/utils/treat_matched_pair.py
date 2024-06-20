import difflib
import re
# 먼저 같은 줄 제외
def filter_special_chars(text):
    return re.sub(r'[\U000f012b]', '', text)
def compare_texts_with_difflib_by_word(text1, text2):
    # Split the texts into words
    words1 = text1.split()
    words2 = text2.split()
    
    # Use difflib to compare the texts
    differ = difflib.Differ()
    diff = list(differ.compare(words1, words2))
    
    # Initialize a list to hold the differences
    differences = []

    # Process the difflib output
    for item in diff:
        if item.startswith('- '):
            # Removed from text1
            differences.append((item[2:], None))
        elif item.startswith('+ '):
            # Added in text2
            differences.append((None, item[2:]))
    
    return differences

# def compare_texts_with_difflib_by_each_text(str1, str2):

#     # Remove spaces from both strings
#     str1_clean = str1.replace(' ', '')
#     str2_clean = str2.replace(' ', '')

#     # Use difflib to get the differences
#     diff = difflib.ndiff(str1_clean, str2_clean)

#     # Extract the differences
#     # differences = []
#     l_diffs = []
#     r_diffs = [] 

#     # Process the difflib output
#     for item in diff:
#         if '\U000f012b' in item:
#             continue
#         if item.startswith('- '):
#             # Removed from text1
#             l_diffs.append(item[2:])
#         elif item.startswith('+ '):
#             # Added in text2
#             r_diffs.append(item[2:])
    
#     return l_diffs, r_diffs
def remove_matching_elements(ele1, ele2):
    # Strip texts and create sets of stripped texts for both lists
    stripped_texts_ele1 = {item['text'].strip() for item in ele1}
    stripped_texts_ele2 = {item['text'].strip() for item in ele2}
    
    # Find common stripped texts
    common_texts = stripped_texts_ele1 & stripped_texts_ele2
    
    # Remove elements with common stripped texts from both lists
    ele1 = [item for item in ele1 if item['text'].strip() not in common_texts]
    ele2 = [item for item in ele2 if item['text'].strip() not in common_texts]
    
    return ele1, ele2
def compare_texts_with_difflib_by_each_text(str1, str2):
    # Remove spaces from both strings
    # str1 = str1.replace(' ', '')
    # str1_clean = re.sub(r'[()]', '', str1)
    # str2 = str2.replace(' ', '')
    # str2_clean = re.sub(r'[()]', '', str2)

    # # Function to split the text into numbers and non-numbers
    # # def split_numbers_and_text(text):
    # #     parts = re.findall(r'\d+|[^\d]', text)
    # #     return parts
    # def split_numbers_and_text(text):
    #     # 정규 표현식을 사용하여 숫자, 영어 단어, 한국어 글자를 분리합니다.
    #     parts = re.findall(r'\d+|[a-zA-Z]+|[가-힣]', text)
    #     return parts

    # # Split the cleaned strings into numbers and non-numbers
    # str1_split = split_numbers_and_text(str1_clean)
    # str2_split = split_numbers_and_text(str2_clean)
    # def split_numbers_and_text(text):
    # # 정규 표현식을 사용하여 숫자, 영어 단어, 한국어 글자를 분리합니다.
    #     parts = re.findall(r'\d+|[a-zA-Z]+|[가-힣]', text)
    #     return parts
    def split_numbers_and_text(text):
        # 정규 표현식을 사용하여 숫자, 영어 단어, 한국어 글자를 분리합니다.
        parts = re.findall(r'\d+|[a-zA-Z]+|[가-힣]+', text)
        
        result = []
        for part in parts:
            if re.match(r'\d+|[a-zA-Z]+', part):  # 숫자나 영어 단어인 경우
                result.append(part)
            elif re.match(r'[가-힣]+', part):  # 한국어 글자인 경우
                result.extend(list(part))
        
        return result
    # str1과 str2를 먼저 숫자와 텍스트로 분리합니다.
    str1_split = split_numbers_and_text(str1)
    str2_split = split_numbers_and_text(str2)

    # 각 요소에서 클리닝 작업을 수행합니다.
    str1_split_clean = [re.sub(r'[ ()]', '', part) for part in str1_split]
    str2_split_clean = [re.sub(r'[ ()]', '', part) for part in str2_split]
    # Use difflib to get the differences
    diff = difflib.ndiff(str1_split_clean, str2_split_clean)

    # Extract the differences
    l_diffs = []
    r_diffs = []

    # Process the difflib output
    for item in diff:
        if '\U000f012b' in item:
            continue
        if item.startswith('- '):
            # Removed from text1
            l_diffs.append(item[2:])
        elif item.startswith('+ '):
            # Added in text2
            r_diffs.append(item[2:])
    
    return l_diffs, r_diffs

def return_only_diffs(matched_pairs):
    new_matched_pairs = []
    for text1, ele1, text2, ele2 in matched_pairs:
        ele1, ele2 = remove_matching_elements(ele1, ele2)
        if filter_special_chars(text1.strip()) != filter_special_chars(text2.strip()):
            # diff = compare_texts_with_difflib(text1, text2)
            l_diffs, r_diffs = compare_texts_with_difflib_by_each_text(text1, text2)

            new_matched_pairs.append([l_diffs, r_diffs, ele1, ele2])
    
    return new_matched_pairs