'''{
	card_current: 0,
	cards_info:
	[
		{
		hand_cards:[],
		desk_front_cards:[],     #上家牌信息
		desk_back_cards:[],
		discard_cards:[]
		},
		{
		hand_cards:[],
		desk_front_cards:[],	 #当前玩家牌信息	
		desk_back_cards:[],
		discard_cards:[]
		},
		{
		hand_cards:[],
		desk_front_cards:[],	 #下家牌信息		
		desk_back_cards:[],
		discard_cards:[]
		}
	]
	}
'''
# 我的盖牌: 1-10  10 	0   
# 我的盖牌: 1-10  11	1
# 我的手牌: 1-10  8 	2
# 我的手牌: 1-10  9		3

# 我的弃牌：1-10  14	4	
# 我的弃牌：1-10  15	5
# 我的手牌: 1-10  8 	6
# 我的手牌: 1-10  9		7

# 上家明牌：1-10  4 	8
# 上家明牌：1-10  5		9
# 我的手牌: 1-10  8 	10
# 我的手牌: 1-10  9		11

# 下家明牌：1-10  20	12
# 下家明牌：1-10  21	13
# 我的手牌: 1-10  8 	14
# 我的手牌: 1-10  9		15

# 上家弃牌：1-10  6		16
# 上家弃牌：1-10  7		17
# 我的手牌: 1-10  8 	18
# 我的手牌: 1-10  9		19

# 下家弃牌：1-10  22	20
# 下家弃牌：1-10  23	21
# 我的手牌: 1-10  8 	22
# 我的手牌: 1-10  9		23

# 我的明牌：1-10  12	24
# 我的明牌：1-10  13	25
# 我的手牌: 1-10  8 	26
# 我的手牌: 1-10  9		27

# 桌面当前牌：1-10      28
# 桌面当前牌：11-20     29
# 我的手牌: 1-10  8 	30
# 我的手牌: 1-10  9		31

import numpy as np 

def formatCards_up(cards, cur_card = False, act_name = 'chu'):
	fm_cards = [[0,0,0,0] for i in range(13)]
	for card in (cards):
		if card > 10:
			index = fm_cards[card - 10 - 1 + 3].index(0)
			fm_cards[card - 10 - 1 + 3][index] = 1
			if act_name == 'peng':
				if card == 12 and True != cur_card:
					index = fm_cards[0].index(0)
					fm_cards[0][index] = 1
				if card == 17 and True != cur_card:
					index = fm_cards[1].index(0)
					fm_cards[1][index] = 1
				if card == 20 and True != cur_card:
					index = fm_cards[2].index(0)
					fm_cards[2][index] = 1	
	#print("show allInputs shape",fm_cards)				
	return fm_cards	

def formatCards_down(cards, cur_card = False, act_name = 'put'):
		fm_cards = [[0,0,0,0] for i in range(13)]
		for card in (cards):
			if card <= 10:
				index = fm_cards[card - 1 + 3].index(0)
				fm_cards[card - 1 + 3][index] = 1
				if act_name == 'peng':
					if card == 2 and True != cur_card:
						index = fm_cards[0].index(0)
						fm_cards[0][index] = 1
					if card == 7 and True != cur_card:
						index = fm_cards[1].index(0)
						fm_cards[1][index] = 1
					if card == 10 and True != cur_card:
						index = fm_cards[2].index(0)
						fm_cards[2][index] = 1	
		#print("show allInputs shape",fm_cards)				
		return fm_cards

def formate_cards(cards):
	hand_cards = [0 for i in range(20)]
	for card in cards:
		hand_cards[card - 1] += 1
	return hand_cards

def formate_data(data, act_name):
	
	hand_cards_cur_card_num = 0 

	if act_name == "peng" or act_name == "chi" :
		hand_cards = data['cards_info'][1]['hand_cards']

		new_data = [0 for i in range(21)]
		for card in hand_cards:
			new_data[card] += 1
		new_data[0] = data['card_current']
		new_data = np.array(new_data, dtype = np.uint8).reshape(1,21)

		hand_cards = formate_cards(data['cards_info'][1]['hand_cards'])
		hand_cards_cur_card_num = hand_cards[data['card_current'] - 1]
		print("show formate_data card_current ", data['card_current'] - 1)
		print("show formate_data hand_cards ", hand_cards)
		
	else:	
		pre_front_cards_down = formatCards_down(data['cards_info'][0]['desk_front_cards'], False, act_name)
		pre_front_cards_up = formatCards_up(data['cards_info'][0]['desk_front_cards'], False, act_name)
		pre_discard_cards_down = formatCards_down(data['cards_info'][0]['discard_cards'], False, act_name)
		pre_discard_cards_up = formatCards_up(data['cards_info'][0]['discard_cards'], False, act_name)

		cur_hand_cards_down = formatCards_down(data['cards_info'][1]['hand_cards'], False, act_name)
		cur_hand_cards_up = formatCards_up(data['cards_info'][1]['hand_cards'], False, act_name)
		cur_back_cards_down = formatCards_down(data['cards_info'][1]['desk_back_cards'], False, act_name)
		cur_back_cards_up = formatCards_up(data['cards_info'][1]['desk_back_cards'], False, act_name)
		cur_front_cards_down = formatCards_down(data['cards_info'][1]['desk_front_cards'], False, act_name)
		cur_front_cards_up = formatCards_up(data['cards_info'][1]['desk_front_cards'], False, act_name)
		cur_discard_cards_down = formatCards_down(data['cards_info'][1]['discard_cards'], False, act_name)
		cur_discard_cards_up = formatCards_up(data['cards_info'][1]['discard_cards'], False, act_name)
		
		next_front_cards_down = formatCards_down(data['cards_info'][2]['desk_front_cards'], False, act_name)
		next_front_cards_up = formatCards_up(data['cards_info'][2]['desk_front_cards'], False, act_name)
		next_discard_cards_down = formatCards_down(data['cards_info'][2]['discard_cards'], False, act_name)
		next_discard_cards_up = formatCards_up(data['cards_info'][2]['discard_cards'], False, act_name)
		
		new_data = [
			cur_back_cards_down,
			cur_back_cards_up,
			cur_hand_cards_down,
			cur_hand_cards_up,

			cur_discard_cards_down,
			cur_discard_cards_up,
			cur_hand_cards_down,
			cur_hand_cards_up,

			pre_front_cards_down,
			pre_front_cards_up,
			cur_hand_cards_down,
			cur_hand_cards_up,

			next_front_cards_down,
			next_front_cards_up,
			cur_hand_cards_down,
			cur_hand_cards_up,

			pre_discard_cards_down,
			pre_discard_cards_up,
			cur_hand_cards_down,
			cur_hand_cards_up,

			next_discard_cards_down,
			next_discard_cards_up,
			cur_hand_cards_down,
			cur_hand_cards_up,

			cur_front_cards_down,
			cur_front_cards_up,
			cur_hand_cards_down,
			cur_hand_cards_up
		]
		if act_name != 'chu':
			card_current_down = formatCards_down([data['card_current']], True, act_name)
			card_current_up = formatCards_up([data['card_current']], True, act_name)
			new_data.extend([card_current_down, card_current_up, cur_hand_cards_down, cur_hand_cards_up])

			hand_cards = formate_cards(data['cards_info'][1]['hand_cards'])
			hand_cards_cur_card_num = hand_cards[data['card_current'] - 1]
		
		data_len = len(new_data)	
		new_data = np.array(new_data, dtype = np.uint8).reshape(1,data_len,13,4)
	
	#print(new_data)
	return new_data, hand_cards_cur_card_num

chi_list = [
	[],			#0
	[1,2,3],	#1
	[1,1,11],	#2
	[2,3,4],	#3
	[2,7,10],	#4
	[2,2,12],	#5
	[3,4,5],	#6
	[3,3,13],	#7
	[4,5,6],	#8
	[4,4,14],	#9
	[5,6,7],	#10
	[5,5,15],	#11
	[6,7,8],	#12
	[6,6,16],	#13
	[7,8,9],	#14
	[7,7,17],	#15
	[8,9,10],	#16
	[8,8,18],	#17
	[9,9,19],	#18
	[10,10,20],	#19
	[11,12,13],	#20
	[1,11,11],	#21
	[12,13,14],	#22
	[12,17,20],	#23
	[2,12,12],	#24
	[13,14,15],	#25
	[3,13,13],	#26
	[14,15,16],	#27
	[4,14,14],	#28
	[15,16,17],	#29
	[5,15,15],	#30
	[16,17,18],	#31
	[6,16,16],	#32
	[17,18,19],	#33
	[7,17,17],	#34
	[18,19,20],	#35
	[8,18,18],	#36
	[9,19,19],	#37
	[10,20,20],	#38
]


if __name__ == '__main__':

	cards = [
		{
		'hand_cards':[],
		'desk_front_cards':[],     #上家牌信息
		'desk_back_cards':[],
		'discard_cards':[]
		},
		{
		'hand_cards':[1,2,3,4,],
		'desk_front_cards':[],	 #当前玩家牌信息	
		'desk_back_cards':[],
		'discard_cards':[]
		},
		{
		'hand_cards':[],
		'desk_front_cards':[6,6,6],	 #下家牌信息		
		'desk_back_cards':[],
		'discard_cards':[]
		}
	]
	test_data = {'card_current': 1,'cards_info': cards}
	formate_data(test_data,'chi')
