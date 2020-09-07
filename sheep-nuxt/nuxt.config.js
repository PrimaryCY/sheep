module.exports = {
    mode: 'universal',
    /*
    ** Headers of the page
    */
    head: {
        title: process.env.npm_package_name || '',
        meta: [
            {charset: 'utf-8'},
            {name: 'viewport', content: 'width=device-width, initial-scale=1'},
            {hid: 'description', name: 'description', content: process.env.npm_package_description || ''},
        ],
        link: [
            {rel: 'icon', type: 'image/x-icon', href: '/favicon.png'},
        ],
        script: [
            {src: "http://libs.baidu.com/jquery/1.8.3/jquery.min.js"},
            {src: "http://at.alicdn.com/t/font_1739386_3bmedkb9dpo.js"}
        ],
        bodyAttrs: {
            class: 'left-sidebar is-desktop is-1200px'
        }
    },
    /*
    ** Customize the progress-bar color
    */
    loading: {color: '#fff'},
    /*
    ** Global CSS
    */
    css: [
        // "./static/font/17font.css",
        './static/css/reset.css',
        //导入17素材的css文件
        './static/css/5grid/core.css',
        './static/css/style.css',
        './static/css/5grid/core-desktop.css',
        './static/css/style-desktop.css',
        './static/css/5grid/core-1200px.css',
        './static/css/style-1200px.css',
    ],
    /*
    ** Plugins to load before mounting the App
    */
    plugins: [
        '~/plugins/nuxt-cookies',
        {src: '~/plugins/vue-particles', ssr: false},
        {src: '~/plugins/nprogress', ssr: false},
        {src: '~/plugins/element/element', ssr: true},
        {src: '~/plugins/vue-infinite-scroll', ssr: false},
        {src: '~/plugins/axios', ssr: true},
        {src: '@/plugins/util', ssr: true},
    ],
    router: {
        // middleware: 'user_auth'    // 是js文件名字
    },
    /*
    ** Nuxt.js dev-modules
    */
    buildModules: [
        // Doc: https://github.com/nuxt-community/eslint-module
        '@nuxtjs/eslint-module'
    ],
    /*
    ** Nuxt.js modules
    */
    modules: [
        // Doc: https://axios.nuxtjs.org/usage
        // '@nuxtjs/axios',
        '@nuxtjs/router',
        'cookie-universal-nuxt',
    ],
    /*
    ** Axios module configuration
    ** See https://axios.nuxtjs.org/options
    */
    axios: {},
    /*
    ** Build configuration
    */
    build: {
        analyze: false,
        extractCSS: true,
        optimization: {
            splitChunks: {
                chunks: 'all',
                automaticNameDelimiter: '.',
                name: 'sheep',
                minSize: 200000,
                maxSize: 256000
            }
        },
        extend(config, ctx) {
        },
        vendor: ['axios', 'tinymce/tinymce', '@tinymce/tinymce-vue', 'element-ui'],
        maxChunkSize: 300000
    }
}