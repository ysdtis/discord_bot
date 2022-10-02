# インストールした discord.py を読み込む
import discord
import random
import pickle
import os
from dotenv import load_dotenv

# .envファイルの内容を読み込む
load_dotenv()

path = os.getcwd()

reply_path = os.path.join(path,"reply.sav")
list_path = os.path.join(path,"list.sav")

# 接続に必要なオブジェクトを生成
client = discord.Client()

async def get_filetext(path, text = None):
    try:
        file = open(path,"rb")
        texten = pickle.load(file)
        file.close
    except:
        texten = None

    if text is None:
        return texten
    else:
        return texten.get(text)

async def save(key, text):
    try:
        texten = await get_filetext(reply_path)
        file = open(reply_path, 'wb')
        file.dump(texten, file)
        file.close
    except:
        return False

"""Bot起動時に実行されるイベントハンドラ"""
# 起動時に動作する処理
@client.event # イベントを受信するための構文（デコレータ）
async def on_ready(): # イベントに対応する関数と受け取る引数
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました') # 処理いろいろ

"""メッセージ受信時に実行されるイベントハンドラ"""
# メッセージ受信時に動作する処理
@client.event
async def on_message(message):

    if client.user in message.mentions: # 話しかけられたかの判定
        await reply(message) # 返信する非同期関数を実行

    if message.author == client.user:
        return
    randomizer = random.randint(0,len(texten)-1)
    random2 = random.randint(1,1) #返信を行う頻度を変更可能 ex) ...randint(1,100) 1%の確立で返信
    if random2 == 1:
        await message.channel.send(texten[randomizer])
    if message.content.startswith("Save"):  #誰かがSaveと発言すると蓄積したデータが実際にファイルに保存される。
        file =open(reply_path, "wb")
        pickle.dump(texten,file)
        file.close()
        print("textfile Saved!")
    else:
        texten.append(message.content)

# 返信する非同期関数を定義
async def reply(message):
    if message.content.startswith('/l'):  #誰かが/lと発言すると指定したワードでリプライ対象の語録を学習する。

    reply = f'{message.author.mention} 呼んだ？' # 返信メッセージの作成
    await message.channel.send(reply) # 返信メッセージを送信

# Botの起動とDiscordサーバーへの接続
client.run(os.environ['TOKEN'])