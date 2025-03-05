import itertools
import random
from collections import Counter

def roll_dice(n=5):
    return [random.randint(1, 6) for _ in range(n)]

def calculate_score(dice):
    count = Counter(dice)
    unique_numbers = sorted(count.keys())
    
    # 1~5까지 1개씩 or 2~6까지 1개씩이면 300점
    if unique_numbers == [1, 2, 3, 4, 5] or unique_numbers == [2, 3, 4, 5, 6]:
        return 300
    
    best_score = 0
    
    for A, B in itertools.permutations(set(dice), 2):
        A_count = count[A]
        B_count = count[B]
        
        if A_count == 2 and B_count < 2:
            best_score = max(best_score, 20)
        elif A_count == 2 and B_count == 2:
            best_score = max(best_score, 50)
        elif A_count == 3 and B_count < 2:
            best_score = max(best_score, 80)
        elif A_count == 3 and B_count == 2:
            best_score = max(best_score, 250)
        elif A_count == 4:
            best_score = max(best_score, 800)
        elif A_count == 5:
            best_score = max(best_score, 3000)
    
    return best_score

def expected_value(dice, rerolls_left, joker_cards):
    if rerolls_left == 0:
        return calculate_score(dice)
    
    current_score = calculate_score(dice)
    
    possible_rolls = [roll_dice(len(dice)) for _ in range(1000)]  # Monte Carlo 시뮬레이션
    expected_scores = [calculate_score(new_roll) for new_roll in possible_rolls]
    avg_reroll_score = sum(expected_scores) / len(expected_scores)
    
    return max(current_score, avg_reroll_score)

def best_strategy(dice, rerolls_left, joker_cards):
    current_score = calculate_score(dice)
    
    if rerolls_left == 0:
        return dice, current_score, joker_cards
    
    best_dice = dice
    best_expected_score = current_score
    
    for i in range(len(dice)):
        new_dice = dice[:i] + [random.randint(1, 6)] + dice[i+1:]
        exp_score = expected_value(new_dice, rerolls_left - 1, joker_cards)
        if exp_score > best_expected_score:
            best_expected_score = exp_score
            best_dice = new_dice
    
    # 조커 카드 사용 판단 (각 주사위를 개별적으로 고정하는 것 반영)
    count = Counter(dice)
    most_common = count.most_common(1)
    if most_common and joker_cards > 0:
        A, A_count = most_common[0]
        needed_jokers_for_4 = max(0, 4 - A_count)
        needed_jokers_for_5 = max(0, 5 - A_count)
        
        if A_count >= 3 and joker_cards >= needed_jokers_for_5 and joker_cards <= 50:  # A를 5개로 만들기 위한 조커 개수 확인 및 제한 적용
            best_expected_score = 3000
            joker_cards -= needed_jokers_for_5
        elif A_count >= 2 and joker_cards >= needed_jokers_for_4 and joker_cards <= 50:  # A를 4개로 만들기 위한 조커 개수 확인 및 제한 적용
            best_expected_score = 800
            joker_cards -= needed_jokers_for_4
    
    return best_dice, best_expected_score, joker_cards

# 예제 실행
dice = roll_dice()
rerolls_left = 1000  # 주사위를 굴릴 기회 증가
joker_cards = 50  # 조커 카드 제한 적용

print("초기 주사위:", dice)
best_dice, best_score, remaining_jokers = best_strategy(dice, rerolls_left, joker_cards)
print("최적 전략 후 주사위:", best_dice, "예상 점수:", best_score, "남은 조커:", remaining_jokers)
