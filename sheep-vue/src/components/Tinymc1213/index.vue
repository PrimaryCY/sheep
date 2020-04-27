<template>
  <div :class="{fullscreen:fullscreen}" class="tinymce-container" :style="{width:containerWidth}">
    <textarea :id="tinymceId" class="tinymce-textarea" />
    <!--    <div class="editor-custom-btn-container">-->
    <!--      <editorImage color="#1890ff" class="editor-upload-btn" @successCBK="imageSuccessCBK" />-->
    <!--    </div>-->

  </div>

</template>
<script>

/**
   * docs:
   * https://panjiachen.github.io/vue-element-admin-site/feature/component/rich-editor.html#tinymce
   */
// import editorImage from './components/EditorImage'
import tinymce from 'tinymce/tinymce' //tinymce默认hidden，不引入不显示
import 'tinymce/themes/silver'

import plugins from '../Tinymce/plugins'
import toolbar from '../Tinymce/toolbar'


// const tinymceCDN = 'https://cdn.jsdelivr.net/npm/tinymce-all-in-one@4.9.5/tinymce.min.js' // 只有这个版本的cdn 没有问题



export default {
  name: 'Tinymce',
  components: {},
  props: {
    id: {
      type: String,
      default: function() {
        return 'vue-tinymce-' + +new Date() + ((Math.random() * 1000).toFixed(0) + '')
      }
    },
    value: {
      type: String,
      default: ''
    },
    toolbar: {
      type: Array,
      required: false,
      default() {
        return []
      }
    },
    menubar: {
      type: String,
      default: 'file edit insert view format table'
    },
    height: {
      type: [Number, String],
      required: false,
      default: 360
    },
    width: {
      type: [Number, String],
      required: false,
      default: 'auto'
    }
  },
  data() {
    return {
      hasChange: false,
      hasInit: false,
      tinymceId: this.id,
      fullscreen: false,
      languageTypeList: {
        'en': 'en',
        'zh': 'zh_CN',
        'es': 'es_MX',
        'ja': 'ja'
      }
    }
  },
  computed: {
    containerWidth() {
      const width = this.width
      if (/^[\d]+(\.[\d]+)?$/.test(width)) { // matches `100`, `'100'`
        return `${width}px`
      }
      return width
    }
  },
  watch: {
    value: {
      handler(val) {
        if (!this.hasChange && this.hasInit) {
          this.$nextTick(() =>
            window.tinymce.get(this.tinymceId).setContent(val || ''))
        }
      },
      immediate: true,
      deep: true
    }

  },
  mounted() {
    console.log('富文本生命周期')
    this.init()
  },
  activated() {
    if (window.tinymce) {
      this.initTinymce()
    }
  },
  deactivated() {
    this.destroyTinymce()
  },
  destroyed() {
    this.destroyTinymce()
  },
  methods: {
    init() {
      // dynamic load tinymce from cdn
      // load(tinymceCDN, (err) => {
      //   if (err) {
      //     this.$message.error(err.message)
      //     return
      //   }
      //   this.initTinymce()
      // })
      // 不使用cdn  使用本地的tinymce
      window.tinymce=tinymce
			this.initTinymce()
    },
    initTinymce() {
      const _this = this
      window.tinymce.init({
        selector: `#${this.tinymceId}`,
        base_url: './static/tinymce/',
        skin_url: './static/tinymce/skins/ui/oxide/',
        emoticons_database_url: './static/tinymce/plugins/emojis/emojis.js',
        language_url: './static/tinymce/langs/zh_CN.js',
        theme:'silver',
        fontsize_formats: '12px 14px 16px 18px 24px 36px 48px 56px 72px',
        font_formats: '微软雅黑=Microsoft YaHei,Helvetica Neue,PingFang SC,sans-serif;苹果苹方=PingFang SC,Microsoft YaHei,sans-serif;宋体=simsun,serif;仿宋体=FangSong,serif;黑体=SimHei,sans-serif;Arial=arial,helvetica,sans-serif;Arial Black=arial black,avant garde;Book Antiqua=book antiqua,palatino;',
        link_list: [
          { title: '百度', value: 'http://www.baidu.com' },
          { title: '新浪', value: 'http://www.sina.com' }
        ],
        image_list: [
          { title: '预置图片1', value: 'https://www.tiny.cloud/images/glyph-tinymce@2x.png' },
          { title: '预置图片2', value: 'https://www.baidu.com/img/bd_logo1.png' }
        ],
        image_class_list: [
          { title: 'None', value: '' },
          { title: 'Some class', value: 'class-name' }
        ],
        importcss_append: true,
        schema: 'html5',
        content_style: 'img { margin-bottom: 10px;  width:100%}',
        language: this.languageTypeList['zh'],
        height: this.height,
        min_height: this.height,
        body_class: 'panel-body',
        object_resizing: true, // 此选项允许您打开/关闭图像、表或媒体对象的大小调整句柄。默认情况下，此选项处于启用状态，允许您调整表和图像的大小。您还可以指定一个CSS3选择器来选择要在其上启用大小调整的对象。
        toolbar: this.toolbar.length > 0 ? this.toolbar : toolbar,
        menubar: this.menubar, // 菜单栏
        plugins: plugins,
        end_container_on_empty_block: true, // 如果在空的内部块元素中按enter键，则此选项允许您拆分当前容器块元素

        powerpaste_word_import: 'clean', // https://www.tiny.cloud/docs/plugins/powerpaste/#powerpaste_word_import 此设置控制如何筛选从Microsoft Word粘贴的内容。
        code_dialog_height: 450, // 此配置选项设置对话框的内部可编辑区域高度code。 请注意，实际模态的外部尺寸将略大于设置的值。
        code_dialog_width: 1000, // 此配置选项设置对话框的内部可编辑区域宽度code。 请注意，实际模态的外部尺寸将略大于设置的值。

        advlist_bullet_styles: 'square', // 此选项允许您在默认bullist工具栏控件中包含特定的无序列表项标记。此选项允许您在默认bullist工具栏控件中包含特定的无序列表项标记。https://www.tiny.cloud/docs-4x/plugins/advlist/#advlist_bullet_styles
        advlist_number_styles: 'default', // 此选项允许您在默认的numlist工具栏控件中包含特定的有序列表项标记。
        /* https://www.tiny.cloud/docs-4x/plugins/imagetools/#imagetools_cors_hosts
                      由于浏览器对所谓的跨域HTTP请求施加了安全性措施，因此Image Tools无法使用来自其他域的图像。为了克服这些限制，必须在指定的域上显式启用跨域资源共享（CORS）（有关更多信息，请参阅HTTP访问控制）。
              可以通过imagetools_cors_hosts选件将一系列受支持的图像域（启用了CORS）提供给TinyMCE 。

              注意：数组中的每个字符串都必须采用的格式mydomain.com。http://, https://域中请勿包含协议（）或任何斜杠。

              注： imagetools_cors_hosts在不使通过这个插件时，需要TinyMCE的云。
              类型： String[]
                      * */
        imagetools_cors_hosts: ['www.tinymce.com', 'codepen.io'], //
        // 自定义上传逻辑
        images_upload_handler: (blobInfo, success, failure) => {
          // const img = 'data:image/jpeg;base64,' + blobInfo.base64()
          // success(img)
          const file = blobInfo.blob()// 转化为易于理解的file对象
          const formData = new FormData()
          formData.append('image', file)

          this.$api.globalApi.upLoadImage(formData).then(function(res) {
            console.log(res)
            if (res.status === 0) {
              const data = res.data
              success(data.file_path)
            }
          }).catch(function(error) {
            if (error.response) {
              // The request was made and the server responded with a status code
              // that falls out of the range of 2xx
              failure('文件上传失败(' + error.response.status + ')，' + error.response.data)
            } else if (error.request) {
              // The request was made but no response was received
              // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
              // http.ClientRequest in node.js
              failure('文件上传失败，服务器端无响应')
            } else {
              // Something happened in setting up the request that triggered an Error
              failure('文件上传失败，请求封装失败')
            }
          })
        },
        file_picker_callback: (callback, value, meta) => {
          // Provide file and text for the link dialog
          if (meta.filetype === 'file') {
            callback('mypage.html', { text: 'My text' })
          }
          // Provide image and alt text for the image dialog
          if (meta.filetype === 'image') {
            callback('请输入正确的图片外链地址例如:https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif')
          }
          // Provide alternative source and posted for the media dialog
          if (meta.filetype === 'media') {
            // 要先模拟出一个input用于上传本地文件
            console.log(value)
            console.log(meta)
            var input = document.createElement('input')
            input.setAttribute('type', 'file')
            // 你可以给input加accept属性来限制上传的文件类型
            // 例如：input.setAttribute('accept', '.jpg,.png');
            input.click()
            const _this = this
            input.onchange = function() {
              const file = this.files[0]
              const formData = new FormData()
              formData.append('video', file)
              _this.$api.globalApi.upLoadVideo(formData).then(function(res) {
                console.log(res)
                if (res.status === 0) {
                  const data = res.data
                  console.log(data)

                  // callback(data.file_path)
                  callback(data.file_path)
                }
              }).catch(function(error) {
                if (error.response) {
                  // The request was made and the server responded with a status code
                  // that falls out of the range of 2xx
                  _this.$meesage('文件上传失败(' + error.response.status + ')，' + error.response.data)
                } else if (error.request) {
                  // The request was made but no response was received
                  // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                  // http.ClientRequest in node.js
                  _this.$message('文件上传失败，服务器端无响应')
                } else {
                  // Something happened in setting up the request that triggered an Error
                  _this.$message('文件上传失败，请求封装失败')
                }
              })

              //
              // var xhr, formData
              // console.log(file.name)
              // xhr = new XMLHttpRequest()
              // xhr.withCredentials = false
              // xhr.open('POST', '/demo/upimg.php')
              // xhr.onload = function() {
              //   var json
              //   if (xhr.status != 200) {
              //     failure('HTTP Error: ' + xhr.status)
              //     return
              //   }
              //   json = JSON.parse(xhr.responseText)
              //   if (!json || typeof json.location !== 'string') {
              //     failure('Invalid JSON: ' + xhr.responseText)
              //     return
              //   }
              //   callback(json.location)
              // }
              // formData = new FormData()
              // formData.append('file', file, file.name)
              // xhr.send(formData)
            }
          }
        },

        default_link_target: '_blank', // 使用此选项，您可以在插入/编辑链接时为链接设置默认目标
        link_title: false, // 此选项使您可以禁用对话框中的链接title输入字段link。
        /*
                      * 使用此选项，您可以&nbsp;在用户按下键盘tab键时强制TinyMCE插入三个实体。

              请务必注意，这不会更改菜单和工具栏控件的行为，&nbsp当nonbreaking_force_tabvalue 为时，菜单和工具栏控件将继续插入单个实体true。
              但是，true条件确实捕获了Tab键并将其包含在可编辑区域中，而当设置为falseTab键的默认状态时，按下该键会将光标移动到下一个可编辑区域（例如，当前页面上的浏览器网址栏或表单字段） ）。*/
        nonbreaking_force_tab: true, // tab缩进
        /* 使用init_instance_callback选项，您可以指定每次初始化编辑器实例时要执行的函数名称。该函数的格式为initInstance(editor)哪里editor是编辑器实例对象引用。
                      * */
        init_instance_callback: editor => {
          if (_this.value) {
            editor.setContent(_this.value)
          }
          _this.hasInit = true
          editor.on('NodeChange Change KeyUp SetContent', () => {
            this.hasChange = true
            this.$emit('input', editor.getContent())
          })
        },
        /*
                      * 此选项使您可以指定在渲染TinyMCE编辑器实例之前将执行的回调。

              要指定设置回调，请为该setup选项提供JavaScript函数。该函数应该有一个参数，该参数是对正在设置的编辑器的引用。

              此设置的常见用例是将编辑器事件新增到TinyMCE。例如，如果您想向TinyMCE新增点击事件，则可以通过设置配置设置来新增它。
                      * */
        setup(editor) {
          editor.on('FullscreenStateChanged', (e) => {
            console.log(e)
            _this.fullscreen = e.state
          })
        }
        // 整合七牛上传
        // images_dataimg_filter(img) {
        //   setTimeout(() => {
        //     const $image = $(img);
        //     $image.removeAttr('width');
        //     $image.removeAttr('height');
        //     if ($image[0].height && $image[0].width) {
        //       $image.attr('data-wscntype', 'image');
        //       $image.attr('data-wscnh', $image[0].height);
        //       $image.attr('data-wscnw', $image[0].width);
        //       $image.addClass('wscnph');
        //     }
        //   }, 0);
        //   return img
        // },
        // images_upload_handler(blobInfo, success, failure, progress) {
        //   progress(0);
        //   const token = _this.$store.getters.token;
        //   getToken(token).then(response => {
        //     const url = response.data.qiniu_url;
        //     const formData = new FormData();
        //     formData.append('token', response.data.qiniu_token);
        //     formData.append('key', response.data.qiniu_key);
        //     formData.append('file', blobInfo.blob(), url);
        //     upload(formData).then(() => {
        //       success(url);
        //       progress(100);
        //     })
        //   }).catch(err => {
        //     failure('出现未知问题，刷新页面，或者联系程序员')
        //     console.log(err);
        //   });
        // },
      })
    },
    destroyTinymce() {
      const tinymce = window.tinymce.get(this.tinymceId)
      if (this.fullscreen) {
        tinymce.execCommand('mceFullScreen')
      }

      if (tinymce) {
        tinymce.destroy()
      }
    },
    setContent(value) {
      window.tinymce.get(this.tinymceId).setContent(value)
    },
    getContent() {
      window.tinymce.get(this.tinymceId).getContent()
    },
    imageSuccessCBK(arr) {
      const _this = this
      arr.forEach(v => {
        window.tinymce.get(_this.tinymceId).insertContent(`<img class="wscnph" src="${v.url}" >`)
      })
    }
  }
}
</script>

<style scoped>

  .img-class {
    width: 100% !important;
  }

  .tinymce-container {
    position: relative;
    line-height: normal;
  }

  .tinymce-container >>> .mce-fullscreen {
    z-index: 10000;
  }

  .tinymce-textarea {
    visibility: hidden;
    z-index: -1;
  }

  .editor-custom-btn-container {
    position: absolute;
    right: 4px;
    top: 4px;
    /*z-index: 2005;*/
  }

  .fullscreen .editor-custom-btn-container {
    z-index: 10000;
    position: fixed;
  }

  .editor-upload-btn {
    display: inline-block;
  }
</style>
