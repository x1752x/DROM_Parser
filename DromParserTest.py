import json

from DromParser import DromParser
from Settings import Settings

class DromParserTest:
    def __init__(self):
        with open('config/settings.json', 'r') as file:
            settings_dict = json.load(file)
        settings = Settings(**settings_dict)
        self.parser = DromParser(settings)

    def __get_pages(self):
        return self.parser._DromParser__get_pages()

    def __scrape_links(self, pages):
        return self.parser._DromParser__scrape_links(pages)

    def __retrieve_primary_date(self):
        return self.parser._DromParser__retrieve_primary_date("https://auto.drom.ru/chulym/toyota/avensis/885192694.html")

    def run(self):
        pages = self.__get_pages()
        print(pages)
        links = self.__scrape_links(pages)
        print(links)
        pdate = self.__retrieve_primary_date()
        print(pdate)
        valid_links = self.parser._DromParser__validate_links(links)
        print(valid_links)

if __name__ == '__main__':
    DromParserTest().run()