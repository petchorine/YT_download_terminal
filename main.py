import os
import ffmpeg
import shutil

from pytube import Playlist, YouTube


# liens pour les tests
# playlist courte : https://www.youtube.com/playlist?list=PL6wtbJKOh3fGOVxYNrL7nRQT6wcaThm7m
# video 4k = https://www.youtube.com/watch?v=LXb3EKWsInQ&t=1s


def introduction():
    print(""""
                #####################################
                #                                   #
                # Bienvenue dans YOUTUBE DOWNLOADER #
                #                par                # 
                #             Petchorine            #
                #####################################
    """)

def get_url_and_verify_integrity():
    while True:
        print("\n")
        print("Copier-coller l'url de la video ou la playlist que vous souhaitez télécharger.")
        user_url = input("=> ")
        if user_url.startswith("https://www.youtube.com"):
            print("L'url est valide. Nous allons pouvoir commencer le téléchargement.")
            print("\n")
            print("Voici les clips associés à cette url :")
            print("\n")
            break
        else:
            print("Il semble qu'il y ait une erreur dans l'url. Essaye de copier à nouveau.")
            continue
    return user_url


def is_not_playlist(url):
    if "playlist" not in url:
        return True
    else:
        return False


def show_playlist(url):
    playlist_youtube_video = []
    if is_not_playlist(url) == True:
        youtube_video = YouTube(url)
        playlist_youtube_video.append(youtube_video)
    else:
        p = Playlist(url)
        for url in p.video_urls:
            youtube_video = YouTube(url)
            playlist_youtube_video.append(youtube_video) 
    

    for youtube_video in playlist_youtube_video:
        print(f"{youtube_video.title} - {str(youtube_video.length//60)}.{str(youtube_video.length%60)}")
    
    return playlist_youtube_video
  

def choice_audio_or_video():    
    print("\n")
    print("Tu veux télécharger le(s) clip(s) audio/vidéo ou seulement l'audio ?")
    print("1 - le(s) clip(s) audio/vidéo")
    print("2 - seulement l'audio")
    
    user_choice = ""
    while True:
        user_choice = input("=> ")
        if user_choice == "1":
            print("Tu as choisi de télécharger le (ou les) vidéos.")            
        elif user_choice == "2":
            print("Tu as choisi de télécharger le (ou les) audios.")
        else:
            print("Tu dois entrer soit 1, soit 2.")
            continue
        return user_choice


def resolution_choice(choice_media_type, playlist):
    if choice_media_type == "1":
        quality = ("qualité optimale", "qualité moyenne", "qualité minimale")
        print("\n")
        print(f"Choisissez la qualité des médias à télécharger :")
        print(f"1 - {quality[0]}")
        print(f"2 - {quality[1]}")
        print(f"3 - {quality[2]}")
        while True:
            user_quality_choice = input("=> ")
            if user_quality_choice == "1" or user_quality_choice == "2" or user_quality_choice == "3":
                print(f"Tu as choisi : {quality[int(user_quality_choice) - 1]}")
                print("\n")
                get_resolutions_list(playlist, int(user_quality_choice))
            else:
                print("Tu dois entrer 1, 2 ou 3.")
                continue
    elif choice_media_type == "2":
        download_audio(playlist)


def get_resolutions_list(playlist, user_quality_choice):    
    if user_quality_choice == 1:
        video_stream_list = []
        audio_stream_list = []
        
        for clip in playlist:
            video_stream_list.append(clip.streams.filter(progressive=False, file_extension="mp4", type="video").order_by("resolution").desc())
            audio_stream_list.append(clip.streams.filter(progressive=False, file_extension="mp4", type="audio").order_by("abr").desc())
        
        best_audio_resolutions_list = []
        for idx in range(len(audio_stream_list)):
            best_audio_stream = audio_stream_list[idx][0]
            best_audio_resolutions_list.append(best_audio_stream)      
        
        best_video_resolutions_list = []
        for idx in range(len(video_stream_list)):
            best_video_stream = video_stream_list[idx][0]
            best_video_resolutions_list.append(best_video_stream)         
        download_video(best_video_resolutions_list, list_audio=best_audio_resolutions_list) 
    
    elif user_quality_choice == 2:
        video_stream_list = []
        for clip in playlist:
            video_stream_list.append(clip.streams.filter(progressive=True, file_extension="mp4", type="video").order_by("resolution").desc())  
        
        medium_resolutions_list = []        
        for idx in range(len(video_stream_list)):
            medium_video_stream = video_stream_list[idx][0]
            medium_resolutions_list.append(medium_video_stream)
        download_video(medium_resolutions_list)
    
    elif user_quality_choice == 3:
        video_stream_list = []
        for clip in playlist:
            video_stream_list.append(clip.streams.filter(progressive=True, file_extension="mp4", type="video").order_by("resolution").desc())  
        
        lowest_resolutions_list = []
        for idx in range(len(video_stream_list)):
            lowest_video_stream = video_stream_list[idx][-1]
            lowest_resolutions_list.append(lowest_video_stream)
        download_video(lowest_resolutions_list)

def download_video(resolutions_list, list_audio=None):
    # TELECHARGEMENT AUDIO
    if list_audio is not None:
        for best_audio in list_audio:
            print("Téléchargement audio...")
            best_audio.download("audio_ytdown")
            print("ok")

    for stream_video in resolutions_list:
        if stream_video.is_progressive == False:               
            # TELECHARGEMENT VIDEO
            print("Téléchargement video...")
            stream_video.download("video_ytdown")
            print("OK")

            # COMBINAISON DES FICHIERS AUDIO ET VIDEO
            audio_filename = os.path.join("audio_ytdown", best_audio.default_filename)
            video_filename = os.path.join("video_ytdown", stream_video.default_filename)
            output_filename = stream_video.default_filename

            print("Combinaison des fichiers...")
            ffmpeg.output(ffmpeg.input(audio_filename), ffmpeg.input(video_filename), output_filename,
                            vcodec="copy", acodec="copy", loglevel="quiet").run(overwrite_output=True)
            print("ok")
        else:
            print(f"Téléchargement...")
            stream_video.download()
            print("OK")
    # à la fin de l'opération de combinaison => suppr. des fichiers/dossiers temporaires audio/video
    # si les dossiers ont été crées (dans le cas qualité optimale seulement) / pas d'erreur si autre qualité choisie 
    if os.path.isdir("audio_ytdown"):
        shutil.rmtree('audio_ytdown')
    if os.path.isdir("video_ytdown"):
        shutil.rmtree('video_ytdown')


def download_audio(playlist_audio_to_download):
    all_audio_streams = []
    all_best_audio_streams = []
    
    for clip in playlist_audio_to_download:
        audio_stream = clip.streams.filter(progressive=False, file_extension="mp4", type="audio").order_by(
        "abr").desc()
        all_audio_streams.append(audio_stream)

    for stream in all_audio_streams:
        best_stream = stream[0]
        all_best_audio_streams.append(best_stream)
        print("Téléchargement...")
        # TODO : je ne sais pas encore comment spécifier mon dossier de téléchargement
        # sans doute avec le module os
        best_stream.download()
        print("OK")

    return all_best_audio_streams

def ending():
    print("this is the end")



def main():
    introduction()
    user_url_input = get_url_and_verify_integrity()
    is_not_playlist(user_url_input)
    playlist = show_playlist(user_url_input)
    choice_media_type = choice_audio_or_video()
    resolution_choice(choice_media_type, playlist)
    ending()

main()







