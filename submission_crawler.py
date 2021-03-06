#!/usr/bin/env python
# -*- coding: utf-8 -*-

from catenae import Link, Electron, CircularOrderedSet
import random
import time
import crawler_helper as rch
import logging
from env import MAX_WAIT_SECONDS


class SubmissionCrawler(Link):
    def setup(self):
        self.spider_name = rch.get_spider_name('RSC')
        self.processed_ids = CircularOrderedSet(1000)
        self.wait_seconds = MAX_WAIT_SECONDS  # Max waiting seconds between loops

    def generator(self):
        while (True):
            for submission in rch.get_all_submissions_elements(self.spider_name, items_no=100):
                submission_id = rch.get_submission_id(submission)
                if submission_id in self.processed_ids:
                    continue
                self.processed_ids.add(submission_id)

                subreddit_id = rch.get_subreddit_id(submission, retrieve_user_if_not_subreddit=True)

                user_id = rch.get_user_id(submission)
                timestamp = rch.get_submission_timestamp(submission)
                title = rch.get_submission_title(submission)

                value = {
                    'submission_id': submission_id,
                    'subreddit_id': subreddit_id,
                    'user_id': user_id,
                    'timestamp': timestamp,
                    'title': title
                }
                electron = Electron(None, value, topic=self.output_topics[0])
                self.send(electron)

            time.sleep(random.uniform(0, self.wait_seconds))


if __name__ == "__main__":
    SubmissionCrawler().start()
