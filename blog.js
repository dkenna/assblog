import * as log from 'loglevel'
import axios from 'axios'

const blogAPI = 'http://{blog}.com:8001/art'

log.setLevel('debug')

class BlogClient {
    constructor () {
      this.user = null
      this.arts = []
      this._article = null
      this.token = null
    }
    setUser () {}
    setToken (token) {
        this.token = token
    }
    articles () {
        return axios.get(blogAPI + 's', {withCredentials: true,
                headers: {'Authorization': `Bearer ${this.token}`}})
    }
    article (id) {
        this._article = axios.get(blogAPI + '/' + id,
            {headers: {'Authorization': `Bearer ${this.token}`}})
        return this._article
    }
    delArticle (id) {
        const resp = axios.delete(blogAPI + '/' + id,
            {headers: {'Authorization': `Bearer ${this.token}`}})
        return resp
    }
    saveArticle (id, data) {
        this._article = axios.put(blogAPI + '/' + id, data,
            {headers: {'Authorization': `Bearer ${this.token}`}})
        return this._article
    }
}

const blog = new BlogClient()
export default blog
