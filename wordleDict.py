import re

def load_words(filename="words.txt"):
    """
    단어 목록 파일을 읽어서 소문자로 변환한 리스트로 반환합니다.
    파일이 없을 경우 안내 메시지를 출력하고 빈 리스트를 반환합니다.
    """
    try:
        with open(filename, "r") as f:
            # 각 줄의 단어를 읽어와서 앞뒤 공백을 제거하고 소문자로 변환
            return [word.strip().lower() for word in f if word.strip()]
    except FileNotFoundError:
        print(f"❌ 단어 파일 '{filename}'이 존재하지 않아요. 파일을 확인해주세요!")
        return []

def pattern_to_regex(pattern: str):
    """
    워들 스타일 패턴(예: _ a _ b _)을 정규식으로 변환합니다.
    '_'는 임의의 한 글자를 의미하며, 나머지 글자는 그대로 사용됩니다.
    """
    cleaned = pattern.replace(" ", "").lower()
    # '_'는 '.'로 변환하여 정규식에서 임의의 한 글자를 의미하게 함
    return "^" + "".join("." if ch == "_" else ch for ch in cleaned) + "$"

def parse_loose_letters(input_str):
    """
    유동 글자와 해당 글자가 오면 안 되는 위치를 파싱합니다.
    예시 입력: a(1,4) b(3,4)
    결과: {'a': [0, 3], 'b': [2, 3]}  # 인덱스는 0부터 시작
    """
    pattern = r"([a-zA-Z])\(([\d,]+)\)"
    result = {}
    for match in re.finditer(pattern, input_str):
        letter = match.group(1).lower()
        # 입력 위치는 1부터 시작하므로 0부터 시작하도록 변환
        positions = [int(p)-1 for p in match.group(2).split(",")]
        result[letter] = positions
    return result

def filter_words(words, fixed_pattern, loose_letters, exclude_letters):
    """
    단어 리스트에서 아래 조건을 모두 만족하는 단어만 필터링합니다.
    1. fixed_pattern에 맞는 단어
    2. exclude_letters에 포함된 글자가 없는 단어
    3. loose_letters에 명시된 글자가 반드시 포함되어 있고, 지정된 위치에는 없어야 함
    """
    regex = re.compile(pattern_to_regex(fixed_pattern))
    exclude_set = set(exclude_letters.lower().replace(",", ""))
    loose_map = parse_loose_letters(loose_letters)

    results = []
    for word in words:
        # 패턴에 맞지 않으면 건너뜀
        if not regex.match(word):
            continue

        # 제외할 글자가 포함되어 있으면 건너뜀
        if any(ch in word for ch in exclude_set):
            continue

        # 유동 글자 조건 검사
        valid = True
        for letter, bad_positions in loose_map.items():
            # 해당 글자가 반드시 포함되어야 함
            if letter not in word:
                valid = False
                break
            # 지정된 위치에는 해당 글자가 오면 안 됨
            if any(word[pos] == letter for pos in bad_positions if 0 <= pos < len(word)):
                valid = False
                break
        if valid:
            results.append(word)
    return results

def main():
    print("="*50)
    print("🎯 워들 단어 필터기에 오신 걸 환영합니다!")
    print("이 프로그램은 워들 게임에서 사용할 수 있는 단어를 쉽게 찾아주는 도구입니다.")
    print("아래 안내에 따라 조건을 입력해 주세요 😊")
    print("="*50)

    # 단어 목록 불러오기 및 개수 안내
    words = load_words("words.txt")
    print(f"\n📚 현재 단어 목록에는 총 {len(words)}개의 단어가 저장되어 있습니다.")
    if not words:
        print("단어 목록을 불러올 수 없습니다. 프로그램을 종료합니다.")
        return

    print("\n[1] 확정된 글자 패턴을 입력해주세요.")
    print("    - 예시: _ a _ b _")
    print("    - 언더바(_)는 아직 모르는 글자, 알파벳은 확정된 글자입니다.")
    print("    - 대소문자와 띄어쓰기는 검색에 영향을 주지 않습니다.")
    fixed_pattern = input("    ▶ 패턴 입력: ")

    print("\n[2] 반드시 포함되어야 하지만 특정 위치에는 오면 안 되는 글자를 입력해주세요.")
    print("    - 예시: a(1,4) b(3,4)")
    print("    - a는 1,4번째에 오면 안 되고, b는 3,4번째에 오면 안 됩니다.")
    print("    - 대소문자와 띄어쓰기는 검색에 영향을 주지 않습니다.")
    loose_letters = input("    ▶ 유동 글자 입력: ")

    print("\n[3] 제외할 글자들을 입력해주세요.")
    print("    - 예시: a,d,e,i,s,y")
    print("    - 대소문자와 띄어쓰기는 검색에 영향을 주지 않습니다.")
    exclude_letters = input("    ▶ 제외 글자 입력: ")

    print("\n🔎 조건에 맞는 단어를 찾는 중입니다... 잠시만 기다려 주세요!\n")

    matches = filter_words(words, fixed_pattern, loose_letters, exclude_letters)

    print("="*50)
    if matches:
        print(f"✅ 조건에 맞는 단어는 총 {len(matches)}개입니다!")
        print("="*50)
        for word in matches:
            print(f"  - {word}")
        print("="*50)
        print("검색이 완료되었습니다. 즐거운 워들 플레이 되세요! 🎉")
    else:
        print("😥 조건에 맞는 단어가 없습니다.")
        print("오늘의 워들 정답을 알게 되면 단어 목록에 추가해 주세요!")
        print("다음에 같은 단어가 나왔을 때 더 쉽게 찾을 수 있어요. 😉")
        print("="*50)

if __name__ == "__main__":
    main()
