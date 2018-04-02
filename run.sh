#!/usr/bin/env bash

source env.sh
scrapy crawl git_spider -o git-items.json
