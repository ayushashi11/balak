import subprocess
import os
from pytube import YouTube
from youtube_search import YoutubeSearch
async def search(ctx, txt):
  try:
    os.remove("text.mp3")
  except BaseException as e:
    print(e)
  results = YoutubeSearch(txt, max_results=1).videos
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
