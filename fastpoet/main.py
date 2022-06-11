"""Приложение запуска app:main"""
from fastapi import FastAPI, Request
from sqladmin import Admin, ModelAdmin

from fastpoet.groups.routers import router as groups_router
from fastpoet.posts.routers import router as posts_router
from fastpoet.users.routers import (
    authentications_router,
    permissions_router,
    users_router
)
from fastpoet.users.authentication import middleware
from fastpoet.settings.database import engine
from fastpoet.users.models import User
from fastpoet.posts.models import Post
from fastpoet.groups.models import Group


def create_app():
    """Application Initialization"""
    app = FastAPI(middleware=middleware)
    app.include_router(posts_router)
    app.include_router(users_router.router)
    app.include_router(permissions_router.router)
    app.include_router(authentications_router.router)
    app.include_router(groups_router)
    return app


app = create_app()
admin = Admin(app, engine)


class AuthModelAdmin(ModelAdmin):
    def is_accessible(self, request: Request) -> bool:
        #  Проверяем токен (не сработает, тест)
        """return (
            (request.user.is_admin or request.user.is_superuser)
            if request.user.is_authenticated
            else False
        )"""
        return True

    def is_visible(self, request: Request) -> bool:
        #  Проверяем токен (не сработает, тест)
        """return (
            (request.user.is_admin or request.user.is_superuser)
            if request.user.is_authenticated
            else False
        )"""
        return True


class GroupAdmin(AuthModelAdmin, model=Group):
    """Admin group elements."""
    name = "Группа"
    name_plural = "Группы"
    column_list = [Group.id, Group.title, Group.slug, Group.description]


class PostAdmin(AuthModelAdmin, model=Post):
    """Admin posts elements."""
    name = "Пост"
    name_plural = "Посты"
    page_size = 10
    page_size_options = [25, 50, 100, 200]
    column_list = [
        Post.id,
        Post.title,
        Post.text,
        Post.author,
        Post.group,
    ]


class UserAdmin(AuthModelAdmin, model=User):
    """Admin user elements."""
    name = "Пользователь"
    name_plural = "Пользователи"
    page_size = 10
    page_size_options = [25, 50, 100, 200]
    column_list = [
        User.id,
        User.username,
        User.email,
        User.first_name,
        User.born_year,
        User.is_authenticated,
        User.is_admin,
        User.is_superuser,
        User.is_user
    ]


admin.register_model(UserAdmin)
admin.register_model(PostAdmin)
admin.register_model(GroupAdmin)
