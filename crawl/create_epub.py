import sys
sys.dont_write_bytecode = True
from ebooklib import epub
from PIL import Image

class EpubCreator:
    def __init__(self, title, author, language='en'):
        self.book = epub.EpubBook()
        self.book.set_title(title)
        self.book.set_language(language)
        self.book.add_author(author)

    def set_cover_image(self, cover_image_path):
        cover_image = Image.open(cover_image_path)
        cover_image = cover_image.resize((600, 800))  # image resizing
        cover_image.save('crawl/cover.jpg', 'JPEG')
        self.book.set_cover('crawl/cover.jpg', open('crawl/cover.jpg', 'rb').read())

    def add_chapter_from_file(self, text_file, chapter_title):
        with open(text_file, 'r', encoding='utf-8') as file:
            paragraphs = file.readlines()

        # Create valid HTML content preserving paragraphs
        content = ''.join(f'<p>{para.strip()}</p>' for para in paragraphs if para.strip())

        chapter = epub.EpubHtml(title=chapter_title, file_name=f'{chapter_title.replace(" ", "_").lower()}.xhtml', lang='en')
        chapter.content = f'''<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{chapter_title}</title>
</head>
<body>
    <h1>{chapter_title}</h1>
    {content}
</body>
</html>'''
        self.book.add_item(chapter)
        self.book.toc.append(chapter)

    def add_css(self, style):
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
        self.book.add_item(nav_css)
        self.book.spine = ['nav'] + [chapter for chapter in self.book.toc]

    def create_epub(self, output_path):
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        epub.write_epub(output_path, self.book, {})
