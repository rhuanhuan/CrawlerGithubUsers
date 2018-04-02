import json
from scrapy.contrib.spiders import CrawlSpider
from CrawlerGithubUsers.items import GitUsersItem
import os
import requests


def get_users_list_url(page_index):
    return "https://api.github.com/search/users" \
           "?q=+location:%22Wu%20Han%22&page=" \
           + str(page_index) + \
           "&per_page=100"


def get_user_detail_url(username):
    return "https://api.github.com/users/" + username


class GitHubSpider(CrawlSpider):
    http_user = os.environ['USER_NAME']
    http_pass = os.environ['USER_TOKEN']
    name = "git_spider"
    allowed_domains = ["github.com"]
    start_urls = [
        get_users_list_url(1),
        "https://api.github.com/search/users?"
        "q=+location:%22WuHan%22&page=1&per_page=100"
    ]

    def parse(self, response):
        json_body = json.loads(response.body)
        for users in json_body["items"]:
            item = GitUsersItem()
            item['username'] = users["login"]
            item['link'] = users["html_url"]

            detail_response = requests.get(get_user_detail_url(item['username']))
            user_detail = json.loads(detail_response.content)
            item['name'] = user_detail['name']
            item['email'] = user_detail["email"]
            item['company'] = user_detail["company"]
            item['hireable'] = user_detail["hireable"]
            item['followers'] = user_detail["followers"]
            item['created_at'] = user_detail["created_at"]
            item['product'] = user_detail["public_repos"]
            yield item
