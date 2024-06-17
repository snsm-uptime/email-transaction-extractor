import os
from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

import pandas as pd

from . import OutputFormat, Transaction
from ..utils import create_reports_folder, get_timestamp_name

T = TypeVar('T')


class Report(ABC, Generic[T]):
    def __init__(self, name: str, format: OutputFormat):
        self.name = name
        self.format = format
        self.__content = self.get_content()

    @property
    def content(self) -> List[T]:
        return self.__content

    @abstractmethod
    def get_content(self) -> List[T]:
        pass

    @abstractmethod
    def prepare_content(self, content: List[T]) -> pd.DataFrame:
        pass

    def build(self, data: pd.DataFrame):
        folder = create_reports_folder(self.name)
        file_name = get_timestamp_name(self.name, self.format.value)
        file_path = os.path.join(folder, file_name)
        if self.format == OutputFormat.JSON:
            data.to_json(file_path)
        elif self.format == OutputFormat.CSV:
            data.to_csv(file_path)

    def __call__(self):
        df = self.prepare_content(self.__content)
        self.build(df)
