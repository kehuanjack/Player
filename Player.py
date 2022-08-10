import os  # 主要用于执行终端命令
import re  # 匹配文本
import pygame  # 主要用于音乐播放控制
import requests  # 用于爬取资源
import pyperclip  # 用于复制
import tkinter.messagebox as mex  # 用于信息提示
from tkinter import *  # UI框架设计
from PIL import Image, ImageTk
from pydub import AudioSegment as AS  # 需配合安装依赖ffmpeg，用于音乐格式转换


# 爬取歌曲数据
def music1(name,pages): 
    url = f'{api}&types=search&count={count}&source={source}&name={name}&pages={pages}'
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
               'cookie':'UM_distinctid=18040c51f383fe-0c21dd6a211e89-3e604809-144000-18040c51f392a7'}
    list_all = eval(requests.get(url=url,headers=headers).text)
    mid_list = []
    music_title_list = []
    music_album_name = []
    music_singer_name = []
    for index, for_dict in enumerate(list_all):
        # 专辑名
        album_name = for_dict["album"]
        music_album_name.append(album_name)
        # new url
        mid_list.append(for_dict["id"])
        # 歌名
        music_title = for_dict["name"]
        music_title_list.append(music_title)
        # 歌手
        singer_name = for_dict["artist"][0]
        music_singer_name.append(singer_name)
    return mid_list, music_title_list, music_singer_name, music_album_name

# 爬取歌单数据
def playlist():
    url = f"{api}&types=playlist&source=netease&id={playlist_id}"
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                   'cookie':'UM_distinctid=18040c51f383fe-0c21dd6a211e89-3e604809-144000-18040c51f392a7'}
    list_all = eval(requests.get(url=url,headers=headers).text.replace('null','0').replace('false','0').replace('true','0'))['playlist']['tracks']
    mid_list = []
    music_title_list = []
    music_album_name = []
    music_singer_name = []
    
    for index, for_dict in enumerate(list_all):
        # 专辑名
        album_name = for_dict['al']['name']
        music_album_name.append(album_name)
        # new url
        mid_list.append(for_dict["id"])
        # 歌名
        music_title = for_dict["name"]
        music_title_list.append(music_title)
        # 歌手
        singer_name = for_dict['ar'][0]['name']
        music_singer_name.append(singer_name)
    return mid_list, music_title_list, music_singer_name, music_album_name


# 获取音乐url
def get_url(song_id):  
    t = requests.get(f'{api}&types=url&id={song_id}&source={source}')
    if 'http' not in t.text:
        mex.showinfo("提示","无链接，换首歌试试")
    else:
        song_url = list(re.findall(r'(http.*?(.mp3|.m4a|.aac|.wav))',t.text)[0])[0].replace('\\','')
        gs(song_url)
        return song_url

# 链接格式判断
def gs(song_url): 
    global music_gs
    if 'mp3' in song_url:music_gs = 'mp3'
    if 'm4a' in song_url:music_gs = 'm4a'       
    if 'aac' in song_url:music_gs = 'aac'
    if 'wav' in song_url:music_gs = 'wav'

# 打印音乐列表事件，'ev=None'与绑定回车键有关,不可省略掉
def show(ev=None):  
    global my_data
    global name_num
    
    try:
        music_dir()
        name_num = str(e3.get())
        e2.delete(0.0, END)
        e2.insert(END, '\t  歌曲\t\t\t\t 歌手\t\t\t 专辑\n')
        my_data = music1(name=str(e1.get()),pages=name_num)
        long = len(my_data[0])
        for i in range(0,long):
            my_music_list = '%d'%(i+1) + '\t' + my_data[1][i] + '\t\t\t\t' + my_data[2][i] + '\t\t\t' + my_data[3][i] + '\n'
            e2.insert(END, my_music_list)
    except:
        mex.showinfo("提示","无填写页数")

# 打印歌单
def my_slist():  
    global my_data
    global name_num

    try:
        music_dir()
        v2.set('netease')
        name_num = str(e3.get())
        e2.delete(0.0, END)
        e2.insert(END, '\t  歌曲\t\t\t\t 歌手\t\t\t 专辑\n')
        my_data = playlist()
        long = len(my_data[0])
        for i in range(0,long):
            my_music_list = '%d'%(i+1) + '\t' + my_data[1][i] + '\t\t\t\t' + my_data[2][i] + '\t\t\t' + my_data[3][i] + '\n'
            e2.insert(END, my_music_list)
    except:
        mex.showinfo("提示","请检查歌单id")


# 解析url
def analyze_url(): 
    global music_url
    global response
    global name_num
    global path
    
    try:
        response = None
        name_num = str(e3.get())
        music_url = get_url(my_data[0][int(name_num)-1])
        if music_url != None:
            path = r'{}\{}_{}.{}'.format(save_dir,my_data[1][int(name_num)-1],my_data[0][int(name_num)-1],music_gs)  # 音乐保存路径
            if not os.path.exists(path):
                response = requests.get(music_url).content  # 将音乐链接转换成二进制流
                with open(path, 'wb') as f:
                    f.write(response)
                    f.flush()
                gs_change()
    except:
        music_url = None
        mex.showinfo("提示","无链接或无填写歌序")
    
# 下载并播放事件
def download_play(): 
    global flag
    analyze_url()
    if music_url != None and music_gs == "mp3":
        pygame.mixer.init()
        pygame.mixer.music.unload()
        songload()
        play()
        mex.showinfo("提示",r"正在播放：{}_{}".format(my_data[1][int(name_num)-1],my_data[0][int(name_num)-1]))
        flag = True


# 下一首播放事件
def next_play():  
    global flag
    analyze_url()
    if music_url != None and music_gs == "mp3":
        if flag == False:
            songload()
            play()
            mex.showinfo("提示",r"正在播放：{}_{}".format(my_data[1][int(name_num)-1],my_data[0][int(name_num)-1]))
            flag = True
        else:
            pygame.mixer.music.queue(path)
            mex.showinfo("提示",r"下首将播放：{}_{}".format(my_data[1][int(name_num)-1],my_data[0][int(name_num)-1]))


# 载入歌曲事件        
def songload(): 
    pygame.mixer.init()
    pygame.mixer.music.load(path)   

# 播放事件
def play(): 
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(value)

# 音乐格式转换 -> mp3 
def gs_change(): 
    global path
    global music_gs
    if music_gs != 'mp3':
        inp = path
        oup = path.replace(music_gs,'mp3')
        try:
            os.popen(r'ffmpeg -i {} -acodec libmp3lame {}'.format(inp,oup)).read()
            a = True
        except:
            a = False
            mex.showinfo("提示","没有安装配置ffmpeg")
            
        if a == True:
            os.remove(path)
            path = path.replace(music_gs,'mp3')

# 复制链接事件
def copy_url(): 
    try:
        pyperclip.copy(music_url)
    except:
        mex.showinfo("提示","无链接")

# 循环播放事件
def cycle_play():
    try:
        num = str(e3.get())
        pygame.mixer.music.play(loops=int(num))
    except:
        mex.showinfo("提示","无链接或无填写循环次数")

# 暂停播放事件
def pause_button(): 
    global pause1
    if pause1 == 'pause':
        pause1 = 'unpause'
        pygame.mixer.music.unpause()
    elif pause1 == 'unpause':
        pause1 = 'pause'  
        pygame.mixer.music.pause()

# 音量控制事件
def play_void(v):
    if pygame.mixer.music.get_busy() != False: 
        pygame.mixer.music.set_volume(float(v))

# 音源切换事件
def chose_source():
    global source
    source = v2.get()

# api切换事件
def change_api():
    global api
    if api == first_api:
        api = second_api
        mex.showinfo("提示","second_api")
    elif api == second_api:
        api = first_api
        mex.showinfo("提示","first_api")

# 文本操作
def music_dir():
    global save_dir
    global text
    global count
    global playlist_id
    
    with open(r'.\setting.txt','r',encoding='utf-8')as f:
        all_text = f.read()
        
    text = re.findall(r":\"(.*?)\";",all_text)
    save_dir = text[0]
    count = text[1]  # 搜索的歌曲数
    playlist_id = text[5]
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

if __name__ == "__main__":
    # 设置初值
    global value
    global pause1
    global flag

    first_txt = '''
            参数设置：（By:科幻木影）
                Save_dir:".\music";
                Count:"50";
                First_source:"qq";
                First_api:"https://fm.liuzhijin.cn/api.php?";
                Second_api:"https://api.zhuolin.wang/api.php?";
                Playlist_id:"3778678";
                background:"#CA0316";
                foreground:"white";
                activebackground:"red";
                activeforeground:"white";
                title:"音乐播放器";
                
                '''
    
    # 判断文件并创建
    if not os.path.exists(r'.\setting.txt'):
        with open(r'.\setting.txt','w',encoding='utf-8')as f:
            f.write(first_txt)

    try:      
        music_dir()
        first_api = text[3]
        second_api = text[4]
        api = first_api
        source = text[2]
        bg = text[6]
        fg = text[7]
        abg = text[8]
        afg = text[9]
        title = text[10]
    except:
        os._exit(0)
    
    source_data = [(1,'kugou','酷狗'),(2,'kuwo','酷我'),(3,'qq','QQ'),

                   (4,'netease','网易云')]
    flag = False
    music_url = None
    value = 0.50 # 音量初始值
    pause1 = 'unpause'  # 暂停播放初值标记
    pygame.mixer.init()

    # 设计窗口与组件事件
    app = Tk()
    app.geometry('900x260')  # 窗口大小
    app.title(title)
    app.resizable(False,False)  # 禁止窗口拉伸
    
    Label(app, text="请输入歌名/歌手：").grid(row=1, column=0)

    v1 = StringVar()
    e1 = Entry(app, textvariable=v1,)
    e1.grid(row=1, column=1)
    e1.bind("<Return>",show)  # 将输入框与回车键绑定
    
    B1 = Button(app, text="搜索", background=bg, foreground=fg, activebackground=abg, activeforeground=afg, width=10, command=show)
    B1.grid(row=1, column=2, padx=5)
    
    B4 = Button(app, text="复制链接", background=bg, foreground=fg, activebackground=abg, activeforeground=afg, width=10, command=copy_url)
    B4.grid(row=1, column=3, padx=5)

    # 音量条
    s = Scale(app, from_=0, to=1, orient=HORIZONTAL, length=80, showvalue=1,tickinterval=0, resolution=0.05, command=play_void)
    s.set(0.5)
    s.grid(row=1,column=4,padx=5)

    # 音源
    v2 = StringVar()
    v2.set(source) # 默认音源
    for num,sou,txt in source_data:
        b = Radiobutton(app,text=txt,variable=v2,value=sou,command=chose_source)
        ro=1
        if num >= 7:
            ro=2
            num=num-6
        b.grid(row=ro,column=num+4)
    
    e2 = Text(app, font=('华文新魏', 11)) # 字体设置
    e2.place(relx=0.03, rely=0.25, relwidth=0.938, relheight=0.5)

    Label(app, text="页数/歌序/循环次数：").grid(row=3, column=0, padx=10, pady=180)

    v3 = StringVar()
    e3 = Entry(app, textvariable=v3)
    e3.grid(row=3, column=1)
    e3.insert(END,'1')
    
    B5 = Button(app, text="下载播放", background=bg, foreground=fg, activebackground=abg, activeforeground=afg, width=10, command=download_play)
    B5.grid(row=3, column=2)
    
    B6 = Button(app, text="循环播放", background=bg, foreground=fg, activebackground=abg, activeforeground=afg, width=10, command=cycle_play)
    B6.grid(row=3, column=3)
    
    B7 = Button(app, text="下首播放", background=bg, foreground=fg, activebackground=abg, activeforeground=afg, width=10, command=next_play)
    B7.grid(row=3, column=4)
    
    B8 = Button(app, text="暂停播放", background=bg, foreground=fg, activebackground=abg, activeforeground=afg, width=10, command=pause_button)
    B8.grid(row=3, column=5)

    B9 = Button(app, text="切换API", background=bg, foreground=fg, activebackground=abg, activeforeground=afg, width=10, command=change_api)
    B9.grid(row=3, column=6, padx=10)

    B10 = Button(app, text="我的歌单", background=bg, foreground=fg, activebackground=abg, activeforeground=afg, width=10, command=my_slist)
    B10.grid(row=3, column=7)

    mainloop()

