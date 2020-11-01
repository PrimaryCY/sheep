import common_crud from './common-crud'
/*
搜索
 */
export const api_s=common_crud('/v1/s/')
/*
轮播图
 */
export const api_banner=common_crud('/v1/web/banner/')
/*
热门
*/
export const api_hot=common_crud('/v1/web/hot/')
/*
所有文章
 */
export const api_post=common_crud('/v1/web/post/')
/*
详情页分类推荐
*/
export const api_category_post=common_crud('/v1/web/category_post')
/*
详情页相关分类
*/
export const api_correlation_category=common_crud('/v1/web/correlation_category')
/*
详情页作者推荐
*/
export const api_author_post=common_crud('/v1/web/author_post')
/*
登录相关
 */
export const api_login=common_crud('/v1/web/login/')
/*
第三方登录app
 */
export const api_o_applications=common_crud('v1/o/applications/')
/*
第三方code登录
 */
export const api_o_token=common_crud('v1/o/token/')
/*
第三方绑定用户登录
 */
export const api_o_register=common_crud('v1/o/register/')
/*
第三方用户信息
 */
export const api_o_user_oauth=common_crud('v1/o/user_oauth/')

/*
用户修改相关
 */
export const api_user=common_crud('/v1/web/user/')
/*
用户修改密码
 */
export const api_pwd=common_crud('v1/web/pwd/')
/*
用户关注
 */
export const api_user_focus=common_crud('v1/web/user_focus/')
/*
获取所有帖子类别
 */
export const api_post_category=common_crud('/v1/web/post_category/')
/*
个人创建帖子,个人所有帖子
 */
export const api_user_post=common_crud('/v1/web/user_post/')
/*
获取反馈类别
 */
export const api_feedback_category=common_crud('/v1/feedback_category/')
/*
提交反馈相关
 */
export const api_feedback=common_crud('/v1/feedback/')

/*
获取远端公共配置
 */
export const api_option=common_crud('/v1/option/')
/*
收藏分类
*/
export const api_user_collect_category=common_crud('/v1/web/user_collect_category')
/*
用户收藏
 */
export const api_user_collect=common_crud('/v1/web/user_collect')
/*
用户点赞或踩
 */
export const api_user_praise=common_crud('v1/web/user_praise');
/*
用户历史浏览记录
 */
export const api_user_history=common_crud('v1/web/user_history');
/*
所有帖子回复
 */
export const api_post_reply=common_crud('v1/web/post_reply')
/*
用户个人回复
 */
export const api_user_reply=common_crud('v1/web/user_reply')
/*
用户动态
 */
export const api_dynamic=common_crud('v1/web/dynamic/')
/*
关于我们
 */
export const api_about=common_crud('v1/web/about')

/*
* 上传文件接口
* post请求:{file:文件对象}
* 响应:{'code':2000,'msg':'ok',url:文件存储后的url}
* */
export const api_upload=common_crud('/v1/upload/')

