from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from core.core import *
from core.bcolor import bcolors
import core.core
import game.GameLogic.RPS

class RPSConsumer(WebsocketConsumer):
  def connect(self):
    print(core.core.room_manager)
    # core.core.room_manager

    self.sessionKey = self.scope['url_route']['kwargs']['sessionKey']

    self.user = core.core.room_manager.get_user_by_sessionKey(self.sessionKey)
    self.room = self.user.room
    self.game = self.room.game_obj

    self.room_group_name = 'RPS_%s' % self.game_code

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
    if self.type == 0: # 호스트가 연결이 끊어진 경우 방 폭파
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

    if op == "start_request":
      if self.type == 0: # 게임시작은 호스트만 가능
        selected_game = text_data_json['game']
        self.room.selected_game = selected_game
    elif op == "rock":
      self.game.playRPS_set(self.user, "R")
    elif op == "paper":
      self.game.playRPS_set(self.user, "P")
    elif op == "scissors":
      self.game.playRPS_set(self.user, "S")
    elif op == "":
      pass
    elif op == "":
      pass
    elif op == "":
      pass
    

    # message = text_data_json['message']
    # print(self)
    # print(message)
    # print(self.username)
    # room group 에게 메세지 send
    async_to_sync(self.channel_layer.group_send)(
      self.room_group_name,
      {
          'type': 'chat_message',
          'message': message
      }
    )

  # room group 에서 메세지 receive
  def chat_message(self, event):
    message = event['message']

    # WebSocket 에게 메세지 전송
    self.send(text_data=json.dumps({
        'message': message
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