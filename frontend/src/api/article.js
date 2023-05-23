import request from '@/utils/request'

export function fetchList(query) {
  return request({
    url: '/passports/',
    method: 'get',
    params: query
  })
}
export function fetchRecordList(query) {
  return request({
    url: '/records/',
    method: 'get',
    params: query
  })
}

export function fetchIndex() {
  return request({
    url: '/home_data',
    method: 'get'
    // params: query
  })
}

export function fetchCameraList() {
  return request({
    url: '/cameras/',
    method: 'get'
  })
}

export function fetchArticle(id) {
  return request({
    url: '/vue-element-admin/article/detail',
    method: 'get',
    params: { id }
  })
}

export function fetchPv(pv) {
  return request({
    url: '/vue-element-admin/article/pv',
    method: 'get',
    params: { pv }
  })
}

export function createArticle(data) {
  return request({
    url: '/passports/',
    method: 'post',
    data
  })
}
export function publishPassport(pk) {
  return request({
    url: '/passports/',
    method: 'put',
    params: { pk }
  })
}

export function deletePassport(pk) {
  return request({
    url: '/passports/',
    method: 'delete',
    params: { pk }
  })
}

export function updateArticle(data) {
  return request({
    url: '/vue-element-admin/article/update',
    method: 'post',
    data
  })
}
