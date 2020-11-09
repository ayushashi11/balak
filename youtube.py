import subprocess
import os
from pytube import YouTube
from youtube_search import YoutubeSearch
async def search(ctx, txt, key):
  await ctx.send('this command is under redevelopment\nyoutube-dl was removed recently, which cripples this functionality, the bot might get stuck while using this, if such a thing happens, contact the developer asap')
  if key != "balakaloogobi":
    await ctx.send("incorrect developer key")
    return 
  try:
    await ctx.send("removing text.mp3...")
    os.remove("text.mp3")
  except BaseException as e:
    print(e)
  await ctx.send("search phase 1..")
  results = YoutubeSearch(txt, max_results=1).videos
  await ctx.send("phase 2...")
  print(results)
  url = "https://youtube.com"+results[0]["url_suffix"]
  print(url)
  yt=YouTube(url)
  st=yt.streams.filter(only_audio=True)
  await ctx.send("downloading....")
  st[0].download(".",filename="text")
  print(os.listdir())
  res=subprocess.Popen(["ffmpeg","-i","text.mp4","text.mp3"])
  while res.poll() is None:
    pass
  os.remove("text.mp4")
  return results
