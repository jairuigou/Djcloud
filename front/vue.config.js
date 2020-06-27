module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8000/',
                changeOrigin: true,
                ws: true,
                pathRewrite: {
                  '^/api': ''
                }
            }
        }
    },
    pages: {
        client: {
            entry: 'src/pages/client/main.js'
        },
        admin: {
            entry: 'src/pages/admin/main.js'
        }
    }
}