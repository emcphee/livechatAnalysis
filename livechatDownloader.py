from chat_downloader import ChatDownloader
import os
import pathlib
import scrapetube
import datetime

class youtubeLivechatDownloader:
    # checks if the channel videolist has already been downloaded
    def __init__(self, _channelID: str, _forceRecollect: bool = False):
        self.startuptime = datetime.datetime.now()
        self.startuptimeAsWinCompliantStr = str(self.startuptime).replace(":","-")
        self.forceRecollect = _forceRecollect
        self.channelID = _channelID
        if not os.path.exists("channelVideoURLs/"+self.channelID+".txt") or self.forceRecollect:
            print("URL list not found. Downloading now..." if not self.forceRecollect else "forceRecollect enabled. Downloading URL list now...")
            urls = self.retrieveVideoURLs()
            self.writeURLs(urls)
            self.videoIDs = urls
            print("URL list successfully downloaded")
        else:
            self.videoIDs = self.loadVideoIDsFromFile()

    
    def loadVideoIDsFromFile(self):
        readFile = open("channelVideoURLs/"+self.channelID+".txt", encoding="utf-8")
        ids = readFile.readlines()
        ids_without_newlines = []
        for id in ids:
            ids_without_newlines.append(id[:-1])
        return ids_without_newlines


    def retrieveVideoURLs(self):
        videoIDs = []
        videos = scrapetube.get_channel(self.channelID)
        for video in videos:
            videoIDs.append(video['videoId'])
        
        # for whatever reason it doublecounts urls so I remove dupes using a set
        return list(set(videoIDs))


    def writeURLs(self, urls: list):
        writeFile = open("channelVideoURLs/"+self.channelID+".txt", 'a', encoding="utf-8")
        for url in urls:
            print(url, file = writeFile)
        writeFile.close()


    def downloadChatlogs(self, limit: int = None):
        if not os.path.exists("rawChatData/"+self.channelID):
            dir = pathlib.Path("rawChatData/"+self.channelID)
            dir.mkdir(parents=True, exist_ok=True)
        print("Starting chatlog downloads:")
        progressIntoList = 0
        numCompleted = 0
        for ID in self.videoIDs:
            progressIntoList += 1
            # attempts to retrieve a chatlog but does not increment completed if skipped
            if self.retrieveSingleStreamLivechat(ID):
                percent_done = round((progressIntoList / len(self.videoIDs)) * 100, 2)
                current_runtime = str(datetime.datetime.now() - self.startuptime)
                print(f"{ID} download complete, {percent_done}% complete. Current runtime: {current_runtime}")
                numCompleted += 1
            if limit != None and numCompleted >= limit: 
                break
        print(str(numCompleted) + " downloads completed.")


    # returns true if a download was completed otherwise false
    def retrieveSingleStreamLivechat(self, videoID: str) -> None: # creates txt file in rawchatdata
        # tries not to recollect already collected data

        incomplete_path = "rawChatData/"+self.channelID+"/"+"[incomplete]"+str(videoID)+".txt"
        complete_path = "rawChatData/"+self.channelID+"/"+str(videoID)+".txt"

        if os.path.exists(complete_path):
            return False
        if os.path.exists(incomplete_path):
            os.remove(incomplete_path)
        url = 'https://www.youtube.com/watch?v=' + videoID
        try:
            chat = ChatDownloader().get_chat(url)
            writeFile = open(incomplete_path, 'a', encoding="utf-8")
            for message in chat:
                print(chat.format(message), file = writeFile)
        except Exception as err:
            self.logDownloadError(videoID, err)
            return False
        writeFile.close()
        os.rename(incomplete_path, complete_path)
        return True
    
    def logDownloadError(self, videoID, error):
        errorFile = open("errorlogs/"+self.startuptimeAsWinCompliantStr + " ("+self.channelID+")" + ".txt", 'a', encoding="utf-8")
        print(f"error on {videoID} | {error}",file = errorFile)
        errorFile.close()





if __name__ == '__main__':

    print("This file is not meant to be run by users.\nDid you mean to open run.py ?")
    input()