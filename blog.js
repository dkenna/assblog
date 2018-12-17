import * as log from 'loglevel'
import axios from 'axios'

const blogAPI = 'http://dkenna.com:8001/art'

log.setLevel('debug')

class BlogClient {
    constructor () {
      this.arts = []
      this._article = null
    }
    headers (token) {
        if (token !== null) {
            return {'Authorization': `Bearer ${token}`}
        } else {
            return {}
        }
    }
    articles (token = null) {
        return axios.get(blogAPI + 's', {withCredentials: true,
                headers: this.headers(token)})
    }
    article (id, token) {
        this._article = axios.get(blogAPI + '/' + id,
            {headers: this.headers(token)})
        return this._article
    }
    delArticle (id, token) {
        const resp = axios.delete(blogAPI + '/' + id,
            {headers: this.headers(token)})
        return resp
    }
    saveArticle (id, data, token) {
        this._article = axios.put(blogAPI + '/' + id, data,
            {headers: this.headers(token)})
        return this._article
    }
}

const blog = new BlogClient()
export default blog
