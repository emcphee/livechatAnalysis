import os
import re
IGNORE_FILES = ["errors.txt"]

class livechatDataAnalysis:
    def __init__(self, _channelID: str):
        self.channelID = _channelID
        files = os.listdir("rawChatData/"+self.channelID)
        for file in IGNORE_FILES:
            files.remove(file)
        self.chatlogPaths = files

    def loadChatlog(self, fileName: str) -> list:
        readFile = open("rawChatData/"+self.channelID+"/"+fileName, encoding = "UTF-8")
        messages = readFile.readlines()
        readFile.close()
        return messages

    # 2-22 5043826
    def totalNumLines(self):
        totalLines = 0
        for filepath in self.chatlogPaths:
            chatLog = self.loadChatlog(filepath)
            totalLines += len(chatLog)
        return totalLines
    # 2-22 976.816 hours 
    # 2-22 1.435 messages per second
    def getTotalStreamTime(self):
        time_in_seconds = 0
        for filepath in self.chatlogPaths:
            chatLog = self.loadChatlog(filepath)
            last_message = chatLog[-1]
            # cuts out timestamp from last message
            length_of_stream = last_message[:last_message.index("|") - 1]
            time_list = length_of_stream.split(':')
            if len(time_list) == 2:
                #minutes : seconds
                streamTime = int(time_list[0])* 60 + int(time_list[1])
            else:
                #hours : minutes : seconds
                streamTime = int(time_list[0])* 60 * 60 + int(time_list[1])* 60 + int(time_list[1])
            time_in_seconds += streamTime
        time_in_hours = time_in_seconds / (60**2)
        return time_in_hours
    
    
    def findEmoteUsage(self, emote_list):
        emote_usage_table = [0 for x in range(len(emote_list))]
        for filepath in self.chatlogPaths:
            chatLog = self.loadChatlog(filepath)
            for message in chatLog:
                for emote_index in range(len(emote_list)):
                    emote_usage_table[emote_index] += message.count(emote_list[emote_index])
        return emote_usage_table
    
    def findEmoteUsageLIMIT1PERMESSAGE(self, emote_list):
        emote_usage_table = [0 for x in range(len(emote_list))]
        for filepath in self.chatlogPaths:
            chatLog = self.loadChatlog(filepath)
            for message in chatLog:
                for emote_index in range(len(emote_list)):
                    emote_usage_table[emote_index] += int(emote_list[emote_index] in message)
        return emote_usage_table

if __name__ == "__main__":

    print("This file is not meant to be run by users.\nDid you mean to open run.py ?")
    input()
    """
    emote_list = [':_EliraELIKZ:', ':_EliraPenlight:', ':_EliraPIKW:', ':_EliraSmrik:', ':_EliraBlush:', ':_EliraBOOBA:', ':_EliraBanana1:', ':_EliraBanana2:', ':_EliraPog:', ':_EliraPauseChamp:', ':_EliraBonk:', ':_EliraOtamatone:', ':_EliraSweat:', ':_EliraThink:', ':_EliraSwipe:', ':_EliraAngy:', ':_EliraSheesh1:', ':_EliraSheesh2:', ':_EliraFlushed:', ':_EliraBELIEVE:', ':_EliraPien:', ':_EliraHeart:', ':_EliraComfy:', ':_EliraEye:', ':_EliraWingL:', ':_EliraWingR:', ':_EliraFRespect:', ':_EliraPPower:']
    v = livechatDataAnalysis("UCIeSUTOTkF9Hs7q3SGcO-Ow")
    emote_and_usage = list(zip(emote_list, v.findEmoteUsage(emote_list)))
    emote_and_usage.sort(key = lambda x: x[1], reverse = True)
    total_emotes = sum([x[1] for x in emote_and_usage])
    for name,count in emote_and_usage:
        print(f'{name}{" "*(20-len(name))}{count}{" "*(12 - len(str(count)))}{round(count*100/total_emotes, 2)}%')
    """