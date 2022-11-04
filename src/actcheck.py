import copy
import json

OUT_CARD = True                    
IN_CARD = False

def init():		
	global hu_card_list, hu_info
	hu_card_list = []
	hu_info = []

def get_next_card(hand_cards):
	for card, num in enumerate(hand_cards):
		if num > 0 and card > 0:
			return card

def check_available(hand_cards, card, cards):
	if card == None:
		return False

	if card < 0 or card > 20:
		return False

	count = hand_cards[card]
	if count == 1 or count == 2:    
		return True

	if count == 3 and len(cards) >= 3 and cards[0] == card and cards[1] == card and cards[2] == card: 
		return True
	
	if count == 4 and len(cards) == 4 :
		return True

	return False

def hand_cards_put(hand_cards, cards, out):
	for card in cards:
		if out == True: 
			hand_cards[card] -= 1 
		else: 
			hand_cards[card] += 1 
		 
def get_cards_with_king(hand_cards, cards, limit, no_check_available):
	new_cards = []
	replace_cards = []
	for card in(cards):
		if check_available(hand_cards, card, cards) == True or no_check_available == True :
			new_cards.append(card)
			hand_cards[card] = hand_cards[card] - 1
			
		elif hand_cards[0] > 0:
			new_cards.append(0)
			replace_cards.append(card)
			hand_cards[0] = hand_cards[0] - 1
		
	if len(new_cards) == len(cards) and ((limit and limit(new_cards) or not limit)): 
		return new_cards, replace_cards
	else:
		hand_cards_put(hand_cards, new_cards, IN_CARD);
		new_cards = []
		replace_cards = []

	return new_cards, replace_cards

def limitShun(cards): 
    if cards[0] <= 10 and ((cards[0] > 10 and cards[1] != 0) or (cards[2] > 10 and cards[2] != 0)):
        return False
    if cards[0] > 10 and ((cards[0] <= 10 and cards[1] != 0) or (cards[2] <= 10 and cards[2] != 0)):
        return False

    return True
 
def limit_hu(hu_card_list):
	duo_number, dui_number = 0, 0
	for temp in hu_card_list:
		if len(temp['cards']) == 4:
			duo_number = duo_number + 1
		
		if len(temp['cards']) == 2: 
			dui_number = dui_number + 1
		
	if dui_number > 1 : 
		return
	
	if duo_number >= 1 and dui_number != 1 : 
		return
	
	return True

def limit_nest(cards):
	dui_number = 0
	for temp in (hu_card_list): 
		if len(temp['cards']) == 2 : 
			dui_number = dui_number + 1

	if len(cards) == 2 and dui_number > 0 : 
		return False

	return True

def get_huxi_shun(first_card):
	if first_card == 1:
		return 3
	elif first_card == 11: 
		return 6
	else:
		return 0
	
def get_huxi_kan(card):
	global front_cards, back_cards
	if card > 10:
		if front_cards[card] == 3:
			return 3
		return 6
	else:
		if front_cards[card] == 3:
			return 1
		return 3
		
def get_huxi_duo(card):
	global front_cards, back_cards
	if card > 10:
		if front_cards[card] == 3:
			return 9
		return 12
	else:
		if front_cards[card] == 3:
			return 6
		return 9
		
def card_duo(card, hand_cards):
	new_cards, replace_cards = get_cards_with_king(hand_cards, [card, card, card, card], None, None)
	if len(new_cards) != 0: 
		#print("->  card_duo ",card,"			", new_cards)
		return True, new_cards, replace_cards, get_huxi_duo(card)
	return False, [], [], 0

def card_kan(card, hand_cards):
	new_cards, replace_cards = get_cards_with_king(hand_cards, [card, card, card], None, None)
	if len(new_cards) != 0:
		#print("->  card_kan ",card,"			", new_cards)
		return True, new_cards, replace_cards, get_huxi_kan(card)
	return False, [], [], 0

def card_shun(card, hand_cards):
	new_cards, replace_cards = get_cards_with_king(hand_cards, [card - 2, card -1, card], limitShun, None)
	if len(new_cards) != 0: 
		#print("->  card_shun ",card,"			", new_cards)
		return True, new_cards, replace_cards, get_huxi_shun(card - 2)
	return False, [], [], 0

def card_shun_1(card, hand_cards):
	new_cards, replace_cards = get_cards_with_king(hand_cards, [card - 1, card , card + 1], limitShun, None)
	if len(new_cards) != 0:  
		#print("->  card_shun_1 ",card,"			", new_cards)
		return True, new_cards, replace_cards, get_huxi_shun(card - 1)
	return False, [], [], 0

def card_shun_2(card, hand_cards):
	new_cards, replace_cards = get_cards_with_king(hand_cards, [card, card + 1 , card + 2], limitShun, None);
	if len(new_cards) != 0: 
		#print("->  card_shun_2 ",card,"			", new_cards)
		return True, new_cards, replace_cards, get_huxi_shun(card)
	return False, [], [], 0

def card_da(card, hand_cards):
	if card <= 10 :
		new_cards, replace_cards = get_cards_with_king(hand_cards, [card, card + 10 , card + 10], None, None)
	else:
		new_cards, replace_cards = get_cards_with_king(hand_cards, [card, card - 10 , card - 10], None, None)
	
	if len(new_cards) != 0: 
		#print("->  card_da ",card,"			", new_cards)
		return True, new_cards, replace_cards, 0
	return False, [], [], 0

def card_da_1(card, hand_cards):
	if card <= 10 :
		new_cards, replace_cards = get_cards_with_king(hand_cards, [card, card, card + 10], None, None)
	else:
		new_cards, replace_cards = get_cards_with_king(hand_cards, [card, card, card - 10], None, None)
	
	if len(new_cards) != 0: 
		#print("->  card_da_1 ",card,"			", new_cards)
		return True, new_cards, replace_cards, 0
	return False, [], [], 0

def card_2_7_10(card, hand_cards):
	if card == 2 or card == 7 or card == 10 : 
		new_cards, replace_cards = get_cards_with_king(hand_cards, [2, 7, 10], None, None);
		if len(new_cards) != 0: 
			#print("->  card_2_7_10 ",card,"			", new_cards)
			return True, new_cards, replace_cards, 3
	return False, [], [], 0

def card_12_17_20(card, hand_cards):
	if card == 12 or card == 17 or card == 20 : 
		new_cards, replace_cards = get_cards_with_king(hand_cards, [12, 17, 20], None, None);
		if len(new_cards) != 0: 
			#print("->  card_12_17_20 ",card,"			", new_cards)
			return True, new_cards, replace_cards, 6
	return False, [], [], 0

def card_dui(card, hand_cards):
	new_cards, replace_cards = get_cards_with_king(hand_cards, [card, card], None, None);
	if len(new_cards) != 0: 
		#print("->  card_dui ",card,"			", new_cards)
		return True, new_cards, replace_cards, 0
	return False, [], [], 0	

def get_hand_cards_nest(hand_cards):
    global hu_card_list
    def check_card_repeat(card, hand_cards):
        for fun in fun_list:
            nest, cards, replace_cards, huxi = fun(card, hand_cards);
            if nest == True :
                #print('nest', card)
                if limit_nest(cards):
                    #print('limit_nest', card)
                    hu_card_list.append({'cards': cards, 'replace_cards': replace_cards, 'huxi': huxi})
                    if True != get_hand_cards_nest(hand_cards) :
                        hand_cards_put(hand_cards, cards, IN_CARD)
                        hu_card_list.pop()
                else:
                    hand_cards_put(hand_cards, cards, IN_CARD);

    checkcard = get_next_card(hand_cards)
    #print('checkcard ', checkcard)
    if checkcard:
        return check_card_repeat(checkcard, hand_cards)
    elif limit_hu(hu_card_list) == True : 
        hu_info.append(copy.deepcopy(hu_card_list))
        #print("hu ------------------", len(hu_info))
        #print(hu_info)
   
def insert_desk_cards(hand_cards, desk_front_cards, desk_back_cards):
	global front_cards, back_cards
	new_hand_cards = [0 for i in range(21)]
	new_hand_cards[0] = 1
	for card in (hand_cards) : 
		new_hand_cards[card] = new_hand_cards[card] + 1
	
	for cards in desk_front_cards : 
		if (len(cards) == 3 or len(cards) == 4) and cards[0] == cards[1] and cards[0] == cards[2] : 
			new_hand_cards[cards[0]] = new_hand_cards[cards[0]] + len(cards)
			front_cards[cards[0]] = len(cards) 

	for cards in desk_back_cards : 
		new_hand_cards[cards[0]] = new_hand_cards[cards[0]] + len(cards)
		back_cards[cards[0]] = len(cards)
		
	return new_hand_cards

def get_desk_card_huxi(desk_front_cards):
	huxi = 0
	for cards in desk_front_cards : 
		if len(cards) == 3 and ((cards[0] == 1 and cards[1] == 2 and cards[2] == 3) or (cards[0] == 2 and cards[1] == 7 and cards[2] == 10)) : 
			huxi = huxi + 3
		
		if len(cards) == 3 and ((cards[0] == 11 and cards[0] == 12 and cards[0] == 13) or (cards[0] == 12 and cards[1] == 17 and cards[2] == 20)) : 
			huxi = huxi + 6
	
	return huxi

def format_desk_cards(desk_front_cards, desk_back_cards, info):
	global front_cards, back_cards
	hand_cards = []
	desk_front_cards = copy.deepcopy(desk_front_cards)
	desk_back_cards = copy.deepcopy(desk_back_cards)
	for detail in info : 
		#先将0还原为对应的牌
		if len(detail['replace_cards']) > 0 : 
			zeroIndex = None
			for index, card in enumerate(detail['cards']) :
				if card == 0 : 
					zeroIndex = index
			if zeroIndex != None :
				detail['cards'][zeroIndex] = detail['replace_cards'][0]
		
		#收集新的手牌
		if len(detail['cards']) == 2 : 
			hand_cards.append(detail['cards']) 
		
		if len(detail['cards']) == 3 : 
			if detail['cards'][0] == detail['cards'][1] and detail['cards'][0] == detail['cards'][2] : 
				if back_cards[detail['cards'][0]] == 0 and not front_cards[detail['cards'][0]] : 
					hand_cards.append(detail['cards'])
			else:
				hand_cards.append(detail['cards'])
		 
		if len(detail['cards']) == 4 : 
			if back_cards[detail['cards'][0]] > 0: 
				for index, cards in enumerate(desk_back_cards) : 
					if (len(cards) == 4 or len(cards) == 3) and cards[0] == detail['cards'][0] : 
						desk_back_cards[index] = detail['cards']
						
			elif front_cards[detail['cards'][0]] > 0 : 
				for index, cards in enumerate(desk_front_cards) : 
					if (len(cards) == 4 or len(cards) == 3) and cards[0] == detail['cards'][0] : 
						desk_front_cards[index] = detail['cards']	
			else:
				hand_cards.append(detail['cards'])	
			
	return {'hand_cards' : hand_cards, 'desk_front_cards' : desk_front_cards, 'desk_back_cards' : desk_back_cards}

def format_hu_info(desk_front_cards, desk_back_cards, desk_card_huxi, hu_count_line, put_card):
	data = []
	for info in hu_info : 
		total_huxi, ting_card, change_huxi = desk_card_huxi or 0, None, None
		for detail in info :
			total_huxi += detail['huxi']
			if len(detail['replace_cards']) > 0 : 
				ting_card = detail['replace_cards'][0]
				if len(detail['cards']) >= 3 and detail['cards'][0] == ting_card and detail['cards'][1] == ting_card : 
					change_huxi = detail['huxi']
				
		if hu_count_line <= total_huxi and ting_card != put_card:
			data.append({'change_huxi' : change_huxi, 'huxi' : total_huxi, 'ting_card' : ting_card, 'cards' : format_desk_cards(desk_front_cards, desk_back_cards, info)})
	
	data.sort(key=lambda x: (x["huxi"]), reverse = True)	
	return data

def reset_hand_cards(hand_cards):
	new_hand_cards = get_hand_cards(hand_cards)
	fun_shun = [
		card_shun,
		card_shun_1,
		card_shun_2
	]
	print("show new_hand_cards in reset_hand_cards", new_hand_cards)
	for card in hand_cards:
		if new_hand_cards[card] == 2:
			for fun in fun_shun:
			 	nest, new_cards, replace_cards, huxi = fun(card, copy.deepcopy(new_hand_cards))
			 	if nest == True and huxi == 0:
			 		new_hand_cards[card] = 0
			 		break

	hand_cards = []
	for card, num in enumerate(new_hand_cards):
		for i in range(num):
			hand_cards.append(card)

	print("show new hand_cards ", hand_cards)
	return hand_cards

def check_ting_for_putcard(hand_cards, desk_front_cards, desk_back_cards, hu_count_line = 15):
	global front_cards, back_cards
	init()
	back_cards = [0 for i in range(21)]
	front_cards = [0 for i in range(21)]
	return_data = []
	new_hand_cards = insert_desk_cards(hand_cards, desk_front_cards, desk_back_cards)
	for card, number in enumerate(new_hand_cards):
		temp_hand_cards = copy.deepcopy(new_hand_cards)
		desk_card_huxi = get_desk_card_huxi(desk_front_cards)
		if number > 0 and number < 3 and card > 0 : 
			global hu_info
			hu_info = []
			temp_hand_cards[card] -= 1
			#print("hand_cards put_card ",card)
			get_hand_cards_nest(temp_hand_cards)
			format_data = format_hu_info(desk_front_cards, desk_back_cards, desk_card_huxi, hu_count_line, card)
			if len(format_data) > 0 : 
				return_data.append({'put_card': card, "format_data": format_data})
	
	return_data.sort(key=lambda x: (len(x["format_data"]), x["format_data"][0]["huxi"]), reverse = True)		
	print("tinghu result  --->>> \n", return_data)
	if len(return_data) == 0:
		#没听不拆无子对
		hand_cards = reset_hand_cards(hand_cards)

	return return_data, hand_cards


def check_ting(hand_cards, desk_front_cards, desk_back_cards, hu_count_line = 15):
	global front_cards, back_cards
	init()
	back_cards = [0 for i in range(21)]
	front_cards = [0 for i in range(21)]
	return_data = []
	new_hand_cards = insert_desk_cards(hand_cards, desk_front_cards, desk_back_cards)
	
	temp_hand_cards = copy.deepcopy(new_hand_cards)
	desk_card_huxi = get_desk_card_huxi(desk_front_cards)
	get_hand_cards_nest(temp_hand_cards)
	format_data = format_hu_info(desk_front_cards, desk_back_cards, desk_card_huxi, hu_count_line, 0)
	if len(format_data) > 0 : 
		return_data.append({'put_card': 0, "format_data": format_data})
	
	return_data.sort(key=lambda x: (len(x["format_data"]), x["format_data"][0]["huxi"]), reverse = True)		
	print("tinghu result not put card --->>> \n", return_data)
	
	return return_data, hand_cards


def check_san_card_number(hand_cards):
	san_card_number = 0
	for card, num in enumerate(hand_cards):
		if num > 0 and num < 3:
			isNest = False
			for fun in fun_list:
				isNest, new_cards, replace_cards, huxi = fun(card, hand_cards)
				if isNest == True:
					break
			if isNest == False:
				san_card_number += 1

	return 	san_card_number		


#检查牌型方法 根据不同游戏规则定义增减
fun_list = [
	card_duo,
	card_kan,
	card_shun,
	card_shun_1,
	card_shun_2,
	card_12_17_20,
	card_2_7_10,
	card_da,
	card_da_1,
	card_dui, 
]

def get_hand_cards(cards):
	hand_cards = [0 for i in range(21)]
	for card in cards:
		hand_cards[card] += 1
	return hand_cards

def main():
	test_cards = [
		18, 18, 18, 12,12,12,10,10,20,13,14,6
	]
	desk_front_cards = [
		[19,19,19],
		[5,5,15],
		[3,4,5],
	]
	desk_back_cards = [
		#[20,20,20,20],
	]
	
	ting_data = check_ting_for_putcard(test_cards, desk_front_cards, desk_back_cards)
	# ting_data = check_ting(test_cards, desk_front_cards, desk_back_cards)
	#ting_data.sort(key=lambda x: (len(x["format_data"])), reverse = True)
	print("\n")
	print(json.dumps(ting_data))

	return ting_data
if __name__ == '__main__':
	main()


	
	

