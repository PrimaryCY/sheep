import axios from 'axios'
import VueCookies from 'vue-cookies'
import vue from '../main'

import settings from '../conf/settings'


let service=axios.create({
	baseURL:settings.SERVER_URL,
	timeout:9000,
	headers:{
		'content-type':'application/json'//转换为key=value的格式必须增加content-type
	},
})

service.interceptors.request.use(
	request => {
		if (VueCookies.get(settings.TOKEN_NAME)) {  // 判断是否存在token，如果存在的话，则每个http header都加上token
			request.headers.tk = VueCookies.get(settings.TOKEN_NAME);
		}
		return request;
	},
	err => {
		return Promise.reject(err);
	});

//http-响应拦截
service.interceptors.response.use(
	response => {
		console.log(response)
		switch(response.data.code) {
			case '4101':
				VueCookies.remove('tk')
				console.log('用户令牌失效!')
				// router.replace({
				//   path: '/login',
				//   query: {
				//     redirect: router.currentRoute.fullPath
				//   }
				// })
				break
		}
		return response.data;
	},
	error => {
		if(!error.response){
			vue.$message('网络连接错误,请检查网络!')
		}else {
			switch (error.response.status) {
				case 404:
					vue.$message('网络错误:'+error.response.status)
					break
				case 500:
					vue.$message('500 internal server error');
					break
			}
		}
		return Promise.reject(error)
	}
)


export default function(url){
	return {
		get: (param = {}) => {//get请求
			return new Promise((resolve,) => {
				service({
					method: 'get',
					url,
					params: param,
				}).then(res => {
					resolve(res)
				})
			})
		},
		post:(param)=>{//post请求
			return new Promise((resolve, ) => {
				service({
					method: 'post',
					url,
					data: param,
				}).then(res => {
					resolve(res)
				})
			})
		},
		patch:(param)=>{//patch请求
			return new Promise((resolve, ) => {
				service({
					method: 'patch',
					url,
					data: param,
				}).then(res => {
					resolve(res)
				})
			})
		},
		delete:(param) =>{//delete请求
			return new Promise((resolve, ) => {
				service({
					method: 'delete',
					url,
					data: param,
				}).then(res => {
					resolve(res)
				})
			})
		},
		upload(data) {//上传文件
			return new Promise((resolve,) => {
				let formData=new FormData();
				if(data.hasOwnProperty('file')){
					// 传进来的是个对象
					Object.getOwnPropertyNames(data).forEach(function(key){
						formData.append(key, data[key])
					});
				}else{
					// 传进来的是个纯文件
					formData.append('file', data)
				}
				console.log('formData:',formData.get('file'))
				service({
					method: 'post',
					url,
					data:formData,
					headers: {
						'content-type':'multipart/form-data'
					}
				}).then(res => {
					resolve(res)
				})
			})
		},
	}
}
