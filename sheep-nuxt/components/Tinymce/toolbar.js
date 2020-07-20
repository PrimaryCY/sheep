// Here is a list of the toolbar
// Detail list see https://www.tinymce.com/docs/advanced/editor-control-identifiers/#toolbarcontrols

// const toolbar = ['searchreplace bold italic underline strikethrough alignleft aligncenter alignright outdent indent  blockquote undo redo removeformat subscript superscript code codesample', 'hr bullist numlist link image charmap preview anchor pagebreak insertdatetime media table emoticons forecolor backcolor fullscreen','fontsizeselect  fontselect']
const toolbar = [`code undo redo restoredraft | cut copy paste pastetext | forecolor backcolor bold italic underline strikethrough link anchor | alignleft aligncenter alignright alignjustify outdent indent |
    styleselect formatselect fontselect fontsizeselect | bullist numlist | blockquote subscript superscript removeformat |
    table image media charmap emoticons hr pagebreak insertdatetime print preview | fullscreen | bdmap indent2em lineheight formatpainter axupimgs`]

const simple_toolbar = [`undo redo restoredraft | cut copy paste pastetext | forecolor backcolor bold italic underline link | alignleft aligncenter alignright outdent indent |
    formatselect fontselect fontsizeselect | bullist numlist | removeformat image media emoticons hr pagebreak insertdatetime preview | fullscreen |  indent2em lineheight formatpainter axupimgs`]

const reply_toolbar = [`forecolor backcolor bold italic underline link alignleft aligncenter alignright outdent indent
   removeformat image emoticons hr insertdatetime |  indent2em lineheight formatpainter axupimgs`]

const sidebar_reply_toolbar = [`forecolor backcolor bold italic underline link alignleft`]

export default {
  toolbar,
  simple_toolbar,
  reply_toolbar
}

