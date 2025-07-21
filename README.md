# 워들 단어 사전 (Wordle Word Dict)

## 소개 (Introduction)

이 프로그램은 워들(Wordle) 게임에서 사용할 수 있는 단어를 쉽게 찾아주는 필터 도구입니다.  
This program is a filter tool to easily find words that can be used in the Wordle game.

사용자는 확정된 글자 패턴, 반드시 포함되어야 하지만 특정 위치에는 오면 안 되는 글자, 그리고 제외할 글자를 입력하여 조건에 맞는 단어를 빠르게 찾을 수 있습니다.  
Users can input a fixed letter pattern, letters that must be included but not in certain positions, and letters to exclude, to quickly find words that match the conditions.

## 사용 방법 (How to Use)

1. **단어 목록 준비 (Prepare word list):**  
   [`프로그램`](wordleDict.exe)과 같은 폴더에 [`words.txt`](words.txt) 파일을 준비하세요. 각 줄마다 하나의 단어를 입력합니다.  
   Prepare a [`words.txt`](words.txt) file in the same folder as the [`program`](wordleDict.exe). Enter one word per line.

2. **프로그램 실행 (Run the program):**  
   [워들 단어 사전 프로그램](wordleDict.exe)을 실행하세요.  
   Run [Wordle Dict program](wordleDict.exe).

4. **조건 입력 (Input conditions):**  
   - **확정된 글자 패턴 (Fixed letter pattern):**  
     예시: `_ a _ b _`  
     언더바(_)는 아직 모르는 글자, 알파벳은 확정된 글자입니다.  
     Example: `_ a _ b _`  
     Underscore(_) means unknown letter, alphabet means fixed letter.
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

5. **결과 확인 (Check results):**  
   조건에 맞는 단어 목록과 개수를 출력합니다.  
   The program will print the list and count of words that match the conditions.

## 주요 함수 (Main Functions)

- [`load_words`](e:/projectFiles/programming/.orbyx%20code/wordleDict.py): 단어 목록을 파일에서 읽어옵니다.  
  Reads the word list from a file.
- [`pattern_to_regex`](e:/projectFiles/programming/.orbyx%20code/wordleDict.py): 워들 스타일 패턴을 정규식으로 변환합니다.  
  Converts Wordle-style patterns to regular expressions.
- [`parse_loose_letters`](e:/projectFiles/programming/.orbyx%20code/wordleDict.py): 유동 글자와 위치 정보를 파싱합니다.  
  Parses loose letters and their forbidden positions.
- [`filter_words`](e:/projectFiles/programming/.orbyx%20code/wordleDict.py): 모든 조건을 만족하는 단어만 필터링합니다.  
  Filters words that satisfy all conditions.

## 파일 구조 (File Structure)

- [`wordleDict.exe`](wordleDict.exe): 워들 단어 사전 실행 파일  
  Wordle Word Dict executable file
- [`wordleDict.py`](wordleDict.py): 워들 단어 사전 메인 코드  
  Main code for Wordle Word Dict
- [`words.txt`](words.txt): [단어 목록 파일(By cfreshman)](https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b#file-wordle-answers-alphabetical-txt)  
  [Word list file(By cfreshman)](https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b#file-wordle-answers-alphabetical-txt)
  - [`icon.ico`](icon.ico): [아이콘(By wikimedia commons)](https://commons.wikimedia.org/wiki/File:Book_with_Lens_Flat_Icon_Vector.svg)  
  [Icon(By wikimedia commons)](https://commons.wikimedia.org/wiki/File:Book_with_Lens_Flat_Icon_Vector.svg)

## 라이선스 (License)

이 프로젝트는 [우주웨어 라이센스](https://velog.io/@uzulee/series/License-Notice)를 따릅니다.  
This project is licensed under the [uzuware license](https://velog.io/@uzulee/series/License-Notice).
