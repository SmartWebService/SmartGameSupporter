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