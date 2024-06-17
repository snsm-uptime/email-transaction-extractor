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
        self._content = self.get_content()
        self.logger = logger

    @property
    def content(self) -> List[RawType]:
        return self._content

    @abstractmethod
    def get_content(self) -> List[RawType]:
        pass

    @abstractmethod
    def prepare_content(self, content: List[RawType]) -> List[TargetType]:
        pass

    def build(self, data: pd.DataFrame):
        folder = create_reports_folder(self.name)
        file_name = get_timestamp_name(self.name, self.format.value)
        file_path = os.path.join(folder, file_name)
        if self.format == OutputFormat.JSON:
            data.to_json(file_path)
        elif self.format == OutputFormat.CSV:
            data.to_csv(file_path, index=False)

    def __call__(self):
        df = pd.DataFrame([
            item.__dict__ for item in self.prepare_content(self.content)
        ])
        df = df.drop('body', axis=1)
        self.logger.info(f'Removing body column from DataFrame')
        self.build(df)
