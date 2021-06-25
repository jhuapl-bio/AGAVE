import axios from 'axios'
const HttpsProxyAgent = require("https-proxy-agent")
const httpsAgent = new HttpsProxyAgent({
	"/api": { 
        host: 'localhost',
        protocol: 'https',
        port: 3098
    }
})
// const api = 

export default axios.create({httpsAgent})

