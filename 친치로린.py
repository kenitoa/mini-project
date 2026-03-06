import random
import time

chip=100000
User_coma=0
NoEyesCount=0
money_count=0
def main(chip,User_coma):
    print("main")

def translate(chip,User_coma):
    coma=int(input("얼마나 바꾸실 건가요? (1코마 =100칩)"))
    User_coma=coma * 100
    chip-=User_coma
    count(chip, User_coma)

#칩 수량 확인
def count(chip, User_coma):
    if User_coma > chip:
        print("돈이 부족합니다. 다시 시도해주시기 바랍니다.")
        return translate(chip,User_coma)
    else:
        game(User_coma)

#게임 시작
def game(User_coma):
    user_dice=[]
    com_dice=[]
    for i in range(3):
        user=int(input("주사위 숫자 3개를 적으시오 (ex: 3->enter 키 -> 4- >enter 키 -> 5 ->enter 키): "))
        user_dice.append(user)
        user_dice.sort()
        com=random.randint(1,6)
        com_dice.append(com)
        com_dice.sort()
    print("주사위를 굴리기 시작합니다.")
    time.sleep(1)
    print("컴퓨터가 부여한 주사위의 숫자는 {}로 나왔습니다.\n 당신이 선택한 숫자는 {}입니다.".format(com_dice, user_dice))
    time.sleep(1)
    rule(com_dice, User_coma, user_dice, NoEyesCount)

#룰에 의한 결과 판독
def rule(com_dice, User_coma, user_dice, NoEyesCount):
    rule_list=["핀조로","시고로","히후미","아라시","고조로","눈 있음", "눈 없음"]
    dice_list=[1,2,3,4,5,6]
    if com_dice==[1,1,1] and user_dice==[1,1,1]:
        print("축하합니다. {}가 나왔습니다. 운이 매우 좋으시군요!".format(rule_list[0]))
        User_coma*=5
        same(chip, User_coma)
    elif com_dice==[4,5,6] and user_dice==[4,5,6]:
        print("축하합니다. {}가 나왔습니다. 운이 나쁘지 않은 편이군요!".format(rule_list[1]))
        User_coma *=2
        same(chip, User_coma)
    elif com_dice==[1,2,3] and user_dice==[1,2,3]:
        print("안타깝게도 {}가 나왔습니다. 다시 한 번 더 해봅시다.".format(rule_list[2]))
        User_coma *=0
        same(chip, User_coma)
    elif com_dice[0]== com_dice[1]==com_dice[2] and user_dice[0]==user_dice[1]==user_dice[2] and com_dice not in [[1,1,1], [5,5,5]] and all(com_dice[i] < user_dice[i] for i in range(len(com_dice))):
        print("축하합니다. {}가 나왔습니다. 운이 좋으시군요! ".format(rule_list[3]))
        User_coma *=3
        same(chip, User_coma)
    elif com_dice==[5,5,5] and user_dice==[5,5,5]:
        print("축하합니다. {}가 나왔습니다. 다음 판에는 {}가 나올 것 같아요!".format(rule_list[4],rule_list[0]))
        User_coma *=4
        same(chip, User_coma)
    elif com_dice[0]==com_dice[1] or user_dice[0]==user_dice[1] and com_dice[1]==com_dice[2] or user_dice[1]==user_dice[2] and com_dice[0]==com_dice[2] or user_dice[0]==user_dice[2]:
        if com_dice[0]==com_dice[1]==user_dice[0]==user_dice[1] and com_dice[2]==user_dice[2]==dice_list[5]:
            print("안타깝습니다. {}가 나왔지만 마지막 1개의 주사위 숫자가 6이 나왔으므로 돈을 잃었습니다.",format(rule_list[5]))
            User_coma -=User_coma *1.5
            same(chip, User_coma)
        elif com_dice[1]== com_dice[2]==user_dice[1]==user_dice[2] and com_dice[0]==user_dice[0]==dice_list[0]:
            print("안타깝습니다. {}가 나왔지만 마지막 1개의 주사위 숫자가 1이 나왔으므로 돈을 잃었습니다.",format(rule_list[5]))
            User_coma -=User_coma *1.5
            same(chip, User_coma)
        else:
            if com_dice[2]>user_dice[2] or com_dice[0]>user_dice[0]:
                print("안타깝습니다. {}이 되었지만, 주사위 마지막 숫자가 컴퓨터가 더 높으므로 돈을 잃었습니다.".format(rule_list[5]))
                User_coma -= User_coma * 2.5
                same(chip, User_coma)
            elif com_dice[2]==user_dice[2] or com_dice[0]==user_dice[0]:
                print("{}이라서 다행입니다. 돈을 잃지 않으셨군요.".format(rule_list[5]))
                same(chip, User_coma)
            elif com_dice[2]<user_dice[2] or com_dice[0] < user_dice[0]:
                print("축하합니다. {}이지만, 마지막 주사위 수가 컴퓨터 보다 크기 때문에 이겼습니다.".format(rule_list[5]))
                same(chip, User_coma)
    else:
        NoEyesCount+=1
        if NoEyesCount <3:
                print("다시 시도해봅시다.")
                game(User_coma)
        else:
            print("대단합니다! {}으로 컴퓨터와 똑같은 생각을 하셨군요!".format(rule_list[6]))
            User_coma *=1
            same(chip, User_coma)
            NoEyesCount-=3

#마무리 멘트
def same(chip, User_coma):
    answer_list=["yes", "no"]
    choose=input("다시 하시겠습니까? (yes / no)")
    if choose in answer_list[0]:
        print("가지고 있는 금액은 총 {}원입니다.".format(chip+User_coma*100))
        return translate(chip,User_coma)
    elif choose in answer_list[1]:
        print("가지고 있는 금액은 총 {}원입니다. ".format(chip+User_coma*100))
        return main(chip, money_count)