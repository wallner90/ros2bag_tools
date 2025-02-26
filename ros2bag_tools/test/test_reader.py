# Copyright 2022 AIT Austrian Institute of Technology GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import NamedTuple
from datetime import timedelta
from rosbag2_py import Info
from ros2bag_tools.reader import FilteredReader
from ros2bag_tools.filter import FilterExtension
from ros2bag_tools.filter.cut import CutFilter
import pytest


class CutArgs(NamedTuple):
    start: timedelta
    end: timedelta
    duration: timedelta


def test_reader_cut_filtered():
    bag_path = 'test/test.bag'
    filter = CutFilter()
    info = Info()
    filter.set_args([info.read_metadata(bag_path, '')],
                    CutArgs(None, timedelta(microseconds=1), None))
    reader = FilteredReader([bag_path], filter)
    it = iter(reader)
    assert('/data' == next(it)[0])
    with pytest.raises(StopIteration):
        next(it)


def test_reader_unfiltered():
    bag_path = 'test/test.bag'
    reader = FilteredReader([bag_path], FilterExtension())
    it = iter(reader)
    assert('/data' == next(it)[0])
    assert('/data' == next(it)[0])
    with pytest.raises(StopIteration):
        next(it)
