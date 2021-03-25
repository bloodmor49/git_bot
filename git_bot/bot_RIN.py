import amino
import threading
import time
from termcolor import colored

client = amino.Client()

###ИСХОДНЫЕ ДАННЫЕ

email = input("Email: ")
password = input("Password: ")
NSP='172854462'

###ЛОГИН

client = amino.Client()
print('Вход в Амино - успешно')
client.login(email=email, password=password) 
print('Логин - успешно')

###СПИСОК МОИХ СООБЩЕСТВ И ВХОД В НСП

subclients_search = client.sub_clients()
for name_com, id_com in zip(subclients_search.name, subclients_search.comId):
    print(name_com, id_com)
sub_client = amino.SubClient(comId=NSP, profile=client.profile) 
print('Вход в "', name_com, '" - успешно')

###СПИСОК МОИХ ЧАТОВ В НСП И ВВОД ТЕСТОВОГО СООБЩЕНИЯ

get_chats = sub_client.get_chat_threads()
for chat_name, chat_id in zip(get_chats.title, get_chats.chatId):
    sub_client.send_message(message='BOT_RIN_ARI_TEST_ONLINE', chatId = chat_id)
    print('Тестовое сообщение отправлено')
    print(chat_name, chat_id)

###АКТИВАЦИЯ ИВЕНТОВ

@client.callbacks.event("TYPE_USER_SHARE_EXURL")
@client.callbacks.event("TYPE_USER_SHARE_USER")
@client.callbacks.event("on_voice_chat_not_answered")
@client.callbacks.event("on_voice_chat_not_cancelled")
@client.callbacks.event("on_voice_chat_not_declined")
@client.callbacks.event("on_video_chat_not_answered")
@client.callbacks.event("on_video_chat_not_cancelled")
@client.callbacks.event("on_video_chat_not_declined")
@client.callbacks.event("on_avatar_chat_not_answered")
@client.callbacks.event("on_avatar_chat_not_cancelled")
@client.callbacks.event("on_avatar_chat_not_declined")
@client.callbacks.event("on_delete_message")
@client.callbacks.event("on_group_member_join")
@client.callbacks.event("on_group_member_leave")
@client.callbacks.event("on_chat_invite")
@client.callbacks.event("on_chat_background_changed")
@client.callbacks.event("on_chat_title_changed")
@client.callbacks.event("on_chat_icon_changed")
@client.callbacks.event("on_voice_chat_start")
@client.callbacks.event("on_video_chat_start")
@client.callbacks.event("on_avatar_chat_start")
@client.callbacks.event("on_voice_chat_end")
@client.callbacks.event("on_video_chat_end")
@client.callbacks.event("on_avatar_chat_end")
@client.callbacks.event("on_chat_content_changed")
@client.callbacks.event("on_screen_room_start")
@client.callbacks.event("on_screen_room_end")
@client.callbacks.event("on_text_message_force_removed")
@client.callbacks.event("on_chat_removed_message")
###@client.callbacks.event("on_text_message")

###ЧТЕНИЕ ЧАТОВ

###def on_text_message(data):
###    print(f"{data.message.author.nickname}: {data.message.content}")

###ПРОВЕРКА НА НАЛИЧИЕ КОНТЕНТА И ТИПА СООБЩЕНИЯ + ЗАПУСК 2 потока

def handle_messages(data): 
    content = data.message.content
    media_type = data.message.mediaType
    print(content)
    if content and media_type == 0: ### Чтение сообщения и запись в переменные
        chatid = data.message.chatId 
        userid = data.message.author.userId
        nickname = data.message.author.nickname
        threading.Thread(target=exploit_message, args=[chatid, userid, nickname]).start() ### запуск 2 потока - спам

###РАБОТА СО СПАМОМ

def exploit_message(chatid: str, userid: str, nickname: str):
    try:
        sub_client.kick(userId=userid, chatId=chatid, allowRejoin=False)
        sub_client.send_message(chatId=chatid, message=f"{nickname} был удален из чата за отправку сообщения с измененным типом")
    except amino.exceptions.AccessDenied:
        pass
    except Exception as e:
        print(e)
    print(colored(f"{nickname} отправил сообщение с измененным типом в чате {chatid}", "red"))


def restart():
    while True:
        time.sleep(120)
        count = 0
        for i in threading.enumerate():
            if i.name == "restart_thread":
                count += 1
        if count <= 1:
            print("Restart")
            client.socket.close()
            client.socket.start()


if __name__ == '__main__':
    restart_thread = threading.Thread(target=restart)
    restart_thread.setName("restart_thread")
    restart_thread.start()
