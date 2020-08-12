# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/12/13 13:54
from django.conf.urls import include
from django.urls import path

from utils.routes import CustomRouter
from apps.user.views import UserViewSet, LoginViewSet
from apps.post.views import PostCategoryViewSet, UserPostViewSet, UserReplyViewSet, \
    PostReplyViewSet, AllPostViewSet, CategoryPostViewSet, AuthorPostViewSet, CorrelationCategoryViewSet
from apps.operate.views import UserCollectCategoryViewSet, CollectCategoryViewSet, CollectViewSet, PraiseViewSet, FocusViewSet
from apps.index.views import BannerViewSet, HotViewSet

router = CustomRouter()
# 轮播图
router.register('banner', BannerViewSet, basename='index')
# 热门
router.register('hot', HotViewSet, basename='hot')
# 用户crud
router.register('user', UserViewSet, basename='user')
# 用户登录退出
router.register('login', LoginViewSet, basename='login')
# 帖子分类crud
router.register('post_category', PostCategoryViewSet, basename='post_category')
# 所有帖子
router.register('post', AllPostViewSet, basename='post')
# 作者相关推荐
router.register('author_post', AuthorPostViewSet, basename='author_post')
# 分类相关推荐
router.register('category_post', CategoryPostViewSet, basename='category_post')
# 同一级分类
router.register('correlation_category', CorrelationCategoryViewSet, basename='correlation_category')
# 个人帖子crud
router.register('user_post', UserPostViewSet, basename='user_post')
# 个人收藏分类
router.register('user_collect_category', UserCollectCategoryViewSet, basename='user_collect_category')
# 个人收藏帖子
router.register('user_collect', CollectViewSet, basename='user_collect')

# 个人回复展示
router.register('user_reply', UserReplyViewSet, basename='user_reply')
# 个人点赞
router.register('user_praise', PraiseViewSet, basename='user_praise')
# 个人关注
router.register('user_focus', FocusViewSet, basename='user_focus')

# 所有帖子回复
router.register('post_reply', PostReplyViewSet, basename='post_reply')
# 所有用户收藏分类
router.register('collect_category', CollectCategoryViewSet, basename='collect_category')
# 所有用户基本信息


urlpatterns = [
    path(r'', include(router.urls)),
]
