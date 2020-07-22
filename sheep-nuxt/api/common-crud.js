import * as qiniu from 'qiniu-js'

import {service} from '@/plugins/axios'
import {guid, extname} from '../utils/util'

export default function (url) {
    if (url.charAt(url.length - 1) !== '/') {
      url = url + '/'
    }

    function url_append_id (id, url) {
      // 详情页面增加id
      if (id) {
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
      retrieve: (id = null, param = {}) => {//详情页请求
        let u = url_append_id(id, url)
        return new Promise((resolve,) => {
          service({
            method: 'get',
            url: u,
            params: param,
          }).then(res => {
            resolve(res)
          })
        })
      },
      create: (data) => {//post请求
        return new Promise((resolve,) => {
          service({
            method: 'post',
            url,
            data: data,
          }).then(res => {
            resolve(res)
          })
        })
      },
      update: (id = null, data) => {//put请求
        let u = url_append_id(id, url)
        return new Promise((resolve,) => {
          service({
            method: 'put',
            url: u,
            data: data,
          }).then(res => {
            resolve(res)
          })
        })
      },
      partial_update: (id = null, data) => {//patch请求
        let u = url_append_id(id, url)
        return new Promise((resolve,) => {
          service({
            method: 'patch',
            url: u,
            data: data,
          }).then(res => {
            resolve(res)
          })
        })
      },
      destory: (id = null, data = {}) => {//delete请求
        let u = url_append_id(id, url)
        return new Promise((resolve,) => {
          service({
            method: 'delete',
            url: u,
            data: data,
          }).then(res => {
            resolve(res)
          })
        })
      },
      upload (data) {//上传文件
        return new Promise((resolve,)  => {
          let history_url = url + 'history/'
          let token_url = url + 'token/'
          service({
            method: 'post',
            url: token_url,
            data: {'bucket': data.upload_path},
          }).then(async(res)=>{
            if(res.data.code!==2000){
              resolve(res)
              return null
            }
            let token = res.data.data.tk

            // 压缩
            let compress_data
            if (data.file.type === "image/jpeg" || data.file.type === "image/png"){
              compress_data = await qiniu.compressImage(data.file, {
                quality: 0.92,
                noCompressIfLarger: true
              })
              compress_data = compress_data.dist
            }

            //修改文件名称
            let new_file_name = `${guid()}.${extname(data.file.name)}`;
            const observable = qiniu.upload(compress_data||data.file, new_file_name, token, {
              fname: data.file.name,
            })

            //上传
            observable.subscribe({
              next(){
                  // 上传中
                  },
              error(){
                // 上传失败
                resolve({
                  data:{
                    msg:'上传失败!'
                  }
                })
              },
              complete(res){
                // 上传成功
                let temp = {}
                temp.data = res
                let complete_data = {
                  url:temp.data.data.url,
                  bucket: data.upload_path,
                  file: new_file_name,
                  raw_file: data.file.name,
                  size: temp.data.data.size
                }
                // 提交上传记录
                service({
                  method: 'post',
                  url:history_url,
                  data: complete_data,
                }).then()
                resolve(temp)
              }
            })
          })
        })
      },
    }
  }

