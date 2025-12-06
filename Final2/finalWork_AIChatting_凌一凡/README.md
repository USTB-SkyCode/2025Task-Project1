# SkyCode2025秋令营 Project1
D202310033 凌一凡



# 内容简介与打开方式

**内容简介**

AI聊天机器人页面（即作业选项2，同时考虑作业1的提示词工程）

本项目基于自己自学的python、html、css、js和AI、bilibili提供的flask教程和代码服务完成。

前端HTML，后端python结合这几周学到的大模型调用，本例用的是python ollma api调用本地的Qwen模型

**打开方式**

- pip flask, ollama
- 需要有ollama, python ollama和Qwen3:4b模型

**在vscode打开项目文件夹，运行app.py，然后访问127.0.0.1：80即可**



# 提示词预设（作业1内容）

[(95 封私信 / 80 条消息) prompt指令之角色篇：角色扮演提示词深度梳理，全文干货【精华】 - 知乎](https://zhuanlan.zhihu.com/p/671981062)

[PromptIDE 提示词开发工具 | 巨人肩膀](https://www.atbigapp.com/prompt?t=jj)

[免费提示生成器：AI提示创建器 | 生成提示](https://prompt-generators.com/zh/ai-prompt-generator)

课程要求（交付选项1）：

> 以文本形式设计一段提示词，该提示词是一份用于**角色扮演**的提示词。需要为大模型指定一个具体的**人设和风格**，并且提示词能够经得起用户的考验（即使用户试探，模型也不能输出一些不该回答的内容，要**合理拒绝**回答某些内容，且对不良请求具有鲁棒性）
>
> 交付：一段提示词，以及将其输入到任意大模型聊天系统（dpsk,qwen,自部署模型...）中进行测试的结果（截图or文档）

提示词保存在`backend\prompts.py`

## 效果展示

[效果见此文件](./prompt_result.md)

# AI聊天助手（作业2内容，即本项目）

> 开发一个聊天的系统，可以直接通过命令行交互或者有GUI
>
> - 对额外信息的获取（如日期、时间）
>   - 对话泡泡自带发送时间
> - 一定的记忆功能（截取对话、总结对话、外部数据库，树的查找结构？）

## 效果展示

1.记忆功能：

```
# 测试时的聊天记录
hi!
你好！很高兴和你聊天。有什么我可以帮你的吗？😊

what did i just say
你刚刚说：**"hi!"** 😊  
有什么需要我帮忙的吗？

what did i just say
你刚刚说：**"what did i just say"** 😊  
（这是你上一条消息的内容，想再确认吗？）
```





# 笔记

## css、js文件引用

- 文件目录修改

  ```
  原目录
  your_project/
  ├── main.py
  ├── frontend/ 
  │   ├── index.html
  │   ├── index.css
  │   └── index.js 
  └── backend/   
      └── chat.py
  ```

  根据flask的要求改成：

  ```
  your_project/
  ├── app.py               # Flask应用入口
  ├── templates/           # HTML模板文件夹（flask默认读取位置）
  │   └── index.html       # 需引用静态文件的HTML
  └── static/              # 静态文件根目录（flask默认读取位置）
  │   ├── css/             # 样式表文件夹
  │   │   └── style.css    # 外部CSS文件
  │   ├── js/              # JavaScript文件夹
  │   │   └── main.js      # 外部JS文件
  │	└── img/
  │   	└── favicon.ico	# 网页图标
  └── backend/
  	├── chat.py			# AI聊天相关函数
  	└── prompt.py		# 提示词配置
  	
  ```

  flask将会通过`render_template()`函数渲染`./templates`文件夹中的html

  其他文件默认在`./static`文件夹获取

- 文件引用代码修改

  而且html中的css和js路径改成可以由flask读取的格式：`"{{ url_for('static', filename='css/style.css') }}"`

  附原格式（相对于html的路径）：`../img/favicon.ico`

## 前后端信息交互（jquery.ajax）

[flask 前端 数据交互 你会了么 第25节 falsk 和前端进行数据交互 跟着SKY学编程_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1TK4y1t7XB/?spm_id_from=333.337.search-card.all.click&vd_source=40879351e43fec3245ccef5adf4b126a)

- 下载jquery框架文件 [Download jQuery | jQuery](https://jquery.com/download/)

- html 添加引用 `<script src="{{ url_for('static', filename='js/jquery3.7.1.js') }}"></script>`

  此时Javascript即可通过`$`访问jquery的方法

- 后端`app.py`准备好对应路由的相应方法（如`/getAnswer`）

  其中可以通过flask.request获取ajax发送的请求中等待data：`request.args`，会获得一个字典，正常取值即可

  ```python
  from flask import Flask, render_template, request
  
  @app.route('/getAnswer', methods=['GET', 'POST'])
  def get_answer():
      # 获取ajax请求的参数
      data = request.args
      print(data)
      name = data.get("name","not found")
      return {
          "data": f'please remember {name} forever',
          "success": 0,
      }
  ```

  

- JS通过ajax发送请求

  ```js
  $.ajax({
      url : "/getAnswer",
      data : {name : "Stuart Westmorland", age:NaN},
      success: (result) => {
          if (result.success === 0){
              alert(result.data)
          }else{
              alert('failed, find him')
          }
      }
  })
  ```



## 前端代码解析

#### 为什么新加的聊天泡泡没有换行

似乎长的整数不会被默认换行，测试发现长的整数中间用空格隔开就会在空格处换行了

#### 说话泡泡没有靠边对齐的问题

加上`margin-left: auto`即可

#### 选择聊天历史框

> 创建新聊天：
>
> - 触发条件：用户点击“new chat”、首次聊天
> - 逻辑：新建上下文、新建聊天选择div（data-id=randomint）
> - 清空当前聊天框
> - 创建新历史
> - 添加聊天信息至聊天框
>
> 更换聊天框：
>
> - 清空当前聊天框
> - 读取历史
> - 添加聊天信息至聊天框

#### 无历史聊天时，用户输入信息自动创建新窗口

在发送信息到后端的函数中判断一下是否存在激活的视窗div，若无则创建一个，然后正常执行发送信息的逻辑

#### css无法读取图片的问题

## Ollama

#### generate和chat的区别

generate-单次输出

chat-适合对话（本例应该用这个）

- ```python
  from ollama import chat
  
  conversation_history = [
  {"role": "system", "content": "You are an assistant."},
  {"role": "user", "content": "使用python写一段读取test.txt的代码，尽量精简，只要代码无需介绍"}
  ]
  response = chat(
  model='llama3.2:1b',
  messages=conversation_history,
  options={
  'num_predict': 128,
  'temperature': 0,
  'top_p': 0.9,
  'stop': ['<EOT>'],
  },
  )
  print(response['message']['content'])
  ```



#### 长上下文压缩

[ollama-python上下文管理：长对话场景优化策略-CSDN博客](https://blog.csdn.net/gitblog_00149/article/details/151286586#:~:text=本文将系统讲解ollama-python中的上下文管理机制，提供4种实战优化策略，并通过完整代码示例展示如何在长对话场景中保持模型性能与对话连贯性的平衡。 读完本文后，你将能够： ollama-python通过双重机制实现对话状态的维持： 消息列表,(messages) 和 上下文令牌 (context)。 这两种机制在不同场景下各有优势，需要根据对话长度和复杂度灵活选择。)

常见方法：

- 滑动窗口：保留最近的N轮
- 内容截断：单条消息过长时，截断为固定长度
- 语义压缩：使用**嵌入（Embedding）**技术，将长对话历史压缩为向量表示，通过相似度比较保留关键信息。适合需要保留长期记忆的场景。
- 摘要记忆：定期对对话历史生成摘要，用摘要替代原始历史。适合需要**长期**上下文但可**接受一定信息损失**的场景。

| 优化策略    | 实现复杂度 | 内存占用 | 历史保留     | 适用场景               |
| ----------- | ---------- | -------- | ------------ | ---------------------- |
| 完整历史/无 | ⭐️          | ⭐️⭐️⭐️⭐️     | 100%         | 短对话、关键信息密集型 |
| 滑动窗口    | ⭐️⭐️         | ⭐️⭐️       | 最近N轮      | 闲聊、客服对话         |
| 内容截断    | ⭐️⭐️         | ⭐️⭐️       | 每次部分保留 | 长文本输入、代码讨论   |
| 语义压缩    | ⭐️⭐️⭐️        | ⭐️        | 关键信息     | 知识问答、决策支持     |
| 摘要记忆    | ⭐️⭐️⭐️        | ⭐️        | 抽象保留     | 长时间对话、项目讨论   |

见原网页，学习如何组合以上的策略