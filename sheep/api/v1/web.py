# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/12/13 13:54
from django.conf.urls import url,include

from utils.routes import CustomRouter
from apps.user.views import UserViewSet, LoginViewSet
from apps.post.views import PostCategoryViewSet, UserPostViewSet, AllPostViewSet, UserReplyViewSet, \
    PostReplyViewSet
from apps.operate.views import UserCollectCategoryViewSet, CollectCategoryViewSet, CollectViewSet, PraiseViewSet, FocusViewSet

router = CustomRouter()
# 用户crud
router.register('user', UserViewSet, base_name='user')
# 用户登录退出
router.register('login', LoginViewSet, base_name='login')
# 帖子分类crud
router.register('post_category', PostCategoryViewSet, base_name='post_category')
# 所有帖子
router.register('all_post', AllPostViewSet, base_name='all_post')
# 个人帖子crud
router.register('user_post', UserPostViewSet, base_name='user_post')
# 个人回复展示
router.register('user_reply', UserReplyViewSet, base_name='user_reply')
# 个人收藏分类
router.register('user_collect_category', UserCollectCategoryViewSet, base_name='user_collect_category')
# 个人收藏帖子
router.register('user_collect', CollectViewSet, base_name='user_collect')
# 个人点赞
router.register('user_praise', PraiseViewSet, base_name='user_praise')
# 个人关注
router.register('user_focus', FocusViewSet, base_name='user_focus')

# 所有帖子回复
router.register('post_reply', PostReplyViewSet, base_name='post_reply')
# 所有用户收藏分类
router.register('collect_category', CollectCategoryViewSet, base_name='collect_category')
# 所有用户基本信息


urlpatterns = [
    url(r'', include(router.urls)),
]
