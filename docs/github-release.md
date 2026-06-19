# GitHub首版发布说明

## 建议仓库信息

- 仓库名称：`three-high-sector-evaluation`
- 显示名称：三高产业链板块评估模型
- 可见性：建议公开（Public）
- 简介：`面向A股AI算力产业链的三高板块评估与气泡图工具。`
- 主页：首版留空
- License：MIT

## 建议Topics

```text
a-share
quantitative-research
industry-chain
sector-analysis
ai-infrastructure
python
data-visualization
chinese-stock-market
```

## 首次提交说明

```text
feat: 发布三高产业链板块评估模型 v0.1.0
```

## Release标题

```text
v0.1.0 首个可运行演示版本
```

## Release正文

这是“三高产业链板块评估模型”的首个可运行版本，面向A股AI算力产业链的3至12个月中期产业配置研究。

主要功能：

- 15个正式排名板块和3个下游观察板块；
- 高增长、高利润、高围墙三维气泡图；
- 估值温度、市场状态和数据置信度；
- 板块筛选、评分明细和CSV导出；
- 零第三方运行依赖，执行`python server.py`即可启动；
- 自动测试和GitHub Actions。

重要说明：当前仓库使用合成演示数据，只验证模型结构和软件流程，不构成投资建议。下一版本将验证光模块、AI服务器和IDC三个代表板块的免费真实数据。

## 发布复核清单

- [x] 项目可以本地运行
- [x] 核心测试通过
- [x] 演示数据已明确标注
- [x] 不含API key和个人路径
- [x] 不含付费数据和完整研报
- [x] README包含运行说明和免责声明
- [x] 已加入LICENSE、贡献指南和安全说明
- [ ] GitHub仓库已创建
- [ ] 首次提交已推送
- [ ] GitHub Actions已通过
- [ ] v0.1.0 Release已发布
