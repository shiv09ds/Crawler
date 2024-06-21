import os
import sys
import platform
sys.dont_write_bytecode = True
from crawl import NovelScrapper

def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else :
        os.system("clear")
def clear_dict():
    text_files = os.listdir("crawl/allchapters/")
    if len(text_files) > 0:
        for file in text_files:
            os.remove("crawl/allchapters/"+file)

def mainKL():
    sc = NovelScrapper()
    """            <------ example link ------>
    https://www.novelhall.com/333Eternal-Sacred-King2022-11108/
    """
    url = input("Enter the novel url \n(link must be from novelhall.com) : ")
    chapters = sc.find_urls(url)
    line = "\nUse only for (10 - 15) chapters at once"
    print(line)
    print("Total chapters available : " , len(chapters))
    start = int(input("\nFrom which chapter you want to start? : "))
    end = int(input("On which chapter you want to end? : "))
    if start < 0 or end < 0:
        clear(); print("Invalid input")
        exit()
    if end - start > 15:
        clear(); print(line)
        exit()
    sc.scrapper(url=url, start = start - 1, end = end)

if __name__ == "__main__" :
    clear_dict()
    try:
        mainKL(); clear()
        print("Epub created successfully")
    except:
        print("An error occured")