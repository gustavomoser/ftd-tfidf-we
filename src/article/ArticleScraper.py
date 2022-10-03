from json import dumps
from os import makedirs, path

import scrapy


class ArticleScraper(scrapy.Spider):
    name = "naturespider"

    articles_url = []

    with open(
        path.join(path.dirname(__file__), "..", "..", "assets", "articles.txt"), "r"
    ) as file:
        lines = file.readlines()
        for line in lines:
            articles_url.append(line)

    start_urls = articles_url
    used_sections = [
        "Abstract",
        "Main",
        "Results",
        "Discussion",
        "Methods",
        "Conclusions",
    ]

    def parse(self, response):
        # extract title and create filename
        title = response.css(".c-article-title::text").get()
        filename = f'article-{title.lower().replace(" ", "-")}.json'

        # extract authors
        authors = response.xpath('//a[@data-test="author-name"]/text()').getall()

        # extract body sections
        sections = self.extract_sections(
            response.xpath('//div[@class="c-article-section"]').getall()
        )

        # write file
        self.write_file(
            filename=filename,
            json=self.create_json(
                {"title": title, "authors": authors, "sections": sections}
            ),
        )

        self.log(f"{filename} saved!")

    def extract_sections(self, sections):
        extracted = []
        for s in sections:
            sec = scrapy.Selector(text=s)
            title = sec.xpath(
                '//h2[contains(@class, "c-article-section__title")]/text()'
            ).get()
            if title in self.used_sections:
                content = self.clean_section_content(
                    sec.xpath('//div[@class="c-article-section__content"]').get()
                )
                extracted.append({"section": title, "content": content})
        return extracted

    def clean_section_content(self, content):
        sec = scrapy.Selector(text=content)
        contents = ",".join(sec.xpath("//p/text()").getall())
        return contents

    def create_json(self, object):
        # create object
        return dumps(object)

    def write_file(self, filename, json):
        # create path to articles folder
        dir = path.join(path.dirname(__file__), "..", "..", "assets/articles")
        filepath = path.join(dir, filename)

        if not path.isdir(dir):
            makedirs(dir, exist_ok=True)

        f = open(filepath, "w")
        f.write(json)
        f.close()
