// Any static23 you want to use has to be imported
// Detail static23 list see https://www.tinymce.com/docs/plugins/
// Custom builds see https://www.tinymce.com/download/custom-builds/

// const static23 = 'print preview searchreplace autolink directionality visualblocks visualchars fullscreen image link media template code codesample table charmap hr pagebreak nonbreaking anchor insertdatetime advlist lists wordcount imagetools textpattern help emoticons autosave bdmap indent2em autoresize lineheight  axupimgs'
if(process.client){
  console.log('123')
  require("tinymce/plugins/print")
  require("tinymce/plugins/preview")
  require("tinymce/plugins/searchreplace")
  require("tinymce/plugins/autolink")
  require("tinymce/plugins/directionality")
  require("tinymce/plugins/visualblocks")
  require("tinymce/plugins/visualchars")
  require("tinymce/plugins/imagetools")
  require("tinymce/plugins/image")
  require("tinymce/plugins/media")
  require("tinymce/plugins/template")
  require("tinymce/plugins/fullscreen")
  require("tinymce/plugins/code")
  require("tinymce/plugins/codesample")
  require("tinymce/plugins/table")
  require("tinymce/plugins/charmap")
  require("tinymce/plugins/hr")
  require("tinymce/plugins/pagebreak")
  require("tinymce/plugins/nonbreaking")
  require("tinymce/plugins/anchor")
  require("tinymce/plugins/insertdatetime")
  require("tinymce/plugins/advlist")
  require("tinymce/plugins/lists")
  require("tinymce/plugins/wordcount")
  require("tinymce/plugins/textpattern")
  require("tinymce/plugins/help")
  require("tinymce/plugins/emoticons")
  require("tinymce/plugins/autosave")
  require("tinymce/plugins/autoresize")
  require("tinymce/plugins/link")
}



const plugins = 'print preview searchreplace autolink directionality visualblocks visualchars fullscreen image link media template code codesample table charmap hr pagebreak nonbreaking anchor insertdatetime advlist lists wordcount imagetools textpattern help emoticons autosave autoresize'


export default plugins
