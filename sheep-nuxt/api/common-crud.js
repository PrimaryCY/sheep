import {service} from '@/plugins/axios'

export default function(url){
	if(url.charAt(url.length-1)!=='/'){
		url = url+ '/'
	}
	function url_append_id(id, url) {
		// 详情页面增加id
		if(id){
			url = `${url}${id}/`
		}
		return url
	}
	return {
		list: (param = {}) => {//get请求
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
		retrieve: (id=null, param = {}) => {//详情页请求
			let u = url_append_id(id, url)
			return new Promise((resolve,) => {
				service({
					method: 'get',
					url:u,
					params: param,
				}).then(res => {
					resolve(res)
				})
			})
		},
		created:(data)=>{//post请求
			return new Promise((resolve, ) => {
				service({
					method: 'post',
					url,
					data: data,
				}).then(res => {
					resolve(res)
				})
			})
		},
		update:(id=null,data)=>{//put请求
			let u = url_append_id(id, url)
			return new Promise((resolve, ) => {
				service({
					method: 'put',
					url:u,
					data: data,
				}).then(res => {
					resolve(res)
				})
			})
		},
		partial_update:(id=null, data)=>{//patch请求
			let u = url_append_id(id, url)
			return new Promise((resolve, ) => {
				service({
					method: 'patch',
					url:u,
					data: data,
				}).then(res => {
					resolve(res)
				})
			})
		},
		destory:(id=null,data={})=>{//delete请求
			let u = url_append_id(id, url)
			console.log(u)
			return new Promise((resolve, ) => {
				service({
					method: 'delete',
					url:u,
					data: data,
				}).then(res => {
					resolve(res)
				})
			})
		},
		upload(data) {//上传文件
			return new Promise((resolve,) => {
				let formData=new FormData();
				if(Object.prototype.hasOwnProperty.call(data,'file')){
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
