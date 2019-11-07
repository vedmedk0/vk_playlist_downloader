import os
import requests
from mp3_tagger import MP3File, VERSION_BOTH, VERSION_1, VERSION_2

download_dir = '.\download'


class Song:
    track = None

    def __init__(self, name, author, album, download_link):
        self.name = name
        self.author = author
        self.album = album
        self.download_link = download_link

    def __repr__(self):
        return f'{self.author} - {self.name.replace(r"/","").replace(r"*","").replace(r"|","").replace(r"?","")}'

    def __str__(self):
        return f'{self.author} - {self.name.replace(r"/","").replace(r"*","").replace(r"|","").replace(r"?","")}'


    def _download_file(self):
        r = requests.get(self.download_link)

        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        with open(os.path.join(self.download_path, f'{self}.mp3'), 'wb') as f:
            f.write(r.content)

    def _fill_tags(self):
        mp3 = MP3File(os.path.join(self.download_path, f"{self}.mp3"))
        mp3.set_version(VERSION_BOTH)
        mp3.artist = self.author
        mp3.album = self.album
        mp3.song = self.name
        if self.track is not None:
            mp3.track = str(self.track)
        mp3.save()

    @property
    def download_path(self):
        if self.album == '':
            return download_dir
        else:
            return os.path.join(download_dir, self.album)

    def get_track(self):
        try:
            if not os.path.exists(os.path.join(self.download_path, f"{self}.mp3")):
                self._download_file()
                self._fill_tags()
                self._fill_tags()
        except Exception as e:
            print(f'не удалось скачать {self}, ошибка:{str(e)}')


class Playlist:

    def __init__(self, file_link):
        self.file_link = file_link
        self.songlist = []
        self.album = ''
        file_name = os.path.basename(file_link)
        if not file_name.startswith('Музыка'):
            self.album = file_name.split('2', 1)[0].strip()
        self.parse_file_to_songlist()

    def __repr__(self):
        return f'{self.album}'

    def extract_author_song(self, line):
        author_song = line.split(',', 1)[1]
        author, song = [s.strip() for s in author_song.split('-', 1)]
        return author, song

    def parse_file_to_songlist(self):
        author = ''
        song = ''
        link = ''
        tracknum=1
        with open(self.file_link, 'r',encoding='utf-8') as f:
            for line in f:
                if line.startswith('#EXTM3U'):
                    continue
                elif line.startswith('#EXTINF'):
                    author, song = self.extract_author_song(line)
                else:
                    link = line
                    newsong = Song(song, author, self.album, link)
                    if self.album!='':
                        newsong.track=tracknum
                        tracknum+=1
                    self.songlist.append(newsong)

    def get_all_songs(self):
        for i,song in enumerate(self.songlist):
            song.get_track()
            print(f'downloaded {song} | {i}/{len(self.songlist)}')

    def __sub__(self, other):
        songs_to_exclude = [str(song) for song in other.songlist]
        self.songlist = [song for song in self.songlist if str(song) not in songs_to_exclude]


if __name__ == "__main__":
    p = Playlist('playlists/Музыка сообщества 7XVN 2019-10-23 20-59_dokach.m3u')
    p.get_all_songs()
    print(1)
