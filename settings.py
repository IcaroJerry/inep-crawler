import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

INEP_URL = "http://inep.gov.br/microdados"

REPOSITORY_URL = "https://github.com/IcaroJerry/inep-crawler"

OPEN_ISSUE_URL = REPOSITORY_URL + "/issues/new"

DATA_DIR = ROOT_DIR + "/storage"
