from logging import Logger
import os
from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

import pandas as pd

from . import OutputFormat, Transaction
from ..utils import create_reports_folder, get_timestamp_name

TargetType = TypeVar('TargetType')
RawType = TypeVar('RawType')


class Report(ABC, Generic[RawType, TargetType]):
    def __init__(self, name: str, format: OutputFormat, logger: Logger):
        self.name = name
        self.format = format
        self.__content = []
        self.logger = logger

    def get_content(self) -> List[RawType]:
        """
        Returns the list of raw data in memory (only calls fetch_content once)
        """
        if self.__content:
            return self.__content
        self.__content = self.fetch_content()
        return self.__content

    @abstractmethod
    def fetch_content(self) -> List[RawType]:
        """
        Gets the list of raw data from the source. This is called once the first time you use self.content to avoid extra calls
        """
        pass

    @abstractmethod
    def prepare_content(self, content: List[RawType]) -> List[TargetType]:
        """
        This is where the raw data is processed into the target type
        """
        pass

    def write_data_to_file(self, data: pd.DataFrame):
        folder = create_reports_folder(self.name)
        file_name = get_timestamp_name(self.name, self.format.value)
        file_path = os.path.join(folder, file_name)
        if self.format == OutputFormat.JSON:
            data.to_json(file_path)
        elif self.format == OutputFormat.CSV:
            data.to_csv(file_path, index=False)

    def get_data(self) -> pd.DataFrame:
        processed_content = self.prepare_content(self.get_content())
        return pd.DataFrame([
            item.__dict__ for item in processed_content
        ])

    def persist_data(self):
        df = self.get_dataframe()
        df.drop('body', axis=1, inplace=True)
        df.sort_values(by='date', inplace=True, ascending=False)
        self.logger.info(f'Removing body column from DataFrame')
        self.write_data_to_file(df)
