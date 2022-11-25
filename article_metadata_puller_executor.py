import requests
from bs4 import BeautifulSoup
from article_metadata_puller.article_metadata_puller_config import MetadataPullerSettings
from article_metadata_puller.article_metadata_puller_exceptions import HTMLPullerException, ArticleDataExtractorException
from nih_logger import logger
from hashlib import md5
from uuid import uuid4
from cloud_storage.cloud_storage_utils import write_to_cloud_storage, read_from_cloud_storage
import json
from cloud_storage.cloud_storage_exceptions import CloudStorageConnectionException
from datetime import date


class NIHArticleMetadataPuller:

    def __init__(self, settings: MetadataPullerSettings):
        self.settings = settings
        self.logger = logger
        self._html_content = None
        self.data = ""

    def get_html(self):
        res = requests.get(self.settings.full_url)
        if res.ok:
            self._html_content = BeautifulSoup(res.content, 'lxml')
            self.logger.info('Successfully got html from NIH')
        else:
            self.logger.error("request failed: failed retrieve html of articles")
            raise HTMLPullerException(
                "request failed: failed retrieve html of articles, status code: %s", res.status_code)

    def get_articles_data(self):
        articles_data = list()
        if self._html_content:
            try:
                page_body = self._html_content.find('div', {'id': 'cgvBody'})
                article_ul = page_body.find('ul')
                article_elems_list = article_ul.find_all('li')
                for article_elem in article_elems_list:
                    article_data = {'title': self._get_title(article_elem),
                                    'link': self._get_link(article_elem),
                                    'gist': self._get_gist(article_elem),
                                    'date': self._get_date(article_elem)}
                    article_data['unique_key'] = md5(article_data['link'].encode('UTF-8')).hexdigest()
                    articles_data.append(article_data)
                self.logger.info('Successfully got article data from NIH')
            except Exception:
                self.logger.exception("Failed to get articles data from nih")
                raise ArticleDataExtractorException
        else:
            self.logger.error("First get the html, then links baby")
        self.data = json.dumps(articles_data)

    def _get_link(self, article_elem):
        link = self.settings.base_url + article_elem.find('a').attrs['href']
        return link

    @staticmethod
    def _get_gist(article_elem):
        gist = article_elem.find('p').text
        return gist

    @staticmethod
    def _get_title(article_elem):
        title = article_elem.find('a').text
        return title

    @staticmethod
    def _get_date(article_elem):
        date = article_elem.find('div', {'class': 'date'}).find('time').attrs['datetime']
        return date

    def execute_upload(self):
        file_name = f'{self.settings.dir}load_dt={date.today()}/{self.settings.filename_prefix}{uuid4().hex}.json'
        try:
            if self.data:
                write_to_cloud_storage(self.settings.bucket_name, self.data, file_name)
                self.logger.info("Uploaded data to Google Cloud Storage successfully, file name: %s", file_name)
            else:
                self.logger.error("No data to write to Google Cloud Storage")
        except Exception:
            self.logger.exception("Failed to upload file to Google Cloud Storage")
            raise CloudStorageConnectionException

    def execute_download(self):
        try:
            data_blob_lst = read_from_cloud_storage(self.settings.bucket_name,
                                                    f'{self.settings.dir}load_dt={self.settings.load_dt}/')
            if data_blob_lst:
                self.logger.info("Read successfully the data from Google Cloud Storage, directory: %s", self.settings.dir)
            else:
                self.logger.error("No data to read from Google Cloud Storage")
        except Exception:
            self.logger.exception("Failed to read data from Google Cloud Storage")
            raise CloudStorageConnectionException
        return data_blob_lst










