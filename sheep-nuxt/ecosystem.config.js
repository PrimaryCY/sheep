module.exports = {
    apps: [
        {
            name: 'sheep-nuxt',
            // exec_mode: 'cluster',
            instances: 'max',
            script: './node_modules/nuxt/bin/nuxt.js',
            args: 'start',
            error_file: './log/err.log',
            out_file: './log/out.log',
        }
    ]
}

/* 启动:
pm2 start ecosystem.config.js
*/