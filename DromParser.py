import json
import requests

from concurrent.futures.thread import ThreadPoolExecutor
from bs4 import BeautifulSoup


class DromParser:
    def __init__(self, settings):
        """
        :type settings: Settings.Settings
        """
        self.settings = settings

    def __get_pages(self) -> list[str]:
        pages = []
        for i in range(1, self.settings.page + 1):
            pages.append(f"https://auto.drom.ru/used/all/page{i}/?minyear={self.settings.production_from}&maxyear={self.settings.production_to}/")
        return pages

    def __scrape_links(self, pages: list[str]) -> list[str]:
        links = []

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(requests.get, page) for page in pages]
            for future in futures:
                response = future.result()
                html = response.text
                soup = BeautifulSoup(html, 'lxml')
                titles = soup.find_all(attrs={"data-ftid": "bull_title"})
                for title in titles:
                    links.append(title.attrs.get("href"))

        return links

    def __retrieve_primary_date(self, link: str) -> dict[str, str]:
        result = {}
        response = requests.get(link)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        script = soup.find('script', attrs={"data-drom-module": "bull-page"}).text
        data = json.loads(script)
        result["primary_date"] = data["report"]["fields"][2]["data"][0].split(' ')[1]
        result["title"] = data["pageMeta"]["titleBull"]
        result["link"] = link
        return result

    def __validate_links(self, links: list[str]) -> dict[str, str]:
        result = {}
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.__retrieve_primary_date, link) for link in links]
            for future in futures:
                try:
                    meta = future.result()
                    pdate = int(meta["primary_date"])
                except (TypeError, ValueError, IndexError) as _:
                    continue

                if pdate < self.settings.primary_from or pdate > self.settings.primary_to:
                    continue

                result[meta["title"]] = meta["link"]
        return result

    def parse(self) -> dict[str, str]:
        pages = self.__get_pages()
        links = self.__scrape_links(pages)
        valid_links = self.__validate_links(links)
        return valid_links