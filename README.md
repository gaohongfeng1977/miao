# miao
this is about app for taking care of  cats or dogs health, with a camer installed at home .

# program 
程序配置：

1.视频存储目录管理
/datasource/
/datasource/video	存储要分析的视频片段
/datasource/image	存储要分析的图片

/processedsource/vedio	处理完成的视频存储
/processedsource/image	处理完成的图片

2.流程

2.1 多模态模型——>智谱GLM 
2.1.1Main主程序：
2.1.1.1 初始化大模型
2.1.1.2 启动for循环检测，检测/datasource/video,如果有视频文件，就进行解析。生成描述（英文）
2.1.1.3调用接口：调用
2.1.1.4调用接口：将描述，描述embedding，视频路径，写入zilliz，便于后面查询相似描述
2.1.1.5调用接口：将处理好的视频mv到/processedsource/vedio
2.1.1.6调用接口：zhipuai接口，生成中文风格化文本
		 参数：
			filename:视频文件名称
			describe:flamingo的文件描述信息（英文）

			return（string）：风格化文本
2.1.1.7将返回内容写入数据库mysql






