from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .core import *
from .bcolor import bcolors
import core.core


class SGSConsumer(WebsocketConsumer):
  def connect(self):
    print(core.core.room_manager)
    # core.core.room_manager

    self.type = int(self.scope['url_route']['kwargs']['type'])
    self.game_code = self.scope['url_route']['kwargs']['game_code']
    self.sessionKey = self.scope['url_route']['kwargs']['sessionKey']
    self.room = core.core.room_manager.get_room(self.game_code)

    print(bcolors.BLUE + "Now Room List: " +
          ", ".join(map(str, core.core.room_manager.room_list)) + bcolors.ENDC)

    if self.type == 1:  # 참가자
      self.username = self.scope['url_route']['kwargs']['username']
      self.user = User(self.sessionKey, self.username)

      myroom = core.core.room_manager.get_room(self.game_code)
      if myroom == None:
        pass  # 사용자가 입력한 방코드에 방이 없는 경우로 예외처리 필요
      else:
        print(myroom)
        myroom.add_user(self.user)
      print(bcolors.BLUE + "WS: Paticipant connected! ",
            str(self.room), self.user, bcolors.ENDC)
    else: # 방 호스트
      self.user = User(self.sessionKey)
      self.room.set_room_host(self.user)
      print(bcolors.BLUE + "WS: Host connected!", str(self.room), bcolors.ENDC)
    core.core.room_manager.add_user(self.user)

    self.room_group_name = 'sgs_%s' % self.game_code

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
    if not self.room.is_in_game(): # 대기실에 있을경우
      if self.type == 0: # 호스트가 연결이 끊어진 경우 방 폭파
        core.core.room_manager.del_room(self.room)
        self.host_out()
      else: # 참가자가 연결이 끊어진경우 퇴장
        self.user.delete()
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
    print(text_data_json)
    if op == "start_request":
      if self.type == 0: # 게임시작은 호스트만 가능
        selected_game = text_data_json['gamename']
        if selected_game == "RPS":
          print(self.room.num_of_participants())
          if self.room.num_of_participants() > 0: #참가자가 한명이상
            self.room.start_game(selected_game)
            self.game_start()
        elif selected_game == "FIVE_POKER":
          print(self.room.num_of_participants())
          if self.room.num_of_participants() > 0: #참가자가 한명이상
            self.room.start_game(selected_game)
            self.game_start()
        elif selected_game == "indian-poker":
          pass
        elif selected_game == "Bomb":
          if self.room.num_of_participants() > 0: #게임 시작 조건 체크: 참가자가 한명이상
            self.room.start_game(selected_game)
            self.game_start()



    elif op == "":
      pass
    elif op == "":
      pass

    # message = text_data_json['message']
    # print(self)
    # print(message)
    # print(self.username)
    # room group 에게 메세지 send
    # async_to_sync(self.channel_layer.group_send)(
    #   self.room_group_name,
    #   {
    #       'type': 'chat_message',
    #       'message': message
    #   }
    # )

  # room group 에서 메세지 receive
  def chat_message(self, event):
    message = event['message']

    # WebSocket 에게 메세지 전송
    self.send(text_data=json.dumps({
        'message': message
    }))


  # room group 에서 메세지 receive
  def chat_message(self, event):
    message = event['message']

    # WebSocket 에게 메세지 전송
    self.send(text_data=json.dumps({
        'message': message
    }))

#####
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


#####
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


#####
  def game_start(self):
    async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
            'type': 'game_start_send'
        }
    )

  def game_start_send(self, event):
    self.send(text_data=json.dumps({
        'opcode': 'game_start'
    }))
