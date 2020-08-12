const middleware = {}

middleware['user_auth'] = require('../middleware/user_auth.js')
middleware['user_auth'] = middleware['user_auth'].default || middleware['user_auth']

export default middleware
