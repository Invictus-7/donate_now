# Объекты, импортированные в __init__.py, становятся доступными уже из самого пакета,
# в котором лежит __init__.py, а не из какого-либо файла.
from .user import router as user_router  # noqa
from .charity_project import router as charity_project_router  # noqa
from .donation import router as donation_router  # noqa
