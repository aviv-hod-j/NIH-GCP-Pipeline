from pydantic import BaseSettings
from datetime import date


class MetadataPullerSettings(BaseSettings):
    base_url: str = "https://www.cancer.gov/"
    uri_types_identifier: str = "types/"
    cancer_type: str = "lung/"
    uri_articles: str = "research/articles/"
    bucket_name: str = 'data-nih-source'
    dir: str = 'raw/articles/metadata/'
    filename_prefix: str = "NIH-metadata-"
    load_dt: str = str(date.today())

    @property
    def full_url(self):
        return self.base_url + self.uri_types_identifier + self.cancer_type + self.uri_articles
