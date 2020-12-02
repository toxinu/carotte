# -*- coding: utf-8 -*-
__version__ = "0.2.2"

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .task import Task
from .client import Client
from .worker import Worker
from .app import Carotte
