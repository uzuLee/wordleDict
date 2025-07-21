import re
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

# =========================
# 디자인 설정
# =========================

BG_COLOR      = "#181824"  # 전체 배경
PANEL_COLOR   = "#2d3142"  # 입력 패널 배경
ENTRY_BG      = "#f6f7fb"  # 입력창 배경
EXAMPLE_TEXT  = "#a0a3b1"  # 예시 글자 색
LABEL_TEXT    = "#f6f7fb"  # 입력창 왼쪽 라벨 글자 색
BTN_COLOR     = "#4f5d75"  # 버튼 배경
BTN_TEXT      = "#f6f7fb"  # 버튼 글자
RESULT_BG     = "#22223b"  # 결과창 배경
RESULT_TEXT   = "#f6f7fb"  # 결과창 글자
LETTER_TAG    = "#9597ff"  # 알파벳 구분자 색상 (고급스러운 색상)
LABEL_FONT    = ("맑은 고딕", 12, "bold")
TITLE_FONT    = ("맑은 고딕", 20, "bold")
RESULT_FONT   = ("맑은 고딕", 12)

# =========================
# 데이터 처리 함수
# =========================

def load_words(filename="words.txt", user_filename="user_words.txt"):
    """
    기본 단어 파일과 사용자가 추가한 단어 파일을 모두 읽어서 리스트로 반환합니다.
    '#'로 시작하는 줄(주석)은 무시합니다.
    두 파일 모두 없으면 안내 메시지를 출력하고 빈 리스트를 반환합니다.
    """
    words = []
    # 기본 단어 파일
    try:
        with open(filename, "r") as f:
            words += [word.strip().lower() for word in f if word.strip() and not word.strip().startswith("#")]
    except FileNotFoundError:
        messagebox.showwarning("파일 경고", f"기본 단어 파일 '{filename}'이 존재하지 않습니다.")
    # 사용자 추가 단어 파일
    try:
        with open(user_filename, "r") as f:
            words += [word.strip().lower() for word in f if word.strip() and not word.strip().startswith("#")]
    except FileNotFoundError:
        # 사용자 파일은 없어도 무방
        pass
    if not words:
        messagebox.showerror("파일 오류", "단어 파일을 찾을 수 없습니다.")
    return words

def pattern_to_regex(pattern: str):
    """
    워들 스타일 패턴(예: _ a _ b _)을 정규식으로 변환합니다.
    '_'는 임의의 한 글자를 의미하며, 나머지 글자는 그대로 사용됩니다.
    """
    cleaned = pattern.replace(" ", "").lower()
    return "^" + "".join("." if ch == "_" else ch for ch in cleaned) + "$"

def parse_loose_letters(input_str):
    """
    유동 글자와 해당 글자가 오면 안 되는 위치를 파싱합니다.
    예시 입력: a(1,4) b(3,4)
    결과: {'a': [0, 3], 'b': [2, 3]}  # 인덱스는 0부터 시작
    """
    if not input_str.strip():
        return {}
    pattern = r"([a-zA-Z])\(([\d,]+)\)"
    result = {}
    for match in re.finditer(pattern, input_str):
        letter = match.group(1).lower()
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
    pattern_length = len(fixed_pattern.replace(" ", ""))
    results = []
    for word in words:
        if len(word) != pattern_length:
            continue
        if not regex.match(word):
            continue
        if any(ch in word for ch in exclude_set):
            continue
        valid = True
        for letter, bad_positions in loose_map.items():
            if letter not in word:
                valid = False
                break
            if any(word[pos] == letter for pos in bad_positions if 0 <= pos < len(word)):
                valid = False
                break
        if valid:
            results.append(word)
    return results

# =========================
# UI 및 이벤트 함수
# =========================

def run_filter():
    """
    검색 버튼 클릭 시 실행되는 함수.
    입력값을 받아 단어를 필터링하고 결과를 출력합니다.
    조건이 모두 비어있으면 알파벳별로 구분자를 넣어 전체 단어 목록을 보여줍니다.
    """
    fixed_pattern = entry_pattern.get().strip()
    loose_letters = entry_loose.get().strip()
    exclude_letters = entry_exclude.get().strip()
    words = load_words("words.txt", "user_words.txt")
    if not words:
        status_label.config(text="단어 파일을 찾을 수 없습니다.")
        return

    result_text.config(state='normal')
    result_text.delete(1.0, tk.END)

    # 조건이 모두 비어있을 때: 전체 단어 알파벳별로 구분하여 출력
    if not fixed_pattern and not loose_letters and not exclude_letters:
        sorted_words = sorted(words)
        result_text.insert(tk.END, f"조건이 입력되지 않았으므로 모든 단어를 알파벳별로 보여드립니다.\n")
        result_text.insert(tk.END, f"총 단어 수: {len(sorted_words)}\n\n")
        current_letter = ""
        for word in sorted_words:
            first = word[0].upper()
            if first != current_letter:
                current_letter = first
                # 알파벳 구분자에 태그 적용
                result_text.insert(tk.END, f"\n[{current_letter}]\n", "letter_tag")
            result_text.insert(tk.END, f"{word}\n")
        # 구분자 태그 스타일(디자인 설정에서 색상 적용)
        result_text.tag_config("letter_tag", foreground=LETTER_TAG, font=("맑은 고딕", 13, "bold"))
        status_label.config(text="전체 단어 목록을 알파벳별로 표시합니다.")
        result_text.config(state='disabled')
        return

    # 기존 조건 검색
    matches = filter_words(words, fixed_pattern, loose_letters, exclude_letters)
    result_text.insert(tk.END, f"총 단어 수: {len(words)}\n")
    if matches:
        result_text.insert(tk.END, f"조건에 맞는 단어는 총 {len(matches)}개입니다!\n\n")
        for word in matches:
            result_text.insert(tk.END, f"• {word}\n")
        result_text.insert(tk.END, "\n검색이 완료되었습니다. 즐거운 워들 플레이 되세요! 🎉")
        status_label.config(text="검색이 완료되었습니다.")
    else:
        result_text.insert(tk.END, "😥 조건에 맞는 단어가 없습니다.\n")
        result_text.insert(tk.END, "오늘의 워들 정답을 알게 되면 user_words.txt 파일에 추가해 주세요!\n")
        result_text.insert(tk.END, "다음에 같은 단어가 나왔을 때 더 쉽게 찾을 수 있어요. 😉")
        status_label.config(text="조건에 맞는 단어가 없습니다.")
    result_text.config(state='disabled')

def create_labeled_entry(master, label_text, example_text, row):
    """
    라벨과 예시, 입력창을 한 줄에 배치하는 고급 입력창 생성 함수
    """
    label = tk.Label(master, text=label_text, font=LABEL_FONT, bg=PANEL_COLOR, fg=LABEL_TEXT, anchor="w")
    label.grid(row=row, column=0, sticky="w", padx=(18,8), pady=10)
    entry_style = ttk.Style()
    entry_style.configure("Custom.TEntry",
                          fieldbackground=ENTRY_BG,
                          borderwidth=0,
                          relief="flat",
                          font=("맑은 고딕", 12),
                          foreground="#222")
    entry_frame = tk.Frame(master, bg=PANEL_COLOR)
    entry_frame.grid(row=row, column=1, sticky="ew", padx=(0,0), pady=10)
    entry = ttk.Entry(entry_frame, width=22, style="Custom.TEntry", font=("맑은 고딕", 12))
    entry.pack(fill="x", ipady=7, padx=(0,0))
    entry_frame.grid_columnconfigure(0, weight=1)
    example = tk.Label(master, text=example_text, fg=EXAMPLE_TEXT, bg=PANEL_COLOR, font=("맑은 고딕", 10))
    example.grid(row=row, column=2, sticky="w", padx=(8,8))
    return entry

# =========================
# 메인 윈도우 구성
# =========================

root = tk.Tk()
root.title("워들 단어 사전")
root.geometry("560x740")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# 타이틀 및 안내
tk.Label(root, text="🎯 워들 단어 사전", font=TITLE_FONT, bg=BG_COLOR, fg=LABEL_TEXT).pack(pady=(28, 5))
tk.Label(root, text="아래 조건을 입력하고 원하는 단어를 찾아보세요!", font=("맑은 고딕", 13), bg=BG_COLOR, fg=EXAMPLE_TEXT).pack()

# 입력 패널
frame = tk.Frame(root, bg=PANEL_COLOR, bd=0, relief="flat")
frame.pack(pady=24, padx=18, fill="x")
frame.grid_columnconfigure(1, weight=1)

# 고급 입력창 생성
entry_pattern = create_labeled_entry(frame, "[1] 확정된 글자 패턴", "예시: _ a _ b _", 0)
entry_loose   = create_labeled_entry(frame, "[2] 특정 위치에는 오면 안 되는 글자", "예시: a(1,4) b(3,4)", 1)
entry_exclude = create_labeled_entry(frame, "[3] 제외할 글자들", "예시: a,b,c,d,e", 2)

# 검색 버튼
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=16)
search_btn = tk.Button(btn_frame, text="🔍 검색하기", command=run_filter, font=("맑은 고딕", 14, "bold"),
          bg=BTN_COLOR, fg=BTN_TEXT, activebackground=RESULT_BG, activeforeground=BTN_TEXT,
          relief="flat", bd=0, cursor="hand2", padx=24, pady=8)
search_btn.pack()

# 결과 출력 영역
result_frame = tk.Frame(root, bg=RESULT_BG, bd=2, relief="groove")
result_frame.pack(padx=18, pady=(0, 18), fill="both", expand=True)

result_text = scrolledtext.ScrolledText(result_frame, width=62, height=22, font=RESULT_FONT,
                                        bg=RESULT_BG, fg=RESULT_TEXT, bd=0, relief="flat", wrap="word")
result_text.pack(padx=10, pady=10, fill="both", expand=True)
result_text.config(state='disabled')

# 상태 표시줄
status_frame = tk.Frame(root, bg=BG_COLOR)
status_frame.pack(side="bottom", fill="x")

status_label = tk.Label(status_frame, text="워들 단어 필터기입니다. 단어 검색을 시작해보세요!", font=("맑은 고딕", 10),
                        bg=BG_COLOR, fg=EXAMPLE_TEXT)
status_label.pack(pady=8)

# =========================
# 프로그램 실행
# =========================

root.mainloop()
