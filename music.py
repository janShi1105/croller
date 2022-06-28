import concurrent.futures
import random
import time
from collections import namedtuple
from os import path
from urllib import parse

import requests

from my_logging import get_my_logger

logger = get_my_logger(__name__)

Music = namedtuple('music', 'file_name, file_content')

RANDOM_SLEEP_TIMES = [x * 0.1 for x in range(10, 40, 5)]

MUSIC_URLS = [
    'https://archive.org/download/ThePianoMusicOfMauriceRavel/01PavanePourUneInfanteDfuntePourPianoMr19.mp3',
    'https://archive.org/download/ThePianoMusicOfMauriceRavel/02JeuxDeauPourPianoMr30.mp3',
    'https://archive.org/download/ThePianoMusicOfMauriceRavel/03SonatinePourPianoMr40-Modr.mp3',
    'https://archive.org/download/ThePianoMusicOfMauriceRavel/04MouvementDeMenuet.mp3',
    'https://archive.org/download/ThePianoMusicOfMauriceRavel/05Anim.mp3',
]

def download(url, timeout=180):
    parsed_url = parse.urlparse(url)
    file_name = path.basename(parsed_url.path)

    sleep_time = random.choice(RANDOM_SLEEP_TIMES)

    logger.info("[download start] sleep: {time} {file_name}".format(time=sleep_time, file_name=file_name))

    time.sleep(sleep_time)

    r = requests.get(url, timeout=timeout)

    logger.info("[download finished] {file_name}".format(file_name=file_name))

    return Music(file_name=file_name, file_content=r.content)

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        logger.info("[main start]")

        futures = [executor.submit(download, music_url) for music_url in MUSIC_URLS]

        for future in concurrent.futures.as_completed(futures):
            music = future.result()

            with open(music.file_name, 'wb') as fw:
                fw.write(music.file_content)
        logger.info("[main finished]")