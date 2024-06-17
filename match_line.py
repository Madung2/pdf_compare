import Levenshtein
threshold = 0.4  # 0에서 1 사이의 값, 높을수록 엄격함
second_threshold = 0.5

def similarity_score(s1, s2):
    return 1 - Levenshtein.distance(s1, s2) / max(len(s1), len(s2))


def get_first_element(string):
    return string.split()[0]

def find_best_matches_by_first_element(items1, items2):
    matches = []
    unmatched_items2 = items2[:]
    for item1 in items1:
        first_element1 = get_first_element(item1[0])
        best_match = None
        best_score = 0
        for item2 in unmatched_items2:
            first_element2 = get_first_element(item2[0])
            similarity = Levenshtein.ratio(first_element1, first_element2)
            if similarity > best_score:
                best_score = similarity
                best_match = item2
        if best_score >= 0.50:
            matches.append((item1, best_match, best_score))
            unmatched_items2.remove(best_match)
    return matches, [item for item in items1 if item not in [m[0] for m in matches]], unmatched_items2



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

    second_matches, final_left, final_right = find_best_matches_by_first_element(unmatched_left_items, unmatched_right_items)
    # 두 번째 매칭 결과 합치기
    for match in second_matches:
        matched_pairs.append((match[0][0], match[0][1], match[1][0], match[1][1]))

    # 최종 매칭되지 않은 항목들
    final_left = [item for item in unmatched_left_items if item not in [m[0] for m in second_matches]]
    final_right = [item for item in unmatched_right_items if item not in [m[1] for m in second_matches]]

    return matched_pairs, final_left, final_right
#    return matched_pairs, unmatched_left_items, unmatched_right_items
