# 遍历文件夹工具（将代码汇总至同一文件夹）
import os
from pathlib import Path
# 欲遍历的文件目录
workPath = "C:\\Users\\q1576\\Desktop\dlib-19.24"
# 欲保存的文件位置
totalSourceFile  = open("d:\\source.txt",'a+',encoding="utf-8")
def getCodeSource(filesdir):
    for filename in os.listdir(filesdir):
        # 合并文件名和路径
        fileBasename = filename
        filename = os.path.join(filesdir,filename)

        if Path(filename).is_dir():
            # 若为目录，递归寻找
            getCodeSource(filename)
        else:
            # 若为文件，判断是否为需要的代码文件cpp/py/h
            if filename.find('.cpp')>0 or filename.find('.py') or filename.find('.h')>0:
                if filename.find('.html')<0:
                    # 排除html文件
                    print(filename)
                    sourcefile = open(filename,encoding="utf-8")
                    # 文件名
                    totalSourceFile.write('\n'+'文件名:'+fileBasename+'文件名'+'\n')
                    # 文件内容
                    totalSourceFile.write(sourcefile.read())
                    sourcefile.close()
    return 
getCodeSource(workPath)



# 测试部分
# 获取当前工作目录
# os.path.basename(Path.cwd())
# print("Your path is : " + str(Path.cwd().parents[0]))
# # 获取第一个斜杠后的内容
# print(os.path.basename(Path.cwd()))
# # 获取目录名加文件名的元组
# print(os.path.split(Path.cwd()))
# # os.sep 目录分隔符
# #返回字节数
# print(os.path.getsize(Path.cwd())/1024)

# 打开一个文件



