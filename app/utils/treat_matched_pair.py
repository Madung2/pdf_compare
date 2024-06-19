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

def compare_texts_with_difflib_by_each_text(str1, str2):
    # Remove spaces from both strings
    str1_clean = str1.replace(' ', '')
    str2_clean = str2.replace(' ', '')

    # Function to split the text into numbers and non-numbers
    def split_numbers_and_text(text):
        parts = re.findall(r'\d+|[^\d]', text)
        return parts

    # Split the cleaned strings into numbers and non-numbers
    str1_split = split_numbers_and_text(str1_clean)
    str2_split = split_numbers_and_text(str2_clean)

    # Use difflib to get the differences
    diff = difflib.ndiff(str1_split, str2_split)

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
        if filter_special_chars(text1.strip()) != filter_special_chars(text2.strip()):
            # diff = compare_texts_with_difflib(text1, text2)
            l_diffs, r_diffs = compare_texts_with_difflib_by_each_text(text1, text2)
            new_matched_pairs.append([l_diffs, r_diffs, ele1, ele2])
    
    return new_matched_pairs