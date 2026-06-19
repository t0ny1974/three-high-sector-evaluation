# 三高产业链板块评估模型

面向 A 股 AI 算力产业链的中期板块研究工具。模型通过“高增长、高利润、高围墙”评价产业质量，并使用“估值温度”和“市场状态”辅助判断研究时点。

> 当前版本只评估产业链细分板块，不选择个股，不提供买卖建议。仓库内置数据全部是界面演示数据，不代表真实市场判断。

## 当前版本

`v0.1.0`是首个可运行演示版本。发布内容见[更新日志](CHANGELOG.md)，GitHub发布材料见[首版发布说明](docs/github-release.md)。

## 当前范围

- 市场：A 股
- 产业链：AI 算力
- 研究周期：3 至 12 个月
- 正式排名：10 个上游板块、5 个中游板块
- 观察板块：3 个下游板块，不参与正式排名

## 五个维度

- `增长分`：气泡大小
- `利润分`：纵轴
- `围墙分`：横轴
- `估值温度`：0 代表相对便宜，100 代表相对昂贵
- `市场状态`：0 代表弱势，100 代表强势

产业质量分：

```text
增长分 × 35% + 利润分 × 30% + 围墙分 × 35%
```

估值温度和市场状态不计入产业质量分，避免把产业质量与交易时点混为一谈。

## 快速开始

需要 Python 3.11 或更高版本。

```powershell
cd C:\LifeOS\projects\three-high-sector-evaluation
python server.py
```

浏览器打开 `http://127.0.0.1:8501`。第一版运行不需要安装第三方 Python 包。

## 测试

核心模型只使用 Python 标准库：

```powershell
python -m unittest discover -s tests -v
```

## 项目结构

```text
server.py                      零依赖本地 HTTP 服务器
config/
  model.json                   模型权重、阈值和研究周期
  sectors.json                 产业链板块定义
data/
  sample/sector_scores.csv     明确标注的演示数据
docs/
  architecture.md              软件架构
  methodology.md               评分方法
  data-policy.md               数据来源与时间口径
  github-release.md            GitHub首版发布材料
src/three_high_model/
  config.py                    配置读取
  model.py                     评分与状态判定
  repository.py                板块快照读取
tests/                         核心测试
web/                           原生网页、样式和气泡图交互
CHANGELOG.md                   版本更新日志
```

## 数据边界

第一阶段将采用免费数据进行研究原型验证。免费接口可能变化，且部分数据存在商业使用限制，因此：

- 原始数据必须缓存并记录来源与抓取时间。
- 财务数据必须记录报告期、公告日和可用日期。
- 历史回测不得使用当时尚未公开的数据。
- 免费盈利预测不进入历史回测，除非已经保存当时的预测快照。
- 将来接入 Wind、Choice 或 iFinD 时，通过数据适配器替换来源，不修改评分核心。

## GitHub 发布前检查

- 不提交 `.env`、API key、付费数据或受限制原始数据。
- 示例数据必须明确标记为 synthetic/demo。
- 研究证据必须记录来源，不复制受版权保护的完整报告。
- 发布前运行测试并复核免责声明。

详细规则见 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [SECURITY.md](SECURITY.md)。

## 免责声明

本项目用于软件开发、量化研究方法和数据可视化学习，不构成证券研究报告、投资顾问服务或任何买卖建议。模型分数依赖数据质量、板块分类和主观研究判断，可能存在重大错误。

## License

代码采用 [MIT License](LICENSE)。数据、第三方接口和研究材料仍受各自许可条款约束。
