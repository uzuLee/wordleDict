import re
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from tkinter import BooleanVar

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

USE_EXTENDED_WORDS = False  # 확장 단어팩 사용 여부 설정

def load_words(filename="words.txt", user_filename="user_words.txt", extended_filename="extended_words.txt"):
    """
    기본 단어 파일, 확장 단어 파일, 사용자가 추가한 단어 파일을 모두 읽어서 리스트로 반환합니다.
    '#'로 시작하는 줄(주석)은 무시합니다.
    두 파일 모두 없으면 안내 메시지를 출력하고 빈 리스트를 반환합니다.
    """
    words = []
    
    # 확장 단어 파일 (USE_EXTENDED_WORDS가 True일 때만 사용)
    if USE_EXTENDED_WORDS:
        try:
            with open(extended_filename, "r") as f:
                words += [word.strip().lower() for word in f if word.strip() and not word.strip().startswith("#")]
        except FileNotFoundError:
            messagebox.showwarning("파일 경고", f"확장 단어 파일 '{extended_filename}'이 존재하지 않습니다.")
    
    else:
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

def parse_loose_letters(input_str):전", font=TITLE_FONT, bg=BG_COLOR, fg=LABEL_TEXT).pack(pady=(28, 5))
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
search_btn.pack(side="left", padx=(0, 12))

# 확장 단어팩 토글 스위치
USE_EXTENDED_WORDS_VAR = BooleanVar(value=USE_EXTENDED_WORDS)

toggle_switch = ttk.Checkbutton(
    btn_frame,
    text="확장 단어팩 사용",
    variable=USE_EXTENDED_WORDS_VAR,
    command=on_extended_switch,
    style="Switch.TCheckbutton"
)
toggle_switch.pack(side="left")

# 스위치 스타일(파란색 강조)
style = ttk.Style()
style.configure("Switch.TCheckbutton",
                font=("맑은 고딕", 12),
                foreground=BTN_TEXT,
                background=BG_COLOR)

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
