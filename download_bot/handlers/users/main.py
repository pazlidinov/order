import os
from aiogram import types
from loader import dp, bot
import yt_dlp
from moviepy.editor import VideoFileClip, AudioFileClip


async def download_from_youtube(url):
    # Video yuklash
    ydl_opts_video = {
        "format": "bestvideo",
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


async def download_from_others(url):
    yt_opts = {"outtmpl": "downloads/%(title)s.%(ext)s"}
    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info_dict)


@dp.message_handler(regexp=r"https?://[^\s]+")
async def download_video(message: types.Message):
    video_url = message.text
    bot_username = (await bot.get_me()).username
    await message.reply("Videoni yuklab olishni boshlayapman. Bir oz kuting...")

    # Videoni yuklab olish
    video_path = (
        await download_from_youtube(video_url)
        if "youtu" in video_url
        else await download_from_others(video_url)
    )

    if video_path:
        # Foydalanuvchiga videoni yuborish
        with open(video_path, "rb") as video:
            await message.reply_video(
                video,
                caption=f"\nBot manzili - <a href='https://t.me/{bot_username}?start={message.from_user.id}'>{bot_username}</a>\n",
            )
            os.remove(video_path)
    else:
        await message.reply(
            "Videoni yuklab bo'lmadi. Iltimos, linkni tekshiring yoki boshqa video yuboring."
        )
