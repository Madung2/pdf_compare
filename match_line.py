import Levenshtein
threshold = 0.3  # 0에서 1 사이의 값, 높을수록 엄격함

def similarity_score(s1, s2):
    return 1 - Levenshtein.distance(s1, s2) / max(len(s1), len(s2))


def get_matched_pairs(position1, position2):
    # 유사도에 따라 매칭
    matched_pairs = []
    unmatched_right = set(position2.keys())  # 매칭되지 않은 오른쪽 딕셔너리 항목
    unmatched_left = set(position1.keys())    # 매칭되지 않은 왼쪽 딕셔너리 항목

    for left_item in position1.keys():
        best_match = None
        best_score = 0  # 유사도는 0에서 1 사이의 값
        
        for right_item in list(unmatched_right):  # 매칭되지 않은 항목만 비교
            score = similarity_score(left_item, right_item)
            if score > best_score:
                best_score = score
                best_match = right_item
        
        if best_match and best_score >= threshold:
            matched_pairs.append((left_item, position1[left_item], best_match, position2[best_match]))
            unmatched_right.remove(best_match)  # 매칭된 항목 제거
            unmatched_left.discard(left_item)
    
    # 매칭되지 않은 항목에 밸류값 포함
    unmatched_left_items = [(item, position1[item]) for item in unmatched_left]
    unmatched_right_items = [(item, position2[item]) for item in unmatched_right]

    return matched_pairs, unmatched_left_items, unmatched_right_items
