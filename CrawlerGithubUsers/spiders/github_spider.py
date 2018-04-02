import json
from scrapy.contrib.spiders import CrawlSpider
from CrawlerGithubUsers.items import GitUsersItem
import os


def generate_url(page_index):
    return "https://api.github.com/search/users" \
           "?q=+location:%22Wu%20Han%22&page=" \
           + page_index + \
           "&per_page=100"


class GitHubSpider(CrawlSpider):
    http_user = os.environ['USER_NAME']
    http_pass = os.environ['USER_TOKEN']
    name = "git_spider"
    allowed_domains = ["github.com"]
    start_urls = [
        generate_url(1),
        "https://api.github.com/search/users?"
        "q=+location:%22WuHan%22&page=1&per_page=100"
    ]

    def parse(self, response):
        for users in json.loads(response.body)["items"]:
            item = GitUsersItem()
            item['username'] = users["login"]
            # item['name'] = users["name"]
            item['link'] = users["html_url"]
            # item['email'] = users["email"]
            item['followers'] = users["followers_url"]
            yield item
