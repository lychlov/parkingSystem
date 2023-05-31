<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.title" placeholder="项目名称" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="listQuery.sort" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key"/>
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        添加
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange"
    >
      <el-table-column label="ID" prop="id" sortable="custom" align="center" width="80" :class-name="getSortClass('id')">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="项目名称" min-width="150px">
        <template slot-scope="{row}">
          <span class="link-type" @click="handleUpdate(row)">{{ row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="施工许可证" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.token }}</span>
        </template>
      </el-table-column>
      <el-table-column label="开发企业" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.provider }}</span>
        </template>
      </el-table-column>
      <el-table-column label="工程名称" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.construction_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="总包单位" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.total_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="项目经理" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.pm_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="实名制负责人" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.smj_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="经理公司" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.jl_corp_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="总监" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.jl_name }}</span>
        </template>
      </el-table-column>
<!--      <el-table-column label="Date" width="150px" align="center">-->
<!--        <template slot-scope="{row}">-->
<!--          <span>{{ row.timestamp | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>-->
<!--        </template>-->
<!--      </el-table-column>-->
<!---->
<!--      <el-table-column label="Author" width="110px" align="center">-->
<!--        <template slot-scope="{row}">-->
<!--          <span>{{ row.author }}</span>-->
<!--        </template>-->
<!--      </el-table-column>-->
<!--      <el-table-column v-if="showReviewer" label="Reviewer" width="110px" align="center">-->
<!--        <template slot-scope="{row}">-->
<!--          <span style="color:red;">{{ row.reviewer }}</span>-->
<!--        </template>-->
<!--      </el-table-column>-->
<!--      <el-table-column label="Imp" width="80px">-->
<!--        <template slot-scope="{row}">-->
<!--          <svg-icon v-for="n in + row.importance" :key="n" icon-class="star" class="meta-item__icon" />-->
<!--        </template>-->
<!--      </el-table-column>-->
<!--      <el-table-column label="Readings" align="center" width="95">-->
<!--        <template slot-scope="{row}">-->
<!--          <span v-if="row.pageviews" class="link-type" @click="handleFetchPv(row.pageviews)">{{ row.pageviews }}</span>-->
<!--          <span v-else>0</span>-->
<!--        </template>-->
<!--      </el-table-column>-->
<!--      <el-table-column label="Status" class-name="status-col" width="100">-->
<!--        <template slot-scope="{row}">-->
<!--          <el-tag :type="row.status | statusFilter">-->
<!--            {{ row.status }}-->
<!--          </el-tag>-->
<!--        </template>-->
<!--      </el-table-column>-->
      <el-table-column label="操作" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            详情
          </el-button>
<!--          <el-button v-if="row.status!='published'" size="mini" type="success" @click="handleModifyStatus(row,'published')">-->
<!--            Publish-->
<!--          </el-button>-->
<!--          <el-button v-if="row.status!='draft'" size="mini" @click="handleModifyStatus(row,'draft')">-->
<!--            Draft-->
<!--          </el-button>-->
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleDelete(row,$index)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="120px" style="width: 400px; margin-left:50px;">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="施工许可证" prop="token">
          <el-input v-model="temp.token" />
        </el-form-item>
        <el-form-item label="开发企业名称" prop="provider">
          <el-input v-model="temp.provider" />
        </el-form-item>
        <el-form-item label="开发企业社会代码" prop="provider_no">
          <el-input v-model="temp.provider_no" />
        </el-form-item>
        <el-form-item label="开发企业注册地址" prop="provider_address">
          <el-input v-model="temp.provider_address" />
        </el-form-item>
        <el-form-item label="开发企业注册日期" prop="provider_sign_date">
          <el-date-picker v-model="temp.provider_sign_date" type="date" placeholder="Please pick a date" />
        </el-form-item>
        <el-form-item label="工程名称" prop="construction_name">
          <el-input v-model="temp.construction_name" />
        </el-form-item>
        <el-form-item label="总包信用代码" prop="total_no">
          <el-input v-model="temp.total_no" />
        </el-form-item>
        <el-form-item label="总包单位名称" prop="total_name">
          <el-input v-model="temp.total_name" />
        </el-form-item>
        <el-form-item label="项目经理" prop="pm_name">
          <el-input v-model="temp.pm_name" />
        </el-form-item>
        <el-form-item label="项目经理电话" prop="pm_name">
          <el-input v-model="temp.pm_phone" />
        </el-form-item>
        <el-form-item label="项目分类" prop="category">
          <el-input v-model="temp.category" />
        </el-form-item>
        <el-form-item label="项目所在区县" prop="az_name">
          <el-input v-model="temp.zone_name" />
        </el-form-item>
        <el-form-item label="项目具体地址" prop="address">
          <el-input v-model="temp.address" />
        </el-form-item>
        <el-form-item label="开工日期" prop="start_date">
          <el-date-picker v-model="temp.start_date" type="date" placeholder="Please pick a date" />
        </el-form-item>
        <el-form-item label="竣工日期" prop="complete_date">
          <el-date-picker v-model="temp.complete_date" type="date" placeholder="Please pick a date" />
        </el-form-item>
        <el-form-item label="项目状态" prop="status">
          <el-input v-model="temp.status" />
        </el-form-item>
        <el-form-item label="建设规模" prop="construct_size">
          <el-input v-model="temp.construct_size" />
        </el-form-item>
        <el-form-item label="建设性质" prop="construct_type">
          <el-input v-model="temp.construct_type" />
        </el-form-item>
        <el-form-item label="工程用途" prop="construct_usage">
          <el-input v-model="temp.construct_usage" />
        </el-form-item>
        <el-form-item label="项目实名制负责人" prop="smj_name">
          <el-input v-model="temp.smj_name" />
        </el-form-item>
        <el-form-item label="项目实名制负责人电话" prop="smj_phone">
          <el-input v-model="temp.smj_phone" />
        </el-form-item>
        <el-form-item label="项目实名制负责人邮箱" prop="smj_email">
          <el-input v-model="temp.smj_email" />
        </el-form-item>
        <el-form-item label="监理单位名称" prop="jl_corp_name">
          <el-input v-model="temp.jl_corp_name" />
        </el-form-item>
        <el-form-item label="监理单位统一社会信用代码" prop="jl_corp_code">
          <el-input v-model="temp.jl_corp_code" />
        </el-form-item>
        <el-form-item label="项目总监" prop="jl_name">
          <el-input v-model="temp.jl_name" />
        </el-form-item>
        <el-form-item label="总监电话" prop="jl_phone">
          <el-input v-model="temp.jl_phone" />
        </el-form-item>
        <el-form-item label="设备安装公司" prop="az_phone">
          <el-input v-model="temp.az_phone" />
        </el-form-item>
<!--        <el-form-item label="Type" prop="type">-->
<!--          <el-select v-model="temp.type" class="filter-item" placeholder="Please select">-->
<!--            <el-option v-for="item in calendarTypeOptions" :key="item.key" :label="item.display_name" :value="item.key" />-->
<!--          </el-select>-->
<!--        </el-form-item>-->
<!--        <el-form-item label="Date" prop="timestamp">-->
<!--          <el-date-picker v-model="temp.timestamp" type="datetime" placeholder="Please pick a date" />-->
<!--        </el-form-item>-->
<!--        <el-form-item label="Title" prop="title">-->
<!--          <el-input v-model="temp.title" />-->
<!--        </el-form-item>-->
<!--        <el-form-item label="Status">-->
<!--          <el-select v-model="temp.status" class="filter-item" placeholder="Please select">-->
<!--            <el-option v-for="item in statusOptions" :key="item" :label="item" :value="item" />-->
<!--          </el-select>-->
<!--        </el-form-item>-->
<!--        <el-form-item label="Imp">-->
<!--          <el-rate v-model="temp.importance" :colors="['#99A9BF', '#F7BA2A', '#FF9900']" :max="3" style="margin-top:8px;" />-->
<!--        </el-form-item>-->
<!--        <el-form-item label="Remark">-->
<!--          <el-input v-model="temp.remark" :autosize="{ minRows: 2, maxRows: 4}" type="textarea" placeholder="Please input" />-->
<!--        </el-form-item>-->
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          确认
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :visible.sync="dialogPvVisible" title="Reading statistics">
      <el-table :data="pvData" border fit highlight-current-row style="width: 100%">
        <el-table-column prop="key" label="Channel" />
        <el-table-column prop="pv" label="Pv" />
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogPvVisible = false">Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
// TODO
import { fetchProjectList, fetchPv, createProject, updateArticle } from '@/api/article'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

const calendarTypeOptions = [
  { key: 'CN', display_name: 'China' },
  { key: 'US', display_name: 'USA' },
  { key: 'JP', display_name: 'Japan' },
  { key: 'EU', display_name: 'Eurozone' }
]

// arr to obj, such as { CN : "China", US : "USA" }
const calendarTypeKeyValue = calendarTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    },
    typeFilter(type) {
      return calendarTypeKeyValue[type]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        title: undefined,
        sort: '+id'
      },
      importanceOptions: [1, 2, 3],
      calendarTypeOptions,
      sortOptions: [{ label: 'ID升序', key: '+id' }, { label: 'ID降序', key: '-id' }],
      statusOptions: ['published', 'draft', 'deleted'],
      showReviewer: false,
      temp: {
        address: '输入地址',
        zone_name: 'XX区',
        az_phone: '13512345678',
        category: '房屋建筑工程',
        complete_date: '2023-04-30T16:00:00.000Z',
        construct_size: '大型',
        construct_type: '新建',
        construct_usage: '居住建筑',
        construction_name: '工程名称',
        jl_corp_code: '社会代码',
        jl_corp_name: '监理',
        jl_name: '监理公司',
        jl_phone: '13512345678',
        name: '项目名称',
        pm_name: '项目经理',
        pm_phone: '13512345678',
        provider: '开发企业',
        provider_address: '地址',
        provider_no: '代码',
        provider_sign_date: '2023-04-30T16:00:00.000Z',
        smj_email: '123@139.com',
        smj_name: '实名制',
        smj_phone: '13512345678',
        start_date: '2023-04-30T16:00:00.000Z',
        status: '筹备',
        token: '1',
        total_name: '总包',
        total_no: '代码'
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      dialogPvVisible: false,
      pvData: [],
      rules: {
        address: [{ required: true, message: '必填项', trigger: 'change' }],
        zone_name: [{ required: true, message: '必填项', trigger: 'change' }],
        az_phone: [{ required: true, message: '必填项', trigger: 'change' }],
        category: [{ required: true, message: '必填项', trigger: 'change' }],
        complete_date: [{ required: true, message: '必填项', trigger: 'change' }],
        construct_size: [{ required: true, message: '必填项', trigger: 'change' }],
        construct_type: [{ required: true, message: '必填项', trigger: 'change' }],
        construct_usage: [{ required: true, message: '必填项', trigger: 'change' }],
        construction_name: [{ required: true, message: '必填项', trigger: 'change' }],
        jl_corp_code: [{ required: true, message: '必填项', trigger: 'change' }],
        jl_corp_name: [{ required: true, message: '必填项', trigger: 'change' }],
        jl_name: [{ required: true, message: '必填项', trigger: 'change' }],
        jl_phone: [{ required: true, message: '必填项', trigger: 'change' }],
        name: [{ required: true, message: '必填项', trigger: 'change' }],
        pm_name: [{ required: true, message: '必填项', trigger: 'change' }],
        pm_phone: [{ required: true, message: '必填项', trigger: 'change' }],
        provider: [{ required: true, message: '必填项', trigger: 'change' }],
        provider_address: [{ required: true, message: '必填项', trigger: 'change' }],
        provider_no: [{ required: true, message: '必填项', trigger: 'change' }],
        provider_sign_date: [{ required: true, message: '必填项', trigger: 'change' }],
        smj_email: [{ required: true, message: '必填项', trigger: 'change' }],
        smj_name: [{ required: true, message: '必填项', trigger: 'change' }],
        smj_phone: [{ required: true, message: '必填项', trigger: 'change' }],
        start_date: [{ required: true, message: '必填项', trigger: 'change' }],
        status: [{ required: true, message: '必填项', trigger: 'change' }],
        token: [{ required: true, message: '必填项', trigger: 'change' }],
        total_name: [{ required: true, message: '必填项', trigger: 'change' }],
        total_no: '代码'
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      fetchProjectList(this.listQuery).then(response => {
        this.list = response.data.items
        this.total = response.data.total

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: '操作Success',
        type: 'success'
      })
      row.status = status
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    resetTemp() {
      this.temp = {
        address: '输入地址',
        zone_name: 'XX区',
        az_phone: '13512345678',
        category: '房屋建筑工程',
        complete_date: '2023-04-30T16:00:00.000Z',
        construct_size: '大型',
        construct_type: '新建',
        construct_usage: '居住建筑',
        construction_name: '工程名称',
        jl_corp_code: '社会代码',
        jl_corp_name: '监理',
        jl_name: '监理公司',
        jl_phone: '13512345678',
        name: '项目名称',
        pm_name: '项目经理',
        pm_phone: '13512345678',
        provider: '开发企业',
        provider_address: '地址',
        provider_no: '代码',
        provider_sign_date: '2023-04-30T16:00:00.000Z',
        smj_email: '123@139.com',
        smj_name: '实名制',
        smj_phone: '13512345678',
        start_date: '2023-04-30T16:00:00.000Z',
        status: '筹备',
        token: '1',
        total_name: '总包',
        total_no: '代码'
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          createProject(this.temp).then(() => {
            this.list.unshift(this.temp)
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Created Successfully',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      // this.temp.timestamp = new Date(this.temp.timestamp)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          // tempData.timestamp = +new Date(tempData.timestamp) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464
          updateArticle(tempData).then(() => {
            const index = this.list.findIndex(v => v.id === this.temp.id)
            this.list.splice(index, 1, this.temp)
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Update Successfully',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleDelete(row, index) {
      this.$notify({
        title: 'Success',
        message: 'Delete Successfully',
        type: 'success',
        duration: 2000
      })
      this.list.splice(index, 1)
    },
    handleFetchPv(pv) {
      fetchPv(pv).then(response => {
        this.pvData = response.data.pvData
        this.dialogPvVisible = true
      })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['timestamp', 'title', 'type', 'importance', 'status']
        const filterVal = ['timestamp', 'title', 'type', 'importance', 'status']
        const data = this.formatJson(filterVal)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'table-list'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal) {
      return this.list.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
    }
  }
}
</script>
