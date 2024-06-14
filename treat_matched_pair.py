import difflib
# 먼저 같은 줄 제외
def compare_texts_with_difflib(text1, text2):
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


def return_only_diffs(matched_pairs):
    new_matched_pairs = []
    for text1, ele1, text2, ele2 in matched_pairs:
        if text1.strip() != text2.strip():
            diff = compare_texts_with_difflib(text1, text2)
            new_matched_pairs.append([diff, ele1, ele2])
    return new_matched_pairs