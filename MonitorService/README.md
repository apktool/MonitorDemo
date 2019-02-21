# 监控告警

该项目为一个简单的监控告警程序，会通过ambari监控大数据组件的状态，对于其他自己的服务则是通过监控端口号实现的。

对于异常的组件，会发送邮件到配置的邮箱

所有的配置在 config.yaml

## 运行该项目
```bash
python3 main.py
```

## 添加定时任务

考虑到应用场景，将本项目添加到定时任务就可以，比如

```bash
*/5 * * * * cd /MonitorDemo/MonitorService && python3 main.py
```
