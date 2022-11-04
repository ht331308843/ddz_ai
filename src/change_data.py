# 转换数据模块
# 部分变量名与参数名采用小驼峰命名法(方便直接解析json使用)
# created by guyanyong 2020/07/03

# [[
# 	转换房间数据
# 	desk {
# 		cardId= number/nil
# 		huCount= number
# 		agent{
# 			_stillCards=[]
# 			_handCards=[]
# 			_passCards=[]
# 			_deskBackCards= [][]
# 			_deskFrontCards= [][]
# 			_badCards= []
# 			passSweepIndex= []
# 		}
# 		actTodo{
# 			{
# 				seatIndex=  1
# 				canEat=     false
# 				canBump=    true
# 				canPut =    false
# 				aiLevle = 	3
# 				returnList = {
# 					type: number
# 					list: []
# 				}
# 			}
# 			{
# 				seatIndex=  2
# 				canEat= 	true
# 				canBump=    false
# 				canPut =    false
# 				aiLevle = 	3
# 				returnList = {
# 					type: number
# 					list: []
# 				}
# 			}
# 			...
# 		}
# 	}
# ]]

import json
from actcheck import *
import copy

actNameGlzp = {
	'discardPass': 1,					# 过张弃
	'discardBad' : 2,                 	# 臭张弃
	'discard' :3,      					# 弃牌
	'chi' : 4,							# 吃
	'peng' : 5,							# 碰
	'kaiZhaoHand' : 6,					# 手牌开招  
	'kaiZhaoDeskFront' : 7,				# 桌面牌明开招
	'kaiZhaoDeskBack' : 8,				# 面牌暗开招
	'hu' : 9,							# 胡 
	'sao' : 10,	    					# 扫
	'saoGuo' : 11,     					# 过扫
	'saoChuanHand' : 12,   				# 手牌扫穿
	'saoChuanDesk' : 13,				# 桌面牌扫穿
	'moCard' : 14,      				# 摸牌
	'putCard' : 15,  					# 出牌
	'longCardsToDesk' : 16,        		# 将笼牌放入桌面
	'chongZhao': 17,                 	# 播放重招
	'huangZhuang': 18,               	# 黄庄 
}

def changeDeskCards(deskCards):
	re_cards = []
	for cards in deskCards:
		for card in cards:
			re_cards.append(card)
	return re_cards

def change2HandCardType(cards):
	handCards = [0 for i in range(21)]
	for card in cards:
		if card > 0 :
			handCards[card] += 1
	return handCards

def formatDecisionCards(cards):
	returnCards = []
	for v in cards:
		if type(v) == int: 
			returnCards.append(v)

		if type(v) == list:
			for card in v:
				returnCards.append(card)			
			returnCards.append(0)
		
	if returnCards[len(returnCards) - 1] == 0:
		returnCards.pop()
		
	return returnCards

def find_act_todo(seatIndex, decisions):
	data = {}
	data['seatIndex'] = seatIndex
	data['canBump'] = False
	data['canEat'] = False
	data['canPut'] = False
	data['canHu'] = False

	for decision in decisions:
		if decision['type'] == actNameGlzp['peng']:
			data['canBump'] = True
		
		if decision['type'] == actNameGlzp['chi']:
			data['canEat'] = True
		
		if decision['type'] == actNameGlzp['putCard']:
			data['canPut'] = True

		if decision['type'] == actNameGlzp['hu']:
			data['canHu'] = True

	return data

def find_hand_cards(cards):
	return cards

def find_pass_cards(fixedDecisions):
	passCards = []
	for decision in fixedDecisions:
		if decision['type'] == actNameGlzp['discardPass']:
			passCards.append(decision['keyCards'][0])

	return passCards

def find_desk_back_cards(fixedDecisions):
	desk_back_cards = []
	for decision in fixedDecisions:
		if decision['type'] == actNameGlzp['sao'] or \
			decision['type'] == actNameGlzp['saoGuo'] or \
			decision['type'] == actNameGlzp['saoChuanHand']: \

			desk_back_cards.append(decision['cards'])

		sao_chuan_index = None
		if decision['type'] == actNameGlzp['saoChuanDesk']:
			for index, cards in enumerate(desk_back_cards):
				if len(cards) == 3 and cards[0] == cards[1] and cards[0] == cards[2] and cards[0] == decision['cards'][0]: 
					sao_chuan_index = index
					break

			if sao_chuan_index != None : 
				desk_back_cards[saoChuanIndex] = decision['cards']

		kaiZhaoIndex = None	
		if decision['type'] == actNameGlzp['kaiZhaoDeskBack']:
			for index, cards in enumerate(desk_back_cards):
				if len(cards) == 3 and cards[0] == cards[1] and cards[0] == cards[2] and cards[0] == decision['cards'][0]: 
					kai_zhao_index = index
					break

			if kaiZhaoIndex != None :
				desk_back_cards.pop(kai_zhao_index)
			
	return changeDeskCards(desk_back_cards), desk_back_cards

def find_desk_front_cards(fixedDecisions):
	desk_front_cards = []
	for decision in fixedDecisions:
		if decision['type'] == actNameGlzp['peng'] or \
			decision['type'] == actNameGlzp['chi'] or \
			decision['type'] == actNameGlzp['kaiZhaoDeskBack'] or \
			decision['type'] == actNameGlzp['kaiZhaoHand'] or \
			decision['type'] == actNameGlzp['kaiZhaoDeskFront']:
			if len(decision['cards']) <= 4 and len(decision['cards']) > 0 : 
				desk_front_cards.append(decision['cards'])
			
			if len(decision['cards']) > 4:
				while len(decision['cards']) > 0:
					if 0 in decision['cards']:
						decision['cards'].remove(0)
					temp_cards = []
					for i in range(3):
						temp_cards.append(decision['cards'].pop(0))
					desk_front_cards.append(temp_cards)
					

		pengIndex = None	
		if decision['type'] == actNameGlzp['kaiZhaoDeskFront']:
			for index, cards in enumerate(desk_front_cards):
				if len(cards) == 3 and cards[0] == cards[1] and cards[0] == cards[2] and cards[0] == decision['cards'][0]: 
					pengIndex = index
					break

			if pengIndex != None :
				desk_front_cards[pengIndex] = decision['cards']

	return changeDeskCards(desk_front_cards), desk_front_cards

def find_bad_cards(fixedDecisions):
	badCards = []
	for decision in fixedDecisions:
		if decision['type'] == actNameGlzp['discardBad']:
			badCards.append(decision['keyCards'][0]) 
		
	return badCards

def find_still_cards(fixedDecisions):
	stillCards = []
	for decision in fixedDecisions:
		if decision['type'] == actNameGlzp['discard']:
			stillCards.append(decision['keyCards'][0])
		
	return stillCards

def get_next_seatIndex(seatIndex, maxPlayers):
	if seatIndex == maxPlayers - 1:
		return 0
	else:
		return seatIndex + 1

def formatRoom(data):
	desk = {}
	desk['agent'] = []
	desk['actTodo'] = []
	if "guid" in data.keys():
		desk['guid'] = data['guid'] 
		print("desk guid ",desk['guid'])
		for index, player in enumerate(data['room']['players']):
			desk['agent'].append({})
			print("player guid ",player['guid'])
			if player['isRobot'] == True and len(player['decisions']) > 0 and player['guid'] == desk['guid']:
				desk['actTodo'].append(find_act_todo(index, player['decisions']))
			
			desk['agent'][index]['_handCards'] = find_hand_cards(player['cards'])
			desk['agent'][index]['_passCards'] = find_pass_cards(player['fixedDecisions'])
			desk['agent'][index]['_deskBackCards'], desk['agent'][index]['nochange_deskBackCards']= find_desk_back_cards(player['fixedDecisions'])
			desk['agent'][index]['_deskFrontCards'], desk['agent'][index]['nochange_deskFrontCards'] = find_desk_front_cards(player['fixedDecisions'])
			
			desk['agent'][index]['_badCards'] = find_bad_cards(player['fixedDecisions'])
			desk['agent'][index]['_stillCards'] = find_still_cards(player['fixedDecisions'])
			desk['agent'][index]['_passSweepIndex'] = []

	elif "uid" in data.keys():	
		desk['uid'] = data['uid'] 
		print("desk uid ",desk['uid'])
		for index, player in enumerate(data['room']['players']):
			desk['agent'].append({})
			print("player uid ",player['uid'])
			if player['isRobot'] == True and len(player['decisions']) > 0 and player['uid'] == desk['uid']:
				desk['actTodo'].append(find_act_todo(index, player['decisions']))
			
			desk['agent'][index]['_handCards'] = find_hand_cards(player['cards'])
			desk['agent'][index]['_passCards'] = find_pass_cards(player['fixedDecisions'])
			desk['agent'][index]['_deskBackCards'], desk['agent'][index]['nochange_deskBackCards']= find_desk_back_cards(player['fixedDecisions'])
			desk['agent'][index]['_deskFrontCards'], desk['agent'][index]['nochange_deskFrontCards'] = find_desk_front_cards(player['fixedDecisions'])
			
			desk['agent'][index]['_badCards'] = find_bad_cards(player['fixedDecisions'])
			desk['agent'][index]['_stillCards'] = find_still_cards(player['fixedDecisions'])
			desk['agent'][index]['_passSweepIndex'] = []


	desk['cardId'] = 0
	print("====================  eee  ")
	print(data['room']['lastDecisions'])

	if desk['actTodo'][0]['canPut'] == False and len(data['room']['lastDecisions']) > 0:
		for decision in data['room']['lastDecisions']:
			if decision['type'] == actNameGlzp['putCard'] or decision['type'] == actNameGlzp['moCard']:
				desk['cardId'] = decision['keyCards'][0];
				break
	
	desk['huCount'] = 15 

	return desk	

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
def change_predict_format(data):
	#转化为深度学习的数据格式（不是最终的格式）
	require_data = {'card_current': 0, 'cards_info': []}
	require_data['card_current'] = data['cardId']
	seat_index = data['actTodo'][0]['seatIndex']
	next_seat_index = get_next_seatIndex(seat_index, len(data['agent']))
	last_seat_index = get_next_seatIndex(next_seat_index, len(data['agent']))

	temp_seat_index = last_seat_index
	for i in range(len(data['agent'])):
		temp_data = {
			'hand_cards': data['agent'][temp_seat_index]['_handCards'],
			'desk_front_cards': data['agent'][temp_seat_index]['_deskFrontCards'],	 
			'desk_back_cards': data['agent'][temp_seat_index]['_deskBackCards'],
			'discard_cards': data['agent'][temp_seat_index]['_stillCards'],
			'nochange_deskBackCards': data['agent'][temp_seat_index]['nochange_deskBackCards'],
			'nochange_deskFrontCards': data['agent'][temp_seat_index]['nochange_deskFrontCards'],
		}
		require_data['cards_info'].append(temp_data)
		temp_seat_index = get_next_seatIndex(temp_seat_index ,len(data['agent']))

	act_list = []
	
	if data['actTodo'][0]['canHu']	== True:
		act_list.append('hu')
	if data['actTodo'][0]['canPut']	== True:
		act_list.append('chu')
	if data['actTodo'][0]['canBump'] == True:
		act_list.append('peng')
	if data['actTodo'][0]['canEat']	== True:
		act_list.append('chi')
		
	return require_data, act_list

def check_can_chu(predict_data, re_info):
	hand_cards = change2HandCardType(predict_data['cards_info'][1]['hand_cards'])	
	card = re_info['result'][0]
	if hand_cards[card] == 0 or hand_cards[card] > 2:
		print("predict chu error")
		for temp_card, number in enumerate(hand_cards):
			if number > 0 and number < 3:
				re_info['result'][0] = temp_card
				break

def check_chi_lawful(predict_data, chi_data):
	hand_cards = change2HandCardType(predict_data['cards_info'][1]['hand_cards'])
	cards = change2HandCardType(chi_data)
	card = predict_data['card_current']
	#检查吃是否合法
	for chi_card in chi_data:
		if chi_card != card and hand_cards[chi_card] >= 3:
			return False

	return True
	
def check_can_chi(predict_data, chi_data):
	hand_cards = change2HandCardType(predict_data['cards_info'][1]['hand_cards'])
	cards = change2HandCardType(chi_data)
	card = predict_data['card_current']
	if hand_cards[card] >= cards[card]:
		for card_remove in chi_data:
			if card_remove in predict_data['cards_info'][1]['hand_cards']:
				predict_data['cards_info'][1]['hand_cards'].remove(card_remove)
			else:
				predict_data = None
				print('chi error')
				return False
		return True

	remove_counts = 0
	for card_remove in chi_data:
		print("card_remove ", card_remove)
		if card_remove in predict_data['cards_info'][1]['hand_cards']:
			predict_data['cards_info'][1]['hand_cards'].remove(card_remove)
			remove_counts += 1
	if remove_counts != len(chi_data) - 1:
		predict_data = None
		print('chi error')
	return False

def check_advance_chu(chu_card, chi_data):
	cards = change2HandCardType(chi_data)
	if len(chi_data) == 3:
		if (chu_card <= 10 and 2 == cards[chu_card + 10]) or (chu_card > 10 and 2 == cards[chu_card - 10]):
			return True

def in_cards(hand_cards, cards):
	for card in cards:
		if hand_cards[card] <= 0 or hand_cards[card] >= 3:
			return False
	return True

def hu_hand_cards(predict_data):
	card_current = predict_data['card_current']
	hand_cards = change2HandCardType(predict_data['cards_info'][1]['hand_cards'])
	if (card_current == 1 or card_current == 2 or card_current == 3) and in_cards(hand_cards, [1,2,3]):
		return True
	if (card_current == 11 or card_current == 12 or card_current == 13) and in_cards(hand_cards, [11,12,13]):
		return True

	if (card_current == 2 or card_current == 7 or card_current == 10) and in_cards(hand_cards, [2,7,10]):
		return True
	if (card_current == 12 or card_current == 17 or card_current == 20) and in_cards(hand_cards, [12,17,20]):
		return True	
			
def reductRoom(data, re_infos):
	room = data['room']  
	do_action_type = 0

	if re_infos['type'] == 'chu':
		do_action_type = actNameGlzp['putCard']

	elif re_infos['type'] == 'peng':
		do_action_type = actNameGlzp['peng']
		if re_infos['result'][0] == 0:
			do_action_type = actNameGlzp['discard']

	elif re_infos['type'] == 'chi':
		do_action_type = actNameGlzp['chi']
		if len(re_infos['result'][0]) == 0:
			do_action_type = actNameGlzp['discard']

	elif re_infos['type'] == 'hu':
		do_action_type = actNameGlzp['hu']

	print(do_action_type)		

	for player in data['room']['players']:
		if "guid" in data.keys():
			if player['guid'] == data['guid']:
				for decision in player['decisions']:
					if do_action_type and decision['type'] == do_action_type: 
						if not 'cards' in decision.keys():
							decision['cards'] = []
						if len(decision['cards']) == 0 and decision['type'] != actNameGlzp['discard']  and decision['type'] != actNameGlzp['hu'] :
							decision['cards'] = formatDecisionCards(re_infos['result'])
						print("predict decision ",decision['type'])
						return decision

		elif "uid" in data.keys():
			if player['uid'] == data['uid']:
				for decision in player['decisions']:
					if do_action_type and decision['type'] == do_action_type: 
						if not 'cards' in decision.keys():
							decision['cards'] = []
						if len(decision['cards']) == 0 and decision['type'] != actNameGlzp['discard']:
							decision['cards'] = formatDecisionCards(re_infos['result'])
						print("predict decision ",decision['type'])
						return decision
				
def chu_by_tinghu(predict_data):

	hand_cards = predict_data['cards_info'][1]['hand_cards']
	desk_front_cards = predict_data['cards_info'][1]['nochange_deskFrontCards']
	desk_back_cards = predict_data['cards_info'][1]['nochange_deskBackCards']
	card_current = predict_data['card_current']
	ting_data, new_hand_cards = check_ting_for_putcard(hand_cards, desk_front_cards, desk_back_cards)
	if len(ting_data) == 0:
		predict_data['cards_info'][1]['hand_cards'] = new_hand_cards
		return None
	else:
		put_card = ting_data[0]['put_card']
		if put_card != None:
			return {'result': [put_card], 'type': 'chu', 'detail': []}
		else:
			return None

def peng_by_tinghu(predict_data):
	hand_cards = copy.deepcopy(predict_data['cards_info'][1]['hand_cards']) 
	desk_front_cards = copy.deepcopy(predict_data['cards_info'][1]['nochange_deskFrontCards'])
	desk_back_cards = predict_data['cards_info'][1]['nochange_deskBackCards']
	card_current = predict_data['card_current']
	ting_data, new_hand_cards = check_ting(hand_cards, desk_front_cards, desk_back_cards)
	hand_cards_format = change2HandCardType(hand_cards)

	if hand_cards_format[card_current] != 2:
		print("[error]  card_current ",card_current)
		print("[error]  hand_cards ",hand_cards)
		return None

	san_card_number_befor = check_san_card_number(hand_cards_format)

	for i in range(2):	
		hand_cards.remove(card_current)

	desk_front_cards.append([card_current,card_current,card_current])	
	san_card_number_after = check_san_card_number(change2HandCardType(hand_cards))
	ting_data_put, new_hand_cards = check_ting_for_putcard(hand_cards, desk_front_cards, desk_back_cards)	
	
	if len(ting_data) > 0 : 
		if len(ting_data_put) > 0 and len(ting_data_put[0]['format_data']) <= len(ting_data[0]['format_data']):
			print("peng card ting number less")
			return {'result': [0], 'type': 'peng', 'detail': []}

	elif len(ting_data_put) > 0 : 
		print("peng card ting number more")
		return {'result': [1], 'type': 'peng', 'detail': []}
		
	if hu_hand_cards(predict_data) and san_card_number_after >= san_card_number_befor:
		print("peng but san card more, san_card_number_after ",san_card_number_after,  "san_card_number_befor ",san_card_number_befor)
		return {'result': [0], 'type': 'peng', 'detail': []}

	return None

def chi_by_tinghu(predict_data, re_info):

	chi_detail = re_info['result']
	hand_cards = copy.deepcopy(predict_data['cards_info'][1]['hand_cards']) 
	desk_front_cards = copy.deepcopy(predict_data['cards_info'][1]['nochange_deskFrontCards'])
	desk_back_cards = predict_data['cards_info'][1]['nochange_deskBackCards']
	card_current = predict_data['card_current']
	ting_data, new_hand_cards = check_ting(hand_cards, desk_front_cards, desk_back_cards)
	
	hand_cards_copy = copy.deepcopy(hand_cards)
	hand_cards.append(card_current)
	for card in chi_detail:
		if card in hand_cards:
			hand_cards.remove(card)

	desk_front_cards.append(chi_detail)
	ting_data_put, new_hand_cards = check_ting_for_putcard(hand_cards, desk_front_cards, desk_back_cards)	
	
	if len(ting_data) > 0 :
		if len(ting_data_put) == 0 or (len(ting_data_put) > 0 and len(ting_data_put[0]['format_data']) <= len(ting_data[0]['format_data'])):
			print("chi card ting number less")
			re_info['result'] = []
			re_info['detail'] = []
	elif len(ting_data_put) == 0 :
		chi_detail_format = change2HandCardType(chi_detail)
		hand_cards_format_befor = change2HandCardType(hand_cards_copy)
		hand_cards_format_after = change2HandCardType(hand_cards)
		if chi_detail_format[card_current] == 2 or (chi_detail_format[card_current] == 1 and (2 in chi_detail_format)):
			if (check_san_card_number(hand_cards_format_befor) <= check_san_card_number(hand_cards_format_after)) or hu_hand_cards(predict_data):
				print("chi card but san card more")
				re_info['result'] = []
				re_info['detail'] = []

if __name__ == '__main__':
	#formatRoom(1)
	data = {"uid":3323,"room":{"seats":[5302,3323,3324],"players":[{"decisions":[],"fixedDecisions":[],"cards":[13,8,6,9,17,9,20,3,12,9,7,10,4,15,4,11,13,4,3,14],"playedCards":[],"guid":5302,"nickname":"robot302","avatar":"","sex":0,"status":1,"ready":False,"isRobot":False,"location":None,"score":9999999,"carriedScore":9999999,"changedScore":0,"takenOver":False,"turnNumber":0,"role":10,"robotPlayTime":0,"winRoundCount":0,"totalWinScore":0,"firstWinRound":0,"highestScoreOfRound":0,"clientInfo":{"gameId":"101"},"rank":0,"isOffline":False,"pushCount":0},{"decisions":[{"subTypes":[],"associatedDecisions":[],"subDecisions":[],"cards":[],"keyCards":[],"id":1,"type":15,"guid":3323,"order":0,"score":0,"step":0,"turnNumber":0,"sender":0}],"fixedDecisions":[],"cards":[10,18,18,20,12,10,16,6,13,12,5,5,6,12,2,1,16,8,7,20,8],"playedCards":[],"guid":3323,"nickname":"本性难改","avatar":"http://czzpdownloadcdn.gllkgame.com/web_upload/AI_header/azvibMt8cnNBfhM7LXwicGk9Ticd6FEzRl5VMPPeibndrDZkJFRtk22MSbAoEA4wINiaQhYcS0qebZIpmcwEK5icswWQ132.png","sex":0,"status":0,"ready":False,"isRobot":True,"location":{"province":"","city":"桂林","district":"七星区","street":"","altitude":0,"longitude":0,"latitude":0},"score":628754,"carriedScore":628754,"changedScore":0,"takenOver":False,"turnNumber":0,"role":10,"robotPlayTime":2161,"winRoundCount":0,"totalWinScore":0,"firstWinRound":0,"highestScoreOfRound":0,"clientInfo":{"gameId":"101"},"rank":0,"isOffline":False,"pushCount":0},{"decisions":[],"fixedDecisions":[],"cards":[19,3,15,17,11,16,16,9,2,19,11,14,17,7,11,1,1,2,13,15],"playedCards":[],"guid":3324,"nickname":"KONG","avatar":"http://czzpdownloadcdn.gllkgame.com/web_upload/AI_header/azllnzWiaKHnucD58lYVQPaZsH3tH0pwibTXr80tQ2oE0mPk9SBIb5oyPYt9PBWficiczPjO7W03zfZhr9qAfibC6aw132.png","sex":1,"status":1,"ready":False,"isRobot":True,"location":{"province":"","city":"桂林","district":"秀峰区","street":"","altitude":0,"longitude":0,"latitude":0},"score":974816,"carriedScore":974816,"changedScore":0,"takenOver":False,"turnNumber":0,"role":10,"robotPlayTime":1062,"winRoundCount":0,"totalWinScore":0,"firstWinRound":0,"highestScoreOfRound":0,"clientInfo":{"gameId":"101"},"rank":0,"isOffline":False,"pushCount":0}],"decisions":[],"finalDecisions":[],"lastDecisions":[],"payments":[],"historyEmojis":[],"cards":[],"playingCards":[],"drawingCards":[],"finishInfo":{},"finalInfo":{},"code":"6757ffa6-24b1-42b0-a93c-2b1c513eb1ee","owner":0,"config":{"robotPlayTimes":[],"scoreLimit":[-2147483648,120],"votes":[{"type":10,"duration":180}],"emojis":[{"costs":[],"id":1,"type":1,"icon":"","cdTime":5000},{"costs":[],"id":2,"type":1,"icon":"","cdTime":5000},{"costs":[],"id":3,"type":2,"icon":"","cdTime":5000},{"costs":[],"id":4,"type":2,"icon":"","cdTime":5000},{"costs":[],"id":5,"type":1,"icon":"","cdTime":5000},{"costs":[],"id":6,"type":1,"icon":"","cdTime":5000},{"costs":[],"id":7,"type":2,"icon":"","cdTime":5000},{"costs":[],"id":8,"type":2,"icon":"","cdTime":5000}],"matchId":"","matchRoomDataId":"","game":"phz","maxPlayers":3,"type":0,"makeTime":15,"baseScore":1,"totalRound":1,"nextRoundDelay":3000,"debug":None,"templateId":"5eb37b6ffc3dd0aaa3920584","changeSeat":False,"paymentType":40,"extraCostAmount":0,"ziPai":{"mingTangs":[],"dianPao":False,"ziMo":False,"repeatedFx":False,"fanXingType":0,"huCountLine":0,"huInterval":0,"ziMoCalculat":0,"dealerCards":False,"chongTun":0,"quPai":False,"forceHu":False,"dao":0,"firstMakeTime":0},"rule":"ziPai"},"playingState":30,"dealer":0,"round":0,"playingUid":0,"makeStartTime":"1593674006806","decisionId":0,"next":"","nextDelay":0,"store":"","madeDecision":False,"vote":None,"type":0,"clubInfo":None,"recordId":"","step":0,"replayId":"","dismiss":None,"clientInfo":None,"makeTime":15,"instanceId":""}}
	change_predict_format(formatRoom(data))

