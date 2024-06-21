import os
import sys
sys.dont_write_bytecode = True
import requests
from tqdm import tqdm
from typing import Optional
import random
from bs4 import BeautifulSoup
from crawl.create_epub import EpubCreator

class NovelScrapper:
    user_agents_list = [
            'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        ]
    GREEN = "\033[92m"
    RESET = "\033[0m"

    def findCover(self,url : str) -> str:
        response = requests.get(url, headers={'User-Agent': random.choice(self.user_agents_list)})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            image = soup.find("img",class_ = "img-thumbnail pull-left visible-xs")
            if image:
                return image["src"]

    def downloadAndSave(self, url : str) -> None:
        response = requests.get(url, headers={'User-Agent': random.choice(self.user_agents_list)})
        if response.status_code == 200:
            with open("crawl/image.jpg", "wb") as file:
                file.write(response.content)
        else :
            print("Error")

    def bookT(self, url : str) -> str:
        response = requests.get(
                                url = url,
                                headers = {'User-Agent': random.choice(self.user_agents_list)}
                    )
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            a = soup.find(class_ = "book-info")
            if a:
                return a.find("h1").get_text()


    def find_urls(self, url : str ) -> dict:
        response = requests.get(url, headers={'User-Agent': random.choice(self.user_agents_list)})
        if response.status_code == 200:
            soup = BeautifulSoup(
                            response.text, "html.parser"
                    )
            a = soup.find(
                        id = "morelist"
                    )
            alldata = []
            if a:
                newData = a.find_all(
                                "a", href = True
                    )
                for link in newData:
                    alldata.append(link['href'])
                return alldata
            

    def find_chapters(self,
                            Link : str
                    ) -> str:
        chapter = {}
        url2 = "https://www.novelhall.com/"+ str(Link)
        response = requests.get(
                                url = url2, 
                                headers = { "User-Agent" : random.choice(self.user_agents_list)}
                    )
        soup = BeautifulSoup(response.text, "html.parser")
        f = soup.find(id = 'htmlContent')
        hea = soup.find(class_ = "single-header")
        if hea:
            n = hea.find("h1")
            chapter["title"] = n.get_text()
        if f :
            text = f.get_text(separator="\n")
            chapter["content"] = text
        return chapter


    def scrapper(self, 
                url : str ,
                AuthorName : Optional[str] = "01.8920.7",
                start : int = 1,
                end : int = 10
            ) -> None:

        data = self.find_urls(url)
        
        if end > len(data):
            print(f"There are only {len(data)} chapter in the novel")
            exit()
        coverLink = self.findCover(url)
        self.downloadAndSave(str(coverLink))
        
        chapterNames = []
        for i in tqdm(range(start, end), desc = self.GREEN + "Processing Chapters" + self.RESET ,colour= "green"):
            final_text = self.find_chapters(data[i])
            chapterNames.append(final_text["title"])
            with open(f"crawl/allchapters/input{i}.txt", "w", encoding='utf-8') as file:
                file.write(final_text["content"])

        name = self.bookT(url)
        epub_creator = EpubCreator(title = name, author=AuthorName)
        epub_creator.set_cover_image('crawl/image.jpg')

        text_files = os.listdir("crawl/allchapters")
        for x in range(len(text_files)):
            chapter_title = f'{chapterNames[x]}'
            pathToFile = "crawl/allchapters/" + text_files[x]
            epub_creator.add_chapter_from_file(pathToFile , chapter_title)
            os.remove(pathToFile)

        style = '''body { font-family: Arial, sans-serif; }'''
        epub_creator.add_css(style)
        f = name.split(" ")
        newName = "_".join(f)
        output_path = f'{newName[:15]}.epub'
        epub_creator.create_epub(output_path)
        os.remove("crawl/image.jpg")
        os.remove("crawl/cover.jpg")