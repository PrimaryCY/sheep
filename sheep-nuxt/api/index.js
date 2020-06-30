import common_crud from './common-crud'
/*
首页
 */
export const api_index=common_crud('/v1/web/index/')
/*
登录相关
 */
export const api_login=common_crud('/v1/web/login/')

/*
用户修改相关
 */
export const api_user=common_crud('/v1/web/user/')

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
* 上传文件接口
* post请求:{file:文件对象}
* 响应:{'code':2000,'msg':'ok',url:文件存储后的url}
* */
export const api_upload=common_crud('/v1/upload/')

