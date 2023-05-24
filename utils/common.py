from config import config
from colorama import Fore, Style, init
from text_box_wrapper import wrap
from logger import logger
from .__version__ import __version__
from db import utils


def is_allow_access(chat_id) -> bool:
  '''
  检查当前chat_id有权限使用bot

  Args:
      chat_id (_type_): Telegram chat id

  Returns:
      bool: 是否允许使用
  '''
  # 非公共服务
  if 'private_service' in config and config['private_service']:
    if 'authorized_users' in config:
      # 只服务指定的用户
      if chat_id in config['authorized_users']:
          return True
    return False
  return True

def read_tag_from_file(filename="version.txt"):
  '''
  获取tag信息  
  Args:
      filename (str, optional): _description_. Defaults to "version.txt".

  Returns:
      _type_: _description_
  '''
  return __version__
  # try:
  #     with open(filename, "r") as f:
  #         tag = f.read().strip()
  # except FileNotFoundError:
  #     tag = "unknown"
  # return tag

@wrap(border_string='##',min_padding=2)
def banner():
  init()  # 初始化colorama
  green_circle = f"{Fore.GREEN}● success{Style.RESET_ALL}\n"
  tag = read_tag_from_file()
  message = f"{green_circle} 🤖️Telegram keyword alert bot (Version: {tag})"
  return message


def is_msg_block(receiver,msg,channel_name,channel_id):
  """
  消息黑名单检查
  Args:
      receiver : 消息接收用户 chat id
      msg : 消息内容
      channel_name : 消息发送的频道名称
      channel_id : 消息发送的频道id

  Returns:
      Bool: True 命中黑名单 不发送消息，False 无命中 发送消息
  """
  user = utils.db.user.get_or_none(chat_id=receiver)

  for blacklist_type in ['length_limit']:
    find = utils.db.connect.execute_sql('select id,blacklist_value from user_block_list where user_id = ? and blacklist_type=? ' ,(user.id,blacklist_type)).fetchone()
    if find:
      (id,blacklist_value) = find 
      if blacklist_type == 'length_limit':
        limit = int(blacklist_value)
        msg_len = len(msg)
        if limit and msg_len > limit:
          logger.info(f'block_list_check refuse send. blacklist_type: {blacklist_type}, limit: {limit}, msg_len: {msg_len}')
          return True
  return False


