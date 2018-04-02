import json

import scrapy
from scrapy.contrib.spiders import CrawlSpider
from CrawlerGithubUsers.items import GitUsersItem
import os
import requests
import dateutil.parser
import time

git_init_date = '2008-03-01T00:00:00Z'
crawler_ended_date = '2018-03-25T00:00:00Z'


def get_users_list_url(date):
    return "https://api.github.com/search/users" \
           "?q=+location:%22WuHan%22+created:>" + date + \
           "&page=1" \
           "&per_page=100&sort=joined&order=asc"


def get_user_detail_url(username):
    return "https://api.github.com/users/" + username


def get_timestamp(iso_time):
    return dateutil.parser.parse(iso_time)


class GitHubSpider(CrawlSpider):
    http_user = os.environ['USER_NAME']
    http_pass = os.environ['USER_TOKEN']
    name = "git_spider"
    allowed_domains = ["github.com"]
    start_urls = [get_users_list_url(git_init_date)]

    def parse(self, response):
        json_body = json.loads(response.body)
        last_created = git_init_date
        for users in json_body["items"]:
            item = GitUsersItem()
            item['username'] = users["login"]
            item['link'] = users["html_url"]

            detail_response = requests.get(
                url=get_user_detail_url(item['username']),
                auth=(self.http_user, self.http_pass)
            )
            time.sleep(2)
            user_detail = json.loads(detail_response.content)
            item['name'] = user_detail["name"]
            item['email'] = user_detail["email"]
            item['company'] = user_detail["company"]
            item['hireable'] = user_detail["hireable"]
            item['followers'] = user_detail["followers"]
            item['created_at'] = user_detail["created_at"]
            item['product'] = user_detail["public_repos"]
            if get_timestamp(last_created) < get_timestamp(item['created_at']):
                last_created = item['created_at']
            yield item
        if get_timestamp(last_created) < get_timestamp(crawler_ended_date):
            yield scrapy.Request(url=get_users_list_url(last_created),
                                 callback=self.parse)
