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
    url: '/home_data/',
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

export function fetchManagerList() {
  return request({
    url: '/managers/',
    method: 'get'
  })
}

export function fetchProjectList() {
  return request({
    url: '/projects/',
    method: 'get'
  })
}

export function fetchArticle(id) {
  return request({
    url: '/vue-element-admin/article/detail',
    method: 'get',
    params: {id}
  })
}

export function fetchPv(pv) {
  return request({
    url: '/vue-element-admin/article/pv',
    method: 'get',
    params: {pv}
  })
}

export function fetchManagerAuth(data) {
  return request({
    url: '/managers/auth/',
    method: 'post',
    data
  })
}

export function createCamera(data) {
  return request({
    url: '/cameras/',
    method: 'post',
    data
  })
}

export function createManager(data) {
  return request({
    url: '/managers/',
    method: 'post',
    data
  })
}

export function createProject(data) {
  return request({
    url: '/projects/',
    method: 'post',
    data
  })
}

export function fetchProjectDelete(pk) {
  return request({
    url: '/projects/',
    method: 'delete',
    params: {pk}
  })
}

export function fetchCameraDelete(pk) {
  return request({
    url: '/cameras/',
    method: 'delete',
    params: {pk}
  })
}

export function fetchManagerDelete(pk) {
  return request({
    url: '/managers/',
    method: 'delete',
    params: {pk}
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
    params: {pk}
  })
}

export function deletePassport(pk) {
  return request({
    url: '/passports/',
    method: 'delete',
    params: {pk}
  })
}

export function updateArticle(data) {
  return request({
    url: '/vue-element-admin/article/update',
    method: 'post',
    data
  })
}
