# The Word Game
import random
VOWELS = 'aeiou'
ALPHABETS = 'abcdefghijklmnopqrstuvwxyz'
HAND_SIZE = 7
LETTER_VALUES = {
'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i':
1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1,
's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}
# -----------------------------------
# Helper code
# 이미 구현된 코드이며, 독스트링을 읽어서 사용 방법을 알아두세요.
WORDLIST_FILENAME = "data/words.txt"
def loadWords() -> list[str]:
    """
    유효한 단어 목록을 반환합니다. 단어는 소문자로 구성된 문자열입니다.
    이 함수가 완료되는 데 시간이 걸릴 수 있습니다.
    """
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    wordList = []
    for line in inFile:
    wordList.append(line.strip().lower())
    print(" ", len(wordList), "words loaded.")
    return wordList
def getFrequencyDict(sequence: str) -> dict[str, int]:
    """
    키가 sequence의 각 문자이고 값이 문자가 반복되는 횟수를 나타내는 정수인 사전을
    반환합니다.
    """
    freq = {}
    for x in sequence:
    freq[x] = freq.get(x,0) + 1
    return freq
# (end of helper code)
# -----------------------------------
#
# Problem #1: Word Scores
#
def getWordScore(word: str, n: int) -> int:
    """
    단어의 점수를 반환합니다. 해당 단어가 유효한 단어라고 가정합니다.
    [점수 규칙]에 따라 점수를 계산합니다.
    """
    # TO DO ...
    # -----------------------------------
    # Helper code
    # 이미 구현된 코드이며, 독스트링을 읽어서 사용 방법을 알아두세요.
def displayHand(hand: dict[str, int]) -> None:
    """
    hand에 있는 글자를 출력합니다.
    Example:
    >>> displayHand({'a':1, 'x':2, 'l':3, 'e':1})
    a x x l l l e
    출력 순서는 중요하지 않습니다.
    """
    for letter in hand.keys():
    for j in range(hand[letter]):
    print(letter,end=" ")
    print()
    def dealHand(n: int) -> dict[str, int]:
    """
    n개의 소문자를 포함하는 임의의 hand(패)를 반환합니다.
    hand 중 최소 n/3(내림)개 문자는 모음입니다.
    hand는 딕셔너리로 표현됩니다.
    키(key)는 문자이고 값(value)은 해당 hand에 포함된 특정 문자의 개수입니다.
    """
    hand={}
    numVowels = n // 3
    for i in range(numVowels):
    x = VOWELS[random.randint(0, len(VOWELS)-1)]
    hand[x] = hand.get(x, 0) + 1
    for i in range(numVowels, n):
    x = ALPHABETS[random.randint(0, len(ALPHABETS)-1)]
    hand[x] = hand.get(x, 0) + 1
    return hand
# (end of helper code)
# -----------------------------------
#
# Problem #2: Dealing with Hands
#
def updateHand(hand: dict[str, int], word: str) -> dict[str, int]:
    """
    'hand'에 word의 모든 글자가 있다고 가정합니다.
    즉, 'word'에 글자가 몇 번 나타나든 'hand'에는 최소한 'word'에 있는 글자만큼의
    글자가 있다고 가정합니다.
    hand를 업데이트합니다. 주어진 단어의 글자를 모두 사용한 상태의 새 딕셔너리를
    반환합니다.
    주의: 매개변수 hand를 수정하지 않습니다.
    """
    # TO DO ...
    #
    # Problem #3: Valid Words
    #
def isValidWord(word: str, hand: dict[str, int], wordList: list[str]) ->bool:
    """
    word가 wordList에 있고, word가 hand에 있는 문자로 구성된 경우 True를
    반환합니다.
    그렇지 않으면 False를 반환합니다.
    주의: hand 또는 wordList를 변경하지 않습니다.
    """
# TO DO ...
#
# Problem #4: Playing a hand
#
def calculateHandLen(hand: dict[str, int]) -> int:
    """
    현재 hand(패)의 길이(문자 수)를 반환합니다.
    """
    # TO DO ...
    #
    # Problem #5: Playing a Hand
    #
def playHand(hand: dict[str, int], wordList: list[str], n: int) -> None:
    """
    사용자가 다음과 같이 주어진 패(hand)를 플레이할 수 있도록 합니다.
    * 패(hand)가 표시됩니다.
    * 사용자는 단어나 마침표(문자열 ".")를 입력합니다.
    * 잘못된 단어를 입력하면 유효하지 않음이 표시되고, 다시 단어를 선택하라는 메시지가
    표시됩니다.
    * 유효한 단어를 입력하면 패(hand)의 글자가 사용(소모)됩니다.
    * 유효한 단어가 입력되면 해당 단어의 점수와 총점수가 표시되고, 패에 남은 글자가
    표시되며, 사용자에게 다시 단어를 입력하라고 요청합니다.
    * 사용되지 않은 글자가 더 이상 없거나 사용자가 "."을 입력하면 패가 종료됩니다.
    * 사용되지 않은 글자가 더 이상 없어서 종료된 경우 문자들을 모두 사용했다는 것을
    표시합니다.
    * 패(hand)가 끝나면 단어 점수의 합계가 표시됩니다.
    출력할 메시지는 과제 안내문 2쪽의 Sample Output을 참고하세요.
    """
# TO DO ...
#
# Problem #6: Playing a game
#
def playGame(wordList: list[str]) -> None:
    """
    사용자가 임의의 수의 패(hand)를 플레이하도록 허용합니다.
    1) 사용자에게 'n', 'r' 또는 'e'를 입력하도록 요청합니다.
    * 사용자가 'n'을 입력하면 새로운 (무작위) 패를 플레이합니다.
    * 사용자가 'r'을 입력하면 마지막 패를 다시 플레이합니다.
    * 사용자가 'e'를 입력하면 게임(프로그램)을 종료합니다.
    * 사용자가 다른 것을 입력하면 입력이 잘못되었다("Invalid command.")고
    알립니다.
    2) 플레이를 마치면 1단계부터 반복합니다.
    """
# TO DO ...
print("playGame not yet implemented.") # <-- 함수 구현 후 지워주세요.
#
# Main Code
#
if __name__ == '__main__':
    random.seed(7) # 재현 가능한 테스트를 위한 코드입니다. 지우지 마세요.
    wordList = loadWords()
    playGame(wordList)