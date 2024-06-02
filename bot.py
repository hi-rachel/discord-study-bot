import os
from dotenv import load_dotenv
import config
import asyncio
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

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# 매 월 새로운 달이 시작될 때 출석 횟수 초기화
async def reset_monthly_attendance():
    global attendance_counts
    while True:
        now = datetime.now()
        if now.day == 1 and now.hour == 0 and now.minute == 0:
            attendance_counts = {}  # 출석 횟수 초기화
            print("새로운 달이 시작되었습니다. 출석 횟수를 초기화합니다.")
        await asyncio.sleep(60 * 60 * 24 * 7)  # 1주일마다 한 번씩 검사

# 멤버별 출석 횟수를 저장하는 딕셔너리
attendance_counts = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    bot.loop.create_task(reset_monthly_attendance())
    check_voice_channel.start()

@tasks.loop(minutes=1)
async def check_voice_channel():
    now = datetime.now()
    if now.hour == int(config.TARGET_HOUR) and now.minute == int(config.TARGET_MINUTE) and now.strftime("%A") in config.TARGET_DAYS:
        print("출석체크 시간!")
        for guild in bot.guilds:
            voice_channel = discord.utils.get(guild.voice_channels, name=config.VOICE_CHANNEL)  # 음성 채널 이름으로 변경
            if voice_channel is not None:
                members = voice_channel.members
                member_list = []
                for member in members:
                    # Discord 유저의 ID를 사용하여 출석 기록 유지
                    user_id = str(member.id)
                    nickname = member.nick if member.nick else member.global_name  # 닉네임이 없으면 사용자 이름 사용
                    attendance_counts[user_id] = attendance_counts.get(user_id, 0) + 1
                    member_list.append(f"{nickname}({attendance_counts[user_id]}회)")
                channel = discord.utils.get(guild.text_channels, name=config.CHATTING_CHANNEL)  # 채팅 채널 이름으로 변경
                if channel is not None:
                    # 출석 명단 메시지 생성
                    attendance_message = f"[{now.strftime('%Y-%m-%d')} {now.strftime('%a')} 출석 명단 ({len(member_list)}명)]\n"
                    attendance_message += f"{now.month}월 {config.STUDY_CLUB_NAME} 스터디에 참여한 명단입니다 😃👍🏻\n"
                    attendance_message += ", ".join(member_list)
                    await channel.send(attendance_message)
                    print('성공적으로 출석체크 메시지를 보냈습니다.')

bot.run(DISCORD_TOKEN)
