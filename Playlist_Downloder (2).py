import re
from pytube import *
from youtube_transcript_api import YouTubeTranscriptApi as yt
from youtube_transcript_api.formatters import SRTFormatter
import os

def download_playlist( Link , Path , resolution_of_vedios , trans_per ) :
   playlist = Playlist( Link )   
   
   DOWNLOAD_PATH = r'{}'.format( Path )
   
   playlist._video_regex = re.compile( r"\"url\":\"(/watch\?v=[\w-]*)" )  
   '''
    This line sets a regular expression pattern on the playlist object. 
    This pattern is used to extract the video URLs from the playlist HTML page. 
    The regular expression looks for a string that starts with 
    "url":" and is followed by a YouTube video ID (a string of letters, numbers, and hyphens). 
    The re.compile() function creates a regular expression object from the pattern.
   '''   

   print( "\nI found {} vedios with URLs : ".format( len ( playlist.video_urls ) ) )  
     
  
   for url in playlist.video_urls :
        print ( url  )
   

   for video in playlist.videos:
        print ( '\ndownloading : {} with url : {}'.format( video.title , video.watch_url ) )

      #! call the function that will get vedio id 
        video_id = get_video_id(video.watch_url)

      #! Change all characters that cannot be used in a file name to "_"
        for i in ( '\\' , ':' , '*' , '\"' , '>' , '<' , '?' , '|' , ' ' ,  '^' , '.' ):
            video.title = video.title.replace(i,"_")
    
      #! download the vedio 
        video.streams.\
        filter( type = 'video' , progressive = True , file_extension = 'mp4' ,  res = resolution_of_vedios ).\
        order_by( 'resolution' ).\
        desc().\
        first().\
        download( DOWNLOAD_PATH )
    
      #! call the function that will download translation cript
        if trans_per == 'y':
              download_transcript( video_id , DOWNLOAD_PATH , video.title )


   print( '\n>>>>>>>>>>>>>>>>> completed <<<<<<<<<<<<<<<<<<<' )



    
    
    
def get_video_id(url):
  video_id = url.split("=")[-1]
  return video_id



def download_transcript( video_id , trans_path , filename ):
   transcript = yt.get_transcript( video_id , languages = ['en'] )
   formatter = SRTFormatter()

   STR_formatted = formatter.format_transcript( transcript )
   new_file_name = trans_path+r"\{}.srt".format( filename )
   old = trans_path + "\\aaa.srt"

   filepath = os.path.join( trans_path , old )
   
   with open( filepath , 'w', encoding = 'utf-8' ) as STR_file :
       STR_file.write( STR_formatted )

   os.rename(  old , new_file_name )
   

def download_sigle(Link , Path , resolution_of_vedios ):
    youtube = YouTube(Link)
    print ( '\ndownloading : {} with url : {}'.format( youtube.title , youtube.watch_url ) )
    video_stream = youtube.streams.filter( res = resolution_of_vedios ).first()
    video_stream.download( Path )
    
    
    print("Download complete!")


if __name__ == "__main__":

    choose = input(' What do you want \n 1 ) Download single video \n 2 ) Download Playlist  \n Your Choose is : ')

    if choose == '1':
        link = input( " Enter the link of the video : " )
        path = input( " Enter the path where the video will be downloaded : " )
        resolution_of_vedios = input( " Enter the resolution of the video you want to download (360p, 720p, 1080p ): " )
        download_sigle( link , path , resolution_of_vedios )


    elif choose == '2' :
       link = input( " Enter the link of the  playlist : " )
       path = input( " Enter the path where the videos will be downloaded : " )
       resolution_of_vedios = input( " Enter the resolution of the videos you want to download (360p, 720p, 1080p ): " )
       Translation_permission = input( " Do you want to download the Translation script of the video  y / n ?  " )
       download_playlist( link , path , resolution_of_vedios , Translation_permission )