import livechatDownloader
import livechatDataAnalysis


def print_help():
    print("help message stuff here")



def main():
    exits = ['q', 'quit', 'exit', ':q']
    while True:
        userInput = input()
        if userInput in exits:
            break
        if userInput == "start":
            downloader = livechatDownloader.youtubeLivechatDownloader("UCIeSUTOTkF9Hs7q3SGcO-Ow")
            downloader.downloadChatlogs(limit = None)
        if userInput == "help":
            print_help()

if __name__ == "__main__":
    main()