from objects import Playlist, Song
import os

playlistdir = 'playlists'

files = os.listdir(playlistdir)
playlists = []
if len(files)>1:
    main_playlist_file = None
    for i,file in enumerate(files):
        if file.startswith('Музыка'):
            main_playlist_file = files.pop(i)
            continue
        playlists.append(Playlist(os.path.join(playlistdir,file)))
    if main_playlist_file is None:
        for file in playlists:
            file.get_all_songs()
    else:
        main_playlist = Playlist(os.path.join(playlistdir,main_playlist_file))

        for file in playlists:
            main_playlist - file
            file.get_all_songs()
        main_playlist.get_all_songs()
else:
    p = Playlist(os.path.join(playlistdir, files[0]))
    p.get_all_songs()

print(1)


