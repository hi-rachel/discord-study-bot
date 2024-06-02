import os
from dotenv import load_dotenv
import discord
from discord.ext import tasks, commands
from datetime import datetime

# 환경 변수를 사용하기 위해 필요합니다.
load_dotenv()

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# 환경 변수에서 특정 요일과 시간을 가져옵니다.
TARGET_DAYS = os.getenv("TARGET_DAYS").split(',')  # 기본값은 일요일, 월요일입니다.
TARGET_HOUR = int(os.getenv("TARGET_HOUR"))  # 기본값은 21시입니다.
TARGET_MINUTE = int(os.getenv("TARGET_MINUTE"))  # 기본값은 0분입니다.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    check_voice_channel.start()

@tasks.loop(minutes=1)
async def check_voice_channel():
    now = datetime.now()
    if now.hour == TARGET_HOUR and now.minute == TARGET_MINUTE and now.strftime("%A") in TARGET_DAYS:
        print("출석체크 시간!")
        for guild in bot.guilds:
            voice_channel = discord.utils.get(guild.voice_channels, name='책 읽는 공간')  # 음성 채널 이름으로 변경
            if voice_channel is not None:
                members = voice_channel.members
                member_names = []
                for member in members:
                    nickname = member.nick  # 닉네임 확인
                    if nickname is None:
                        nickname = member.global_name  # 닉네임이 없으면 전역 이름 사용
                    member_names.append(nickname)
                channel = discord.utils.get(guild.text_channels, name='출석-관리')  # 채팅 채널 이름으로 변경
                if channel is not None:
                    # 출석 명단 메시지 생성
                    attendance_message = f"[{now.strftime('%Y-%m-%d')} {now.strftime('%A')} 출석 명단 ({len(member_names)}명)]\n"
                    attendance_message += "오늘 모각북클럽 스터디에 참여한 명단입니다 😃👍🏻\n"
                    attendance_message += ", ".join(member_names)
                    await channel.send(attendance_message)
                    print('성공적으로 출석체크 메시지를 보냈습니다.')

bot.run(DISCORD_TOKEN)
