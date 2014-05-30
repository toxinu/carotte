# -*- coding: utf-8 -*-
__version__ = "0.1.0"

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

registrar = {}

from .task import Task
from .client import Client
from .worker import Worker
from .decorator import task
