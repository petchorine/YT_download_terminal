import os
import ffmpeg
import shutil
import tkinter
import tkinter.filedialog
from pathlib import Path
from pytube import Playlist, YouTube


# liens pour les tests
# playlist courte : https://www.youtube.com/playlist?list=PL6wtbJKOh3fGOVxYNrL7nRQT6wcaThm7m
# video 4k = https://www.youtube.com/watch?v=LXb3EKWsInQ&t=1s
# video 1080 = https://www.youtube.com/watch?v=6kqivnW1OBM


def introduction():
    print(""""
                #########################################
                #                                       #
                #   Bienvenue dans YOUTUBE DOWNLOADER   #
                #                  par                  # 
                #               Petchorine              #
                #                                       #
                #########################################
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
    
    print("Titre(s)" + (45 * ' ') + "Durée")
    print((50 * '=') + '   ' + (5 * '='))
    for youtube_video in playlist_youtube_video:
        if len(youtube_video.title) > 50:
            print(f"{youtube_video.title[:45]}...     {str(youtube_video.length//60)}.{str(youtube_video.length%60)}")
        else:
            print(youtube_video.title + ((53 - len(youtube_video.title)) * ' ') + str(youtube_video.length//60) + '.' +str(youtube_video.length%60))
    
    return playlist_youtube_video
  

def choice_audio_or_video():    
    print("\n")
    print("Tu veux télécharger le(s) clip(s) audio/vidéo ou seulement l'audio ?")
    print("   1 - le(s) clip(s) audio/vidéo")
    print("   2 - seulement l'audio")
    
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
        print(f"Choisis la qualité des médias à télécharger :")
        print(f"   1 - {quality[0]}")
        print(f"   2 - {quality[1]}")
        print(f"   3 - {quality[2]}")
        while True:
            user_quality_choice = input("=> ")
            if user_quality_choice == "1" or user_quality_choice == "2" or user_quality_choice == "3":
                print(f"Tu as choisi : {quality[int(user_quality_choice) - 1]}")
                print("\n")
                break
            else:
                print("Tu dois entrer 1, 2 ou 3.")
                continue
        get_resolutions_list(playlist, int(user_quality_choice))
    elif choice_media_type == "2":
        user_directory_choice = directory_choice()
        download_audio(playlist, user_directory_choice)

def directory_choice():
    # on initialise tkinter en appelant la fonction Tk()
    racine_tk = tkinter.Tk()
    # permet de masquer la petite fenêtre supplémentaire (je ne sais pas à quoi elle sert ???)
    racine_tk.withdraw()

    print("Dans quel dossier souhaites-tu télécharger tes clips ?")
    print("Note : si tu ne vois pas la fenêtre de choix, elle peut être cachée derrière la fenêtre du script !")
    directory_name = tkinter.filedialog.askdirectory(title='Choisir un dossier')
    
    
    if len(directory_name) != 0:
        user_directory_choice = Path(directory_name)
    else:
        script_directory = os.path.realpath(__file__)
        user_directory_choice = os.path.dirname(script_directory)    
    print("Chemin complet du dossier : ", user_directory_choice)

    return user_directory_choice


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
        user_directory_choice = directory_choice()
        download_video(best_video_resolutions_list, user_directory_choice, list_audio=best_audio_resolutions_list) 
    
    elif user_quality_choice == 2:
        video_stream_list = []
        for clip in playlist:
            video_stream_list.append(clip.streams.filter(progressive=True, file_extension="mp4", type="video").order_by("resolution").desc())  
        
        medium_resolutions_list = []        
        for idx in range(len(video_stream_list)):
            medium_video_stream = video_stream_list[idx][0]
            medium_resolutions_list.append(medium_video_stream)
        user_directory_choice = directory_choice()
        download_video(medium_resolutions_list, user_directory_choice)
    
    elif user_quality_choice == 3:
        video_stream_list = []
        for clip in playlist:
            video_stream_list.append(clip.streams.filter(progressive=True, file_extension="mp4", type="video").order_by("resolution").desc())  
        
        lowest_resolutions_list = []
        for idx in range(len(video_stream_list)):
            lowest_video_stream = video_stream_list[idx][-1]
            lowest_resolutions_list.append(lowest_video_stream)
        user_directory_choice = directory_choice()
        download_video(lowest_resolutions_list, user_directory_choice)


def download_video(resolutions_list, user_directory_choice, list_audio=None):
    # TELECHARGEMENT AUDIO
    audio_temp_directory = fr"{user_directory_choice}\audio_ytdown"
    if list_audio is not None:
        for best_audio in list_audio:
            print("Téléchargement audio...")
            best_audio.download(audio_temp_directory)
            print("ok")

    video_temp_directory = fr"{user_directory_choice}\video_ytdown"  
    for stream_video in resolutions_list:
        if stream_video.is_progressive == False:     
            # TELECHARGEMENT VIDEO
            print("Téléchargement video...")            
            stream_video.download(video_temp_directory)
            print("ok")

            # COMBINAISON DES FICHIERS AUDIO ET VIDEO
            audio_filename = os.path.join(user_directory_choice, "audio_ytdown", best_audio.default_filename)
            video_filename = os.path.join(user_directory_choice, "video_ytdown", stream_video.default_filename)
            output_filename = os.path.join(user_directory_choice, stream_video.default_filename)

            print("Combinaison des fichiers...")
            ffmpeg.output(ffmpeg.input(audio_filename), ffmpeg.input(video_filename), output_filename,
                            vcodec="copy", acodec="copy", loglevel="quiet").run(overwrite_output=True)
            print("ok")
        else:
            print(f"Téléchargement...")
            stream_video.download(user_directory_choice)
            print("OK")
    
    # à la fin de l'opération de combinaison => suppr. des fichiers/dossiers temporaires audio/video
    # si les dossiers ont été crées (dans le cas qualité optimale seulement) / pas d'erreur si autre qualité choisie 
    if os.path.isdir(audio_temp_directory):
        shutil.rmtree(audio_temp_directory)
    if os.path.isdir(video_temp_directory):
        shutil.rmtree(video_temp_directory)


def download_audio(playlist_audio_to_download, user_directory_choice):
    all_audio_streams = []
    print("\n")
    for clip in playlist_audio_to_download:
        audio_stream = clip.streams.filter(progressive=False, file_extension="mp4", type="audio").order_by(
        "abr").desc()
        all_audio_streams.append(audio_stream)

    for stream in all_audio_streams:
        best_stream = stream[0]
        print("Téléchargement...")
        best_stream.download(output_path = user_directory_choice)
        print("OK")


def ending():
    print("\n")
    print(f"Tous les clips ont bien été téléchargés...")
    print("\n")
    print("Veux-tu télécharger autre chose ?")
    print("   1 - oui")
    print("   2 - non, je souhaite quitter le programme.")
    while True:
        user_reload_choice = input("=> ")
        if user_reload_choice == "1":
            main()
        elif user_reload_choice == "2":
            quit()
        else:
            print("Tu dois choisir soit 1, soit 2.")
            continue


def main():
    introduction()
    user_url_input = get_url_and_verify_integrity()
    is_not_playlist(user_url_input)
    playlist = show_playlist(user_url_input)
    choice_media_type = choice_audio_or_video()
    resolution_choice(choice_media_type, playlist)
    ending()

main()







