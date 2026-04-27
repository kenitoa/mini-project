import random
import time

token = 100


# 메인 화면-완료
def main():
    print("게임 랜드에 오신 것을 환영합니다.")
    time.sleep(1)
    answer2 = input("어떤 게임을 하고 싶습니까? (1. 로또 / 2. 가위바위보 / 3. 원카드 / 4. 토큰 개수 확인)")
    if answer2 == "1" or answer2 == "로또":
        return lotto()
    elif answer2 == "2" or answer2 == "가위바위보":
        return rsp()
    elif answer2 == "3" or answer2 == "원카드":
        return one_card()
    else:
        money_question = input("token 개수를 확인하시겠습니까? (yes/no)")
        if money_question == "yes":
            money()
        else:
            return main()


# 토큰 개수 확인-완료
def money():
    global token
    print("현재 가지고 있는 토큰의 개수: {} ".format(token))


# 로또 배팅- 완료
def lotto():
    global token
    print("로또 배팅에 오신 것을 환영합니다.")
    time.sleep(1)
    tuto = input("본 게임에 임하기 앞서 튜토리얼을 진행하려고 합니다.\n 튜토리얼을 진행하시겠습니까? (1. yes/ 2. no)")
    if tuto == "1" or tuto.lower() == "yes":  # lower()로 사용자가 대소문자 구분 없이 입력할 때 정상적으로 인식되게 해줌
        senario1()
    else:
        for i in range(6):
            answer = int(input("정수 입력: "))
            User = list[answer]
            number = random.randint
            computer = list[number]

            if (computer == User):
                print("축하합니다. 보유하고 계신 token의 10배를 획득하셨습니다.")
                token *= 10
                repeat()
            else:
                print("실패하셨습니다. 현재 token에서 -10을 하겠습니다.")
                token -= 2
                repeat()


# 가위바위보-완료
def rsp():
    global token
    print("가위바위보 게임에 오신 것을 환영합니다.")
    time.sleep(1)
    tuto2 = input("본 게임에 임하기 앞서 튜토리얼을 진행하려고 합니다.\n 튜토리얼을 진행하시겠습니까? (1. yes/ 2. no)")
    if tuto2 == "1" or tuto2.lower("yes"):
        senario2()
    elif tuto2 == "2" or tuto2.lower("no"):
        rsplist = ["가위", "바위", "보"]
        User2 = input("가위/바위/보")
        computer2 = random.rsplist(0, 2)

        if (User2 > computer2):
            token *= 3
            print("축하합니다. 가지고 있는 토큰의 3배를 따셨습니다.")
            repeat()
        elif (User2 == computer2):
            print("비겼습니다. 처음부터 다시 한 번 진행합니다.")
            rsp()
        else:
            print("졌습니다. 15 token이 차단됩니다.")
            token -= 15
            repeat()
    else:
        print("다시 한 번 시도해주시기 바랍니다.")
        return rsp()


# 원카드-계속 작성
def one_card():
    global token
    # 카드 덱 형성
    print("원카드 게임에 오신 것을 환영합니다.")
    time.sleep(1)
    tuto3 = input("튜토리얼을 진행하시겠습니까? (1. yes / 2. no)")
    if tuto3 == "1" or tuto3.lower("yes"):
        senario3()
    else:
        cards = {
            "Two of Clubs": 2, "Three of Clubs": 3, "Four of Clubs": 4, "Five of Clubs": 5, "Six of Clubs": 6,
            "Seven of Clubs": 7, "Eight of Clubs": 8, "Nine of Clubs": 9, "Ten of Clubs": 10, "Jack of Clubs": 11,
            "Queen of Clubs": 12, "King of Clubs": 13, "Ace of Clubs": 14,
            "Two of Diamonds": 2, "Three of Diamonds": 3, "Four of Diamonds": 4, "Five of Diamonds": 5,
            "Six of Diamonds": 6, "Seven of Diamonds": 7, "Eight of Diamonds": 8, "Nine of Diamonds": 9,
            "Ten of Diamonds": 10, "Jack of Diamonds": 11, "Queen of Diamonds": 12, "King of Diamonds": 13,
            "Ace of Diamonds": 14,
            "Two of Hearts": 2, "Three of Hearts": 3, "Four of Hearts": 4, "Five of Hearts": 5, "Six of Hearts": 6,
            "Seven of Hearts": 7, "Eight of Hearts": 8, "Nine of Hearts": 9, "Ten of Hearts": 10, "Jack of Hearts": 11,
            "Queen of Hearts": 12, "King of Hearts": 13, "Ace of Hearts": 14,
            "Two of Spades": 2, "Three of Spades": 3, "Four of Spades": 4, "Five of Spades": 5, "Six of Spades": 6,
            "Seven of Spades": 7, "Eight of Spades": 8, "Nine of Spades": 9, "Ten of Spades": 10, "Jack of Spades": 11,
            "Queen of Spades": 12, "King of Spades": 13, "Ace of Spades": 14
        }

        user3 = []  # 사용자가 가질 카드
        computer3 = []  # 컴퓨터가 가질 카드

        for i in range(7):
            selected_cards = random.choice(cards)
            user3_card = cards.pop()
            computer3_card = cards.pop()

            if user3[i] == computer3[i]:
                user3.append(user3_card)
                computer3.append(computer3_card)
            print("현재 받은 카드: ", user3)


# 게임 진행 이후- 완료
def repeat():
    question2 = input("계속 진행하시겠습니까? (1. yes / 2. no)")
    if (question2.lower("yes") or question2 == 1):
        question3 = input("어떤 게임을 하시겠습니까? (1. 로또 배팅 2.가위바위보 3.원카드 게임)")
        if (question3 == "1" or question3 == "로또 배팅"):
            lotto()
        elif (question3 == "2" or question3 == "가위바위보"):
            rsp()
        elif (question3 == "3" or question3 == "원카드 게임"):
            one_card()
        else:
            print("죄송합니다. 다시 입력해 주시기 바랍니다.")
            repeat()
    elif (question2.lower("no") or question3 == 2):
        print("종료하겠습니다. 이용해주셔서 감사합니다.")
        time.sleep(1)
        exit()


# lotto 게임에 대한 룰-완료
def senario1():
    print("이 게임의 튜토리얼을 설명하도록 하겠습니다.")
    time.sleep(1)
    print("사용자는 6개의 번호를 적고 엔터키를 입력한 후 ")
    time.sleep(1)
    print("컴퓨터가 랜덤으로 부여하는 6개의 번호를 대조하여 맞으면 총 token 개수의 10배를 줍니다.")
    time.sleep(1)
    print("만약, 컴퓨터의 숫자와 참가자의 숫자가 다르다면")
    time.sleep(1)
    print("질 때마다 token 10개씩 줄어듭니다.")
    time.sleep(1)

    question4 = input("튜토리얼을 종료하시겠습니까? (yes)")
    if question4 == "yes":
        lotto()
    else:
        print("다시 입력해주시기 바랍니다.")
        senario1()


# rsp 게임에 대한 룰-완료
def senario2():
    print("이 게임의 튜토리얼은 다음과 같습니다.")
    time.sleep(1)
    print("사용자가 가위, 바위, 보 중에 한 가지를 골라 입력하신 후")
    time.sleep(1)
    print("컴퓨터가 낸 것과 비교하여 이긴 쪽이 token을 현재 가지고 있는 개수의 3배를 줍니다.")
    time.sleep(1)
    print("만약 졌을 시, 진 판 마다 15개 씩 차감합니다.")

    question5 = input("튜토리얼을 종료하시겠습니까? (yes)")
    if question5.lower("yes"):
        rsp()
    else:
        print("다시 입력해주시기 바랍니다.")
        senario2()


# one-card 게임에 대한 룰-완료
def senario3():
    print("총 52장의 카드가 준비되어있습니다.")
    time.sleep(1)
    print("컴퓨터와 사용자에게 각각 7장 씩 카드가 준비되어 있습니다.")
    time.sleep(1)
    print("사용자는 자신의 패를 확인하고, 세팅된 카드를 봅니다.")
    time.sleep(1)
    print("만약 클로버 3이 나왔다고 하면, 다이아몬드 3, 하트 3, 스페이드 3과 같이 숫자만 같은 다른 종류의 카드를 낼 수 있거나")
    time.sleep(1)
    print("클로버 4, 클로버 5,...클로버 10 등 같은 모양을 가진 카드를 낼 수 있습니다.")
    time.sleep(1)
    print("이 과정에서 사용자의 손에 카드가 없다면 승리한 것이며, 카드가 20장이 넘어가면 패배한 것으로 간주됩니다.")
    time.sleep(1)
    print("이 판에서 승리시 가지고 있는 token 개수의 20배를 드리며, 질 경우 token개수의 50개 씩 차감합니다.")

    question6 = input("튜토리얼을 종료하시겠습니까? (yes)")
    if question6.lower("yes"):
        rsp()
    else:
        print("다시 입력해주시기 바랍니다.")
        senario3()


main()