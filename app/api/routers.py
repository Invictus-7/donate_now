from fastapi import APIRouter

from app.api.endpoints import user_router, charity_project_router, donation_router

# принимает роутеры из всех пакетов и затем уходит в файл main.py,
# где подключается к объекту приложения - app.include_router(main_router)
main_router = APIRouter()

# Подключаем роутер пользователя к главном роутеру
main_router.include_router(user_router)

# Подключаем роутер благотворительного проекта к главном роутеру
main_router.include_router(charity_project_router, prefix='/charity_project',
                           tags=['Charity Project'])

# Подключаем роутер пожертвования к главном роутеру
main_router.include_router(donation_router, prefix='/donation', tags=['Donation'])
