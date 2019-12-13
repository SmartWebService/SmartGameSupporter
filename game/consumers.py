from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from core.core import *
from core.bcolor import bcolors
import core.core
import game.GameLogic.RPS

import game.GameLogic.Bomb

class RPSConsumer(WebsocketConsumer):
  def connect(self):
    print(core.core.room_manager)
    # core.core.room_manager

    self.sessionKey = self.scope['url_route']['kwargs']['sessionKey']

    self.user = core.core.room_manager.get_user_by_sessionKey(self.sessionKey)
    self.room = self.user.room
    self.game = self.room.game_obj

    self.room_group_name = 'RPS_%s' % self.room.room_code

    # 그룹에 join
    # send 등 과 같은 동기적인 함수를 비동기적으로 사용하기 위해서는 async_to_sync 로 감싸줘야한다.
    async_to_sync(self.channel_layer.group_add)(
        self.room_group_name,
        self.channel_name
    )
    # WebSocket 연결
    self.accept()
    self.participant_refresh()

  def disconnect(self, close_code):
    if not self.user.isParticipant(): # 호스트가 연결이 끊어진 경우 방 폭파
      core.core.room_manager.del_room(self.room)
      self.host_out()
    else: # 참가자가 연결이 끊어진경우 퇴장
      self.user.delete()
    # del self.user
    print("deleted")
    # 그룹에서 Leave
    async_to_sync(self.channel_layer.group_discard)(
        self.room_group_name,
        self.channel_name
    )

  # WebSocket 에게 메세지 receive
  def receive(self, text_data):
    text_data_json = json.loads(text_data)
    op = text_data_json['opcode']
    print("receiced ", text_data_json)

    if op == "game_end":
      if not self.user.isParticipant(): # 게임은 호스트만 가능
        self.game.decision(text_data_json['container'])
        self.result(text_data_json['container'])
        self.refresh()
    elif op == "refresh":
      container = text_data_json['container']

      if container == "R":
        self.game.playRPS_set(self.user, "R")
      elif container == "P":
        self.game.playRPS_set(self.user, "P")
      elif container == "S":
        self.game.playRPS_set(self.user, "S")
      self.refresh()
    elif op == "":
      pass
    elif op == "":
      pass
    elif op == "":
      pass
    


  def refresh(self):
    # room group 에게 메세지 send
    async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
            'type': 'refresh_send'
        }
    )

  def refresh_send(self, event):
    p, c = self.game.get_participants_and_containers()
    print(c)
    # WebSocket 에게 메세지 전송
    self.send(text_data=json.dumps({
        'opcode': 'refresh',
        'participants': p,
        'containers': c
    }))


  def result(self, container):
    # room group 에게 메세지 send
    async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
            'type': 'result_send'
        }
    )

  def result_send(self, event):
    if self.user.isParticipant():
      # container = event['container']
      result = ""
      if self.game.is_user_in_game(self.user):
        result = "true"
      else:
        result = "false"
      print(result)

      # WebSocket 에게 메세지 전송
      self.send(text_data=json.dumps({
          'opcode': 'result',
          'win': result
      }))


  def participant_refresh(self):
    # room group 에게 메세지 send
    async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
            'type': 'participant_refresh_send'
        }
    )

  def participant_refresh_send(self, event):
    participant_list = self.room.room_participants
    print("log", list(map(str, participant_list)))
    # WebSocket 에게 메세지 전송
    self.send(text_data=json.dumps({
        'opcode': 'p_refresh',
        'list': list(map(str, participant_list))
    }))

  def host_out(self):
    async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
            'type': 'host_out_send'
        }
    )

  def host_out_send(self, event):
    self.user.delete()
    self.send(text_data=json.dumps({
        'opcode': 'host_out'
    }))








##### BOMB #####
class BombConsumer(WebsocketConsumer):
  def connect(self):
    print(core.core.room_manager)
    # core.core.room_manager

    self.sessionKey = self.scope['url_route']['kwargs']['sessionKey']

    self.user = core.core.room_manager.get_user_by_sessionKey(self.sessionKey)
    self.room = self.user.room
    self.game = self.room.game_obj

    self.room_group_name = 'bomb_%s' % self.room.room_code

    if not self.user.isParticipant():
      self.game.hostSocket = self

    # 그룹에 join
    # send 등 과 같은 동기적인 함수를 비동기적으로 사용하기 위해서는 async_to_sync 로 감싸줘야한다.
    async_to_sync(self.channel_layer.group_add)(
        self.room_group_name,
        self.channel_name
    )
    # WebSocket 연결
    self.accept()
    self.participant_refresh()

  def disconnect(self, close_code):
    if not self.user.isParticipant(): # 호스트가 연결이 끊어진 경우 방 폭파
      core.core.room_manager.del_room(self.room)
      self.host_out()
    else: # 참가자가 연결이 끊어진경우 퇴장
      self.user.delete()
    # del self.user
    print("deleted")
    # 그룹에서 Leave
    async_to_sync(self.channel_layer.group_discard)(
        self.room_group_name,
        self.channel_name
    )

  # WebSocket 에게 메세지 receive
  def receive(self, text_data):
    text_data_json = json.loads(text_data)
    op = text_data_json['opcode']
    print("receiced ", text_data_json)

    if op == "start":
      if not self.user.isParticipant(): # 게임은 호스트만 가능
        self.game.start_game(text_data_json['IoT_code'])
        self.refresh()
        self.get_bomb()
    elif op == "push_bomb":
      if self.user.isParticipant(): # 게임은 호스트만 가능
        self.game.push_bomb(self.user)
        self.refresh()
        self.get_bomb()
    elif op == "":
      pass
    elif op == "":
      pass
    elif op == "":
      pass
    


  def refresh(self):
    # room group 에게 메세지 send
    async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
            'type': 'refresh_send'
        }
    )

  def refresh_send(self, event):
    if not self.user.isParticipant():
      p, i = self.game.refresh()
      # WebSocket 에게 메세지 전송
      self.send(text_data=json.dumps({
          'opcode': 'refresh',
          'participants': p,
          'bomb_user_index': i
      }))

  def get_bomb(self):
    # room group 에게 메세지 send
    async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
            'type': 'get_bomb_send'
        }
    )

  def get_bomb_send(self, event):
    if self.game.get_bomb(self.user):
      print("def get_bomb_send(self, event):")
      # WebSocket 에게 메세지 전송
      self.send(text_data=json.dumps({
          'opcode': 'get_bomb'
      }))

  def result(self, container):
    # room group 에게 메세지 send
    async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
            'type': 'result_send',
            'container': container
        }
    )

  def result_send(self, event):
    container = event['container']
    result = ""
    if self.game.is_user_in_game(self.user):
      result = "true"
    else:
      result = "false"

    # WebSocket 에게 메세지 전송
    self.send(text_data=json.dumps({
        'opcode': 'result',
        'win': result,
    }))


  def participant_refresh(self):
    # room group 에게 메세지 send
    async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
            'type': 'participant_refresh_send'
        }
    )

  def participant_refresh_send(self, event):
    participant_list = self.room.room_participants
    print("log", list(map(str, participant_list)))
    # WebSocket 에게 메세지 전송
    self.send(text_data=json.dumps({
        'opcode': 'p_refresh',
        'list': list(map(str, participant_list))
    }))

  def host_out(self):
    async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
            'type': 'host_out_send'
        }
    )

  def host_out_send(self, event):
    self.send(text_data=json.dumps({
        'opcode': 'host_out'
    }))

  def bomb_bomb(self):
    # room group 에게 메세지 send
    async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
            'type': 'bomb_bomb_send'
        }
    )

  def bomb_bomb_send(self, event):
    # WebSocket 에게 메세지 전송
    self.send(text_data=json.dumps({
        'opcode': 'bomb_bomb'
    }))







##### FivePoker #####
class FivePokerConsumer(WebsocketConsumer):
  def connect(self):
    print(core.core.room_manager)
    # core.core.room_manager

    self.sessionKey = self.scope['url_route']['kwargs']['sessionKey']

    self.user = core.core.room_manager.get_user_by_sessionKey(self.sessionKey)
    self.room = self.user.room
    self.game = self.room.game_obj

    self.room_group_name = 'FP_%s' % self.room.room_code

    # 그룹에 join
    # send 등 과 같은 동기적인 함수를 비동기적으로 사용하기 위해서는 async_to_sync 로 감싸줘야한다.
    async_to_sync(self.channel_layer.group_add)(
        self.room_group_name,
        self.channel_name
    )
    # WebSocket 연결
    self.accept()
    self.participant_refresh()

  def disconnect(self, close_code):
    self.host_out
    print("deleted")
    # 그룹에서 Leave
    async_to_sync(self.channel_layer.group_discard)(
        self.room_group_name,
        self.channel_name
    )

  # WebSocket 에게 메세지 receive
  def receive(self, text_data):
    text_data_json = json.loads(text_data)
    op = text_data_json['opcode']
    print("receiced ", text_data_json)

    if op == "game_end":
      if not self.user.isParticipant(): # 게임은 호스트만 가능
        self.game.decision(text_data_json['container'])
        self.result(text_data_json['container'])
    elif op == "refresh":
      container = text_data_json['container']

    if op == "call":
      if self.user == self.game.get_nowplayer():
        self.game.call(self.user)
    elif op == "raise":
      if self.user == self.game.get_nowplayer():
        self.game.rais(self.user, self.game.nowbet + 1)
    elif op == "die":
      if self.user == self.game.get_nowplayer():
        self.game.die(self.user)
    
    if self.game.check_break():
      self.game_end()
    
  def game_end(self):
    #room group 에게 메세지 send
    async_to_sync(self.channel_layer.group_send)(
       self.room_group_name,
       {
          'type': 'game_end_send'
       }
    )
  
  def game_end_send(self, event):
    # if
    winner = self.game.check_winner()
    self.game.give_winner_chips(winner)
    self.game.clear_game()
    # WebSocket 에게 메세지 전송
    self.send(text_data=json.dumps({
        'opcode': 'game_end',
        'winner': str(winner.user)
    }))
  
  def participant_card(self, container):
    # room group 에게 메세지 send
    async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
            'type': 'participant_card_send',
            'container': container
        }
    )
  
  def participant_card_send(event):
    container = event['container']
    cards = []
    for player in self.game.players:
      if player.user == self.user:
        cards = player.get_cards

        self.send(text_data=json.dumps({
          'opcode': 'participant_card',
          'card_list': cards
        }))
    
  def current_money(self):
    #room group 에게 메세지 send
    async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
            'type': 'current_money_send'
        }
    )

  def current_money_send(self, event):
    if not self.user.isParticipant():
      money = self.game.get_all_bet()
      print("bet : ",money)
      #WebSocket 에게 메세지 전송
      self.send(text_data=json.dumps({
          'opcode': 'current_money',
          'money': money
      }))


  def participant_refresh(self):
    # room group 에게 메세지 send
    async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
            'type': 'participant_refresh_send'
        }
    )

  def participant_refresh_send(self, event):
    participant_list = self.room.room_participants
    print("log", list(map(str, participant_list)))
    # WebSocket 에게 메세지 전송
    self.send(text_data=json.dumps({
        'opcode': 'p_refresh',
        'list': list(map(str, participant_list))
    }))

  def host_out(self):
    async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
            'type': 'host_out_send'
        }
    )

  def host_out_send(self, event):
    self.send(text_data=json.dumps({
        'opcode': 'host_out'
    }))