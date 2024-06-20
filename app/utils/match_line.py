import Levenshtein
threshold = 0.6  # 0에서 1 사이의 값, 높을수록 엄격함
second_threshold = 0.6

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


def remove_spaces(text):
    return text.replace(" ", "")
# def get_matched_pairs(position1, position2):
#     # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
#     # print(position1, 'position1')
#     # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
#     # print(position2, 'position2')
#     # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
#     # 유사도에 따라 매칭
#     matched_pairs = []
#     unmatched_right = set(position2.keys())  # 매칭되지 않은 오른쪽 딕셔너리 항목
#     unmatched_left = set(position1.keys())    # 매칭되지 않은 왼쪽 딕셔너리 항목

#     for left_item in position1.keys():
#         best_match = None
#         best_score = 0  # 유사도는 0에서 1 사이의 값
        
#         for right_item in list(unmatched_right):  # 매칭되지 않은 항목만 비교
#             score = similarity_score(remove_spaces(left_item), remove_spaces(right_item))
#             if score > best_score:
#                 best_score = score
#                 best_match = right_item
        
#         if best_match and best_score >= threshold:
#             matched_pairs.append((left_item, position1[left_item], best_match, position2[best_match]))
#             unmatched_right.remove(best_match)  # 매칭된 항목 제거
#             unmatched_left.discard(left_item)
    
#     # 매칭되지 않은 항목에 밸류값 포함
#     unmatched_left_items = [(item, position1[item]) for item in unmatched_left]
#     unmatched_right_items = [(item, position2[item]) for item in unmatched_right]

#     second_matches, final_left, final_right = find_best_matches_by_first_element(unmatched_left_items, unmatched_right_items)
#     # 두 번째 매칭 결과 합치기
#     for match in second_matches:
#         matched_pairs.append((match[0][0], match[0][1], match[1][0], match[1][1]))

#     # 최종 매칭되지 않은 항목들
#     final_left = [item for item in unmatched_left_items if item not in [m[0] for m in second_matches]]
#     final_right = [item for item in unmatched_right_items if item not in [m[1] for m in second_matches]]

    
#     return matched_pairs, final_left, final_right




# def get_matched_pairs(position1, position2):
#     def get_y_position(item):
#         return item[0]['bbox'][1]
    
#     matched_pairs = []
#     unmatched_right = set(position2.keys())
#     unmatched_left = set(position1.keys())

#     for left_item in position1.keys():
#         best_match = None
#         best_score = 0  # 유사도는 0에서 1 사이의 값
#         left_y = get_y_position(position1[left_item])

#         for right_item in list(unmatched_right):  # 매칭되지 않은 항목만 비교
#             right_y = get_y_position(position2[right_item])
#             if abs(left_y - right_y) <= 10:
#                 score = similarity_score(remove_spaces(left_item), remove_spaces(right_item))
#                 if score > best_score:
#                     best_score = score
#                     best_match = right_item
        
#         if best_match and best_score >= threshold:
#             matched_pairs.append((left_item, position1[left_item], best_match, position2[best_match]))
#             unmatched_right.remove(best_match)  # 매칭된 항목 제거
#             unmatched_left.discard(left_item)
    
#     unmatched_left_items = [(item, position1[item]) for item in unmatched_left]
#     unmatched_right_items = [(item, position2[item]) for item in unmatched_right]

#     # second_matches, final_left, final_right = find_best_matches_by_first_element(unmatched_left_items, unmatched_right_items)

#     # for match in second_matches:
#     #     matched_pairs.append((match[0][0], match[0][1], match[1][0], match[1][1]))

#     # final_left = [item for item in unmatched_left_items if item not in [m[0] for m in second_matches]]
#     # final_right = [item for item in unmatched_right_items if item not in [m[1] for m in second_matches]]

#     # 마지막으로, 처음 시작하는 두 글자가 동일한 항목 매칭
#     # final_left_texts = {item[0]: item[1] for item in unmatched_left_items}
#     # final_right_texts = {item[0]: item[1] for item in unmatched_right_items}
    
#     # for left_text, left_value in list(final_left_texts.items()):
#     #     for right_text, right_value in list(final_right_texts.items()):
#     #         if remove_spaces(left_text)[:2] == remove_spaces(right_text)[:2]:
#     #             matched_pairs.append((left_text, left_value, right_text, right_value))
#     #             if (left_text, left_value) in unmatched_left_items:
#     #                 unmatched_left_items.remove((left_text, left_value))
#     #             if (right_text, right_value) in unmatched_right_items:
#     #                 unmatched_right_items.remove((right_text, right_value))
#     #             break

#     return matched_pairs, unmatched_left_items, unmatched_right_items


def get_matched_pairs(position1, position2, y_threshold=10, x_threshold=50, similarity_threshold=0.7):
    def get_y_position(item):
        return item[0]['bbox'][1]
    
    def get_x_position(item):
        return item[0]['bbox'][0]
    def first_two_chars_match(str1, str2):
        return str1[:2] == str2[:2]
    
    matched_pairs = []
    unmatched_right = set(position2.keys())
    unmatched_left = set(position1.keys())

    for left_item in position1.keys():
        best_match = None
        best_score = 0  # 유사도는 0에서 1 사이의 값
        left_y = get_y_position(position1[left_item])
        left_x = get_x_position(position1[left_item])

        for right_item in list(unmatched_right):  # 매칭되지 않은 항목만 비교
            right_y = get_y_position(position2[right_item])
            right_x = get_x_position(position2[right_item])
            if abs(left_y - right_y) <= y_threshold and abs(left_x - right_x) <= x_threshold:
                score = similarity_score(remove_spaces(left_item), remove_spaces(right_item))
                if score > best_score:
                    best_score = score
                    best_match = right_item
        
        if best_match and best_score >= similarity_threshold:
            matched_pairs.append((left_item, position1[left_item], best_match, position2[best_match]))
            unmatched_right.remove(best_match)  # 매칭된 항목 제거
            unmatched_left.discard(left_item)


        # 두 번째 매치 조건 추가: y 값 차이가 10 이하이고 처음 두 글자가 같은 경우
    for left_item in list(unmatched_left):  # 아직 매칭되지 않은 항목만 비교
        left_y = get_y_position(position1[left_item])
        left_text = remove_spaces(left_item)

        for right_item in list(unmatched_right):  # 매칭되지 않은 항목만 비교
            right_y = get_y_position(position2[right_item])
            right_text = remove_spaces(right_item)
            if abs(left_y - right_y) <= y_threshold and first_two_chars_match(left_text, right_text):
                matched_pairs.append((left_item, position1[left_item], right_item, position2[right_item]))
                unmatched_right.remove(right_item)  # 매칭된 항목 제거
                unmatched_left.discard(left_item)
                break  # 매칭된 후 루프 종료
    
    unmatched_left_items = [(item, position1[item]) for item in unmatched_left]
    unmatched_right_items = [(item, position2[item]) for item in unmatched_right]

    # # unmatched_left_items 중 y 값의 차이가 6 이하인 항목들을 합침
    # combined_unmatched_left_items = []
    # while unmatched_left_items:
    #     base_item, base_value = unmatched_left_items.pop(0)
    #     base_y = get_y_position(base_value)
    #     combined_group = [(base_item, base_value)]

    #     remaining_items = []
    #     for item, value in unmatched_left_items:
    #         if abs(base_y - get_y_position(value)) <= 6:
    #             combined_group.append((item, value))
    #         else:
    #             remaining_items.append((item, value))

    #     combined_unmatched_left_items.append(combined_group)
    #     unmatched_left_items = remaining_items

    # # unmatched_right_items 중 y 값의 차이가 6 이하인 항목들을 합침
    # combined_unmatched_right_items = []
    # while unmatched_right_items:
    #     base_item, base_value = unmatched_right_items.pop(0)
    #     base_y = get_y_position(base_value)
    #     combined_group = [(base_item, base_value)]

    #     remaining_items = []
    #     for item, value in unmatched_right_items:
    #         if abs(base_y - get_y_position(value)) <= 6:
    #             combined_group.append((item, value))
    #         else:
    #             remaining_items.append((item, value))

    #     combined_unmatched_right_items.append(combined_group)
    #     unmatched_right_items = remaining_items

    # # combined_group의 각 그룹을 하나의 항목으로 병합
    # merged_left_items = [(group[0][0], group[0][1]) for group in combined_unmatched_left_items]
    # merged_right_items = [(group[0][0], group[0][1]) for group in combined_unmatched_right_items]

    # # merged_left_items와 merged_right_items를 비교하여 y 위치 차이가 6 이하인 항목들을 matched_pairs에 추가
    # new_matched_pairs = []
    # remaining_left = []
    # for left_item, left_value in merged_left_items:
    #     left_y = get_y_position(left_value)
    #     found_match = False
    #     for right_item, right_value in merged_right_items:
    #         right_y = get_y_position(right_value)
    #         if abs(left_y - right_y) <= 6:
    #             new_matched_pairs.append((left_item, left_value, right_item, right_value))
    #             found_match = True
    #             break
    #     if not found_match:
    #         remaining_left.append((left_item, left_value))

    # remaining_right = [item for item in merged_right_items if not any(item[0] == pair[2] for pair in new_matched_pairs)]

    # matched_pairs.extend(new_matched_pairs)

    return matched_pairs, unmatched_left_items, unmatched_right_items#remaining_left, remaining_right


