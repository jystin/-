from pydub import AudioSegment
 
 
 
filename ='MP3/jn.mp3'
output_filename = 'MP3/jn_seg.mp3'
 
mp3 = AudioSegment.from_mp3(filename) # 打开mp3文件
slice=mp3[1440000:1740000]
slice.export(output_filename, format="mp3") # 切割前16秒并覆盖保存