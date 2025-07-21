# 워들 단어 사전 (Wordle Word Dict)

## 소개 (Introduction)

이 프로그램은 워들(Wordle) 게임에서 사용할 수 있는 단어를 쉽게 찾아주는 필터 도구입니다.  
This program is a filter tool to easily find words that can be used in the Wordle game.

사용자는 확정된 글자 패턴, 반드시 포함되어야 하지만 특정 위치에는 오면 안 되는 글자, 그리고 제외할 글자를 입력하여 조건에 맞는 단어를 빠르게 찾을 수 있습니다.  
Users can input a fixed letter pattern, letters that must be included but not in certain positions, and letters to exclude, to quickly find words that match the conditions.

## 주요 기능 (Main Features)

- 기본 워들 단어 목록과 사용자가 추가한 단어 목록을 모두 지원합니다.  
  Supports both the default Wordle word list and user-added word list.
- 입력 조건에 따라 단어를 빠르게 필터링합니다.  
  Quickly filters words based on input conditions.
- 조건을 입력하지 않으면 모든 단어를 알파벳 순으로 보여줍니다.  
  Shows all words in alphabetical order if no conditions are entered.
- 결과를 GUI로 보기 쉽게 출력합니다.  
  Displays results in an easy-to-read GUI.
- 단어장 파일에서 `#`으로 시작하는 줄은 주석으로 간주되어 검사되지 않습니다.  
  Lines starting with `#` in the word list files are treated as comments and are not checked.

## 사용 방법 (How to Use)

1. **단어 목록 준비 (Prepare word list):**  
   [`wordleDict.exe`](wordleDict.exe)와 같은 폴더에 [`words.txt`](words.txt)와 [`user_words.txt`](user_words.txt) 파일을 준비하세요. 각 줄마다 하나의 단어를 입력합니다.  
   Prepare [`words.txt`](words.txt) and [`user_words.txt`](user_words.txt) files in the same folder as [`wordleDict.exe`](wordleDict.exe). Enter one word per line.

2. **프로그램 실행 (Run the program):**  
   [`wordleDict.exe`](wordleDict.exe)를 실행하세요.  
   Run [`wordleDict.exe`](wordleDict.exe).

3. **조건 입력 (Input conditions):**  
   - **확정된 글자 패턴 (Fixed letter pattern):**  
     예시: `_ a _ b _`  
     언더바(\_)는 아직 모르는 글자, 알파벳은 확정된 글자입니다.  
     Example: `_ a _ b _`  
     Underscore(\_) means unknown letter, alphabet means fixed letter.
   - **유동 글자 입력 (Loose letter input):**  
     예시: `a(1,4) b(3,4)`  
     a는 1,4번째에 오면 안 되고, b는 3,4번째에 오면 안 됩니다.  
     Example: `a(1,4) b(3,4)`  
     'a' must not be in positions 1 and 4, 'b' must not be in positions 3 and 4.
   - **제외 글자 입력 (Exclude letters):**  
     예시: `a,d,e,i,s,y`  
     입력한 글자가 포함된 단어는 제외됩니다.  
     Example: `a,d,e,i,s,y`  
     Words containing these letters will be excluded.

4. **결과 확인 (Check results):**  
   조건에 맞는 단어 목록과 개수를 출력합니다.  
   The program will print the list and count of words that match the conditions.  
   조건을 입력하지 않으면 모든 단어를 알파벳 순으로 보여줍니다.  
   If no conditions are entered, all words will be shown in alphabetical order.

## 주요 함수 (Main Functions)

- [`load_words`](wordleDict.py): `words.txt`와 `user_words.txt`에서 단어 목록을 읽어옵니다.  
  Reads the word list from `words.txt` and `user_words.txt`.
- [`pattern_to_regex`](wordleDict.py): 워들 스타일 패턴을 정규식으로 변환합니다.  
  Converts Wordle-style patterns to regular expressions.
- [`parse_loose_letters`](wordleDict.py): 유동 글자와 위치 정보를 파싱합니다.  
  Parses loose letters and their forbidden positions.
- [`filter_words`](wordleDict.py): 모든 조건을 만족하는 단어만 필터링합니다.  
  Filters words that satisfy all conditions.

## 파일 구조 (File Structure)

- [`wordleDict.exe`](wordleDict.exe): 워들 단어 사전 실행 파일  
  Wordle Word Dict executable file
- [`wordleDict.py`](wordleDict.py): 워들 단어 사전 메인 코드  
  Main code for Wordle Word Dict
- [`words.txt`](words.txt): 기본 단어 목록 파일  
  Default word list file
- [`user_words.txt`](user_words.txt): 사용자 추가 단어 목록 파일  
  User-added word list file
- [`icon.ico`](icon.ico): 아이콘 파일  
  Icon file

## 라이선스 (License)

이 프로젝트는 [우주웨어 라이센스](https://velog.io/@uzulee/series/License-Notice)를 따릅니다.  
This project is licensed under the [uzuware license](https://velog.io/@uzulee/series/License-Notice).
