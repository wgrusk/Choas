import json
import requests
import time
import sys

CNN_CHANNEL_ID = 'UCupvZG-5ko_eiXAupbDfxWw'

# def hourCheck(mins):
#     mins = 0
#     while mins != 60:
#         time.sleep(60)
#         mins++;
#     id = findvid()

def userInput():
    id = input("Input Video ID: ")
    r = requests.get('https://www.googleapis.com/youtube/v3/videos?part=snippet&id=' + id + '&fields=items/snippet/description&key=AIzaSyAjM0NQVnhEvRY15_bhib3y1m0ilQjdjx0')
    description = json.loads(r.text)
    seed = description["items"][0]["snippet"]["description"].split()
    seed = seed[0:8]
    print(seed)

def cnnTimer():
    # while True:
        r = requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&fields=items/snippet/description,items/id/videoId&channelId=' + CNN_CHANNEL_ID + '&maxResults=1&order=date&type=video&key=AIzaSyAjM0NQVnhEvRY15_bhib3y1m0ilQjdjx0')
        description = json.loads(r.text)
        id = description["items"][0]["id"]["videoId"]
        print(id)


def main():
    if sys.argv[1] == "1":
        userInput()
    elif sys.argv[1] == "2":
        cnnTimer()
    else:
        print("Incorrect Command Line Argument(s)")

if __name__ == "__main__":
    main()
