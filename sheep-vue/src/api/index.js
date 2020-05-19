import axios from './ajax'
import common_crud from './common-crud'

/*
登录
 */
export const post_login=(data)=>axios.post(`/v1/web/login/`,data)
/*
退出登录
 */
export const delete_login=()=>axios.delete('/v1/web/login/')

/*
注册
 */
export const post_user=(data)=>axios.post('/v1/web/user/',data)
/*
获取当前用户信息
 */
export const get_user=()=>axios.get('/v1/web/user/')
/*
修改用户资料
 */
export const patch_user=(data)=>axios.patch('/v1/web/user/',data)

/*
获取所有帖子类别
 */
export const get_post_category=()=>axios.get('/v1/web/post_category/')
/*
创建帖子
 */
export const create_user_post=(data)=>axios.post('/v1/web/user_post/',data)
/*
个人所有帖子
 */
export const user_post = common_crud('/v1/web/user_post/')


/*
获取远端公共配置
 */
export const get_option=()=>axios.get('/v1/option/')

/*
* 上传文件接口
* 请求:{file:文件对象}
* 响应:{'code':2000,'msg':'ok',url:文件存储后的url}
* */
export const upload=(data)=>axios.upload('/v1/upload/',data)

