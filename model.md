# Model

## Project 项目

| Name | Type | Description |
| ---- | ---- | ----------- |
| name_cn | string | 项目中文名称 |
| name_en | string | 项目英文名称(保留) |
| apply_date | date | 项目申报时间(提交申报时间) |
| start_date | date | 项目开始时间(日) |
| end_date | date | 项目结束时间(预估) |
| status | int | 0为正在申报, 1为正在审核, 2为中期检查前, 3为中期检查通过但是项目没有结束, 4为中期检查未通过但是没有结束, 5为项目通过, 6为项目驳回|
| abstract_cn | text | 项目中文摘要 |
| abstract_en | text | 项目英文摘要(保留) |
| project_code_1 | string | 项目代码1 |
| project_code_2 | string | 项目代码2 |
| result_type | int | 预期成果类型, 1为专著, 2为译著, 3为论文(集), 4为研究报告, 5为工具书, 6为电脑软件, 7为其他 |
| apply_funding_count | int | 申请经费总额, 单位为万元 |
| work_unit | string | 工作单位 |
| unit_linkman | string | 单位联系人姓名 |
| unit_linkman_email | string | 联系人邮箱 |
| unit_linkman_tel | string | 单位联系人电话 |
| academy_linkman | string | 学院联系人姓名 |
| academy_linkman_email | string | 学院联系人邮箱 |
| academy_linkman_tel | string | 学院联系人电话 |
| result_index_list | string | "[result_id1..., result_id2, ...]"  |
| member_list | string | {"list":{"name":"",},{},...} |
| project_category_id | int | 项目类型ID |
| funding_plan_id | int | 经费计划ID |

## ProjectCategory 项目类型

| Name | Type | Description |
| ---- | ---- | ----------- |
| category_name | string | 项目类别名称 |
| apply_condition_id | int | 项目申报条件ID |

## Applicant 申报人

| Name | Type | Description |
| ---- | ---- | ----------- |
| name | string | 申报人姓名 |
| sex | boolean | 性别 |
| nation | string | 民族 |
| birth_date | date | 生日 |
| administrative_duty | string | 行政职务 |
| professional_duty | string | 专业职务 |
| last_degree | string | 最后学位 |
| specialization | string | 研究专长 |
| metor | string | 担任导师 |
| province | string | 所在省份 |
| tel | string | 联系电话 |
| location | string | 通讯地址 |
| zip_code | string | 邮政编码 |
| account_id | int | 账户ID |

## FundingPlan 经费计划

| Name | Type | Description |
| ---- | ---- | ----------- |
| count | int | 经费总额 |
| device | float | 设备及耗材 |
| data | float | 资料费 |
| meeting | float | 会议费 |
| travel | float | 差旅费 |
| working | float | 劳务费 |
| manange | float | 管理费 |
| other | float | 其他支出 |
| years | string | JSON格式的年度支出 |
| condition_id | int | 审查条件ID |
| applicant_id | int | 申报人ID |


## Result 成果

| Name | Type | Description |
| ---- | ---- | ----------- |
| result_name | string | 成果名称 |
| result_type | int | 不知道有多少 | 
| start_date | date | 研究阶段开始时间 |
| end_date | date | 研究阶段结束时间 |
| undertakers | string | 承担者们 |