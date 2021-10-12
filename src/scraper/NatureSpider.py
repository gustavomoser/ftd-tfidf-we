import scrapy
from json import dumps
from os import path, makedirs

class NatureSpider(scrapy.Spider):
  name = 'naturespider'
  start_urls = ['https://www.nature.com/articles/s41591-020-0843-2']

  def extract_sections(self, sections):
    extracted = []
    for s in sections:
      sec = scrapy.Selector(text=s)
      title = sec.xpath('//h2[contains(@class, "c-article-section__title")]/text()').get()
      content = self.clean_section_content(
        content=sec.xpath('//div[@class="c-article-section__content"]').get()
      )
      extracted.append({ "section": title, "content": content })
    return extracted
  
  def clean_section_content(sections, content):
    # TODO clean non used html content
    return content

  def create_json(self, object):
    # create object
    return dumps(object)

  def write_file(self, filename, json):
    dir = path.join(path.dirname(__file__), '..', '..', 'files/articles')
    filepath = path.join(dir, filename)

    if not path.isdir(dir):
      makedirs(dir, exist_ok=True)

    f = open(filepath, "w")
    f.write(json)
    f.close()

  def parse(self, response):
    # extract title
    title = response.css('.c-article-title::text').get()
    filename = f'article-{title.lower().replace(" ", "-")}.json'

    # extract authors
    authors = response.xpath('//a[@data-test="author-name"]/text()').getall()

    # extract body sections
    sections = self.extract_sections(response.xpath('//div[@class="c-article-section"]').getall())
  
    # write file
    self.write_file(
      filename=filename, 
      json=self.create_json({"title": title, "authors": authors, "sections": sections})
    )

    self.log(f'{filename} saved!')