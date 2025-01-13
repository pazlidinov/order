import os
import requests
from aiogram import types
from loader import dp, bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import yt_dlp
from moviepy.editor import VideoFileClip, AudioFileClip


VIDEO_URL = ""


async def get_share_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    bot_username = (await bot.get_me()).username
    # Botni ulashish tugmasi yaratish
    share_button = InlineKeyboardButton(
        text="Botni ulashish", url=f"https://t.me/{bot_username}"  # Botning URL manzili
    )
    keyboard.add(share_button)
    return keyboard


async def download_from_youtube(url, format_id):
    # Video yuklash
    ydl_opts_video = {
        "format": format_id,
        "outtmpl": "downloads/video.mp4",
    }
    with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
        ydl.download([url])

    # Audio yuklash
    ydl_opts_audio = {
        "format": "bestaudio",
        "outtmpl": "downloads/audio.m4a",
    }
    with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
        ydl.download([url])

    # Video va audio fayllarni yuklash
    video_clip = VideoFileClip("downloads/video.mp4")
    audio_clip = AudioFileClip("downloads/audio.m4a")

    # Videoga audiolarni qo'shish
    final_clip = video_clip.set_audio(audio_clip)

    # Yangi video faylni saqlash

    final_clip.write_videofile(
        "downloads/output.mp4", codec="libx264", audio_codec="aac"
    )
    os.remove("downloads/video.mp4")
    os.remove("downloads/audio.m4a")
    return "downloads/output.mp4"


async def get_youtube_formats(url, message):
    try:
        # yt-dlp yordamida formatlarni olish
        ydl_opts = {"quiet": True}  # Konsol chiqishini o'chirish
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])

            list_formats = {}
            for fmt in formats:
                if "p)" in fmt.get("format"):
                    one_format = fmt.get("format").split(" ")
                    list_formats[one_format[-1]] = one_format[0]
        return list_formats
    except Exception as e:
        await message.reply(f"Xato yuz berdi")


async def download_from_instagram(url):
    yt_opts = {"outtmpl": "downloads/%(title)s.%(ext)s"}
    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info_dict)



# TikTok videoni yuklab olish uchun funksiya
async def download_tiktok_video(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        logging.info(response)
        
        if response.status_code == 200:
            return response.content  # video faylini olish
        else:
            return None
    except Exception as e:
        return None


async def send_video(message, video_path):
    bot_username = (await bot.get_me()).username

    if video_path:
        # Foydalanuvchiga videoni yuborish
        with open(video_path, "rb") as video:
            await message.reply_video(
                video,
                caption=f"\nBot manzili - <a href='https://t.me/{bot_username}?start={message.from_user.id}'>{bot_username}</a>\n",
                reply_markup=await get_share_keyboard(),
            )
            os.remove(video_path)
    else:
        await message.reply(
            "Videoni yuklab bo'lmadi. Iltimos, linkni tekshiring yoki boshqa video yuboring."
        )


@dp.message_handler(regexp=r"https?://[^\s]+")
async def accept_link(message: types.Message):
    global VIDEO_URL
    VIDEO_URL = message.text
    if "youtu" in VIDEO_URL:
        list_formats = await get_youtube_formats(VIDEO_URL, message)
        inline_keyboard = InlineKeyboardMarkup(row_width=2)
        for key, item in list_formats.items():
            format_btn = InlineKeyboardButton(key, callback_data=f"format_{item}")
            inline_keyboard.add(format_btn)
        await message.answer(
            "YouTube video formatini tanlang:", reply_markup=inline_keyboard
        )

    if "instagram.com" in VIDEO_URL:
        await message.reply("Videoni yuklab olishni boshlayapman. Bir oz kuting...")
        video_path = await download_from_instagram(VIDEO_URL)
        await send_video(message, video_path)

    if "tiktok.com" in VIDEO_URL:
        await message.reply("Videoni yuklab olishni boshlayapman. Bir oz kuting...")
        video_path = await download_tiktok_video(VIDEO_URL)
        await send_video(message, video_path)


# Callback queryni qayta ishlash
@dp.callback_query_handler(lambda c: c.data.startswith("format_"))
async def process_format_selection(callback_query: types.CallbackQuery):
    global VIDEO_URL
    format_id = callback_query.data.split("_")[1]

    await bot.answer_callback_query(
        callback_query.id, "Videoni yuklab olishni boshlayapman. Bir oz kuting..."
    )

    video_path = await download_from_youtube(VIDEO_URL, format_id)
    bot_username = (await bot.get_me()).username

    if video_path:
        # Foydalanuvchiga videoni yuborish
        with open(video_path, "rb") as video:
            await bot.send_video(
                callback_query.from_user.id,
                video=video,
                caption=f"\nBot manzili - <a href='https://t.me/{bot_username}?start={callback_query.from_user.id}'>{bot_username}</a>\n",
                reply_markup=await get_share_keyboard(),
            )
            os.remove(video_path)
    else:
        await bot.answer_callback_query(
            "Videoni yuklab bo'lmadi. Iltimos, linkni tekshiring yoki boshqa video yuboring."
        )

    