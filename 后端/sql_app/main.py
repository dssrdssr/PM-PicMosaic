import os
import io
import pathlib
import cv2
import imageio
import shutil

from scipy import misc
from PIL import Image
from matplotlib import pyplot as plt
from typing import List
from fastapi import applications
from fastapi import Depends, FastAPI, HTTPException,  status
from fastapi import File, UploadFile
from fastapi.responses import FileResponse
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
import fastapi_cdn_host
from . import crud, models, schemas,main_async,mosaic
import pathlib #处理文件路径
from .database import SessionLocal, engine
import base64
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
import zipfile


models.Base.metadata.create_all(bind=engine)
app = FastAPI(docs_url=None,redoc_url=None,title="PM")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
fastapi_cdn_host.patch_docs(app, favicon_url='/static/hospital.svg')


def crop_image(image_path, x1, y1, x2, y2):
    # 打开图片
    img = Image.open(image_path)
    # 裁剪图片
    cropped_img = img.crop((x1, y1, x2, y2))
    # 转换为 RGB 模式（如果需要）
    if cropped_img.mode == 'RGBA':
        cropped_img = cropped_img.convert('RGB')
    # 将图片转换为字节流
    buffered = io.BytesIO()
    cropped_img.save(buffered, format="JPEG")
    # 将字节流转换为base64字符串
    base64_string = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return base64_string


def dict_crop(result_dict,x1, y1):
    if result_dict['all_line_position']==-1:
        return result_dict
    for all_line_position in result_dict['all_line_position']:
        for one_line_all_char_position in all_line_position['one_line_all_char_position']:
            if one_line_all_char_position['characters']!=[]and one_line_all_char_position['result_location']!=[]:
                for result_location in one_line_all_char_position['result_location']:
                    result_location['location']['top']=result_location['location']['top']+y1
                    result_location['location']['left'] = result_location['location']['left'] + x1
    return result_dict
# crop_image('ocr1.png',10,10,200,200)
    # 打开图片
    #img = Image.open(image_path)
    # 裁剪图片
    #cropped_img = img.crop((x, y, x + width, y + height))
    # 显示裁剪后的图片（可选）
    #cropped_img.show()
    # 保存裁剪后的图片
    #cropped_img.save("cropped_image.jpg")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(

        title="PM",
        version="1.0.0",
        summary="这是一个关于敏感信息处理的项目",
        description="您可以提交视频或图片，经过处理后告知您存在敏感信息的位置",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapi



# Dependency
def filetobase64(image_path:str):
    with open(image_path, "rb") as f:
        image_data = f.read()
        base64_string = base64.b64encode(image_data).decode('utf-8')
        return base64_string


def filetoimageurl(image_path:str):
    with open(image_path, "rb") as f:
        image_data = f.read()
        base64_string = base64.b64encode(image_data).decode('utf-8')
        url = "data:image/jpeg;base64," + base64_string
        return url


def path_to_base64_cropping(image_path,x1,y1,x2,y2):
    base64_string=crop_image(image_path, x1, y1, x2, y2)
    return base64_string


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    dbuser = crud.get_user(db, token)
    if not dbuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return dbuser


async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if current_user==None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def mosaic_for_multpic(ID:list[str],location_set:list[list[int]],style:int = 1,mosasize:int =30,current_user: models.User = Depends(get_current_active_user)):
    mosadata= mosaic.MosaData(path=current_user.username,ID=ID,location_set=location_set,style=style,mosasize=mosasize)
    num = mosaic.mul_mosaic(mosadata = mosadata)
    return {"outfolder": mosaic.PATH.joinpath(mosadata.path,'output'),"sucess":num}


#todo
@app.post("/token",tags=["用户管理"],summary="登录用户")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    dbuser = crud.get_user(db, form_data.username)
    if not dbuser:
        raise HTTPException(status_code=400, detail="Incorrect username")
    fpwd=form_data.password
    if not fpwd == dbuser.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    return {"access_token": dbuser.username, "token_type": "bearer","authority":dbuser.authority}


@app.post("/oauth/register", response_model=schemas.User,tags=["用户管理"],summary="注册用户")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="The ID has already been registered")
    path1='userdata/'+user.username+'/input'
    if not os.path.exists(path1):
        os.makedirs(path1)
    path2='userdata/'+user.username+'/output'
    if not os.path.exists(path2):
        os.makedirs(path2)
    return crud.create_user(db=db, user=user)

@app.post("/oauth/admin/register", response_model=schemas.User,tags=["用户管理"],summary="初始管理员")
def create_user(password:str,db: Session = Depends(get_db)):
    user=models.User(username='admin',password=password,authority='1')
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="The ID has already been registered")
    path1='userdata/'+user.username+'/input'
    if not os.path.exists(path1):
        os.makedirs(path1)
    path2='userdata/'+user.username+'/output'
    if not os.path.exists(path2):
        os.makedirs(path2)
    return crud.create_admin_user(db=db, user=user)

@app.post("/oauth/create/admin/register", response_model=schemas.User,tags=["用户管理"],summary="注册管理员用户")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    if current_user.authority!='1':
        raise HTTPException(status_code=401, detail="Unauthorized")
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="The ID has already been registered")
    path1='userdata/'+user.username+'/input'
    if not os.path.exists(path1):
        os.makedirs(path1)
    path2='userdata/'+user.username+'/output'
    if not os.path.exists(path2):
        os.makedirs(path2)
    return crud.create_admin_user(db=db, user=user)


@app.get("/oauth/me",tags=["用户管理"],summary="查看当前用户")
async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user


@app.get("/oauth/", response_model=list[schemas.User],tags=["用户管理"],summary="查看用户列表")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    if current_user.authority=='0':
        raise HTTPException(status_code=401, detail=" Unauthorized")
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.put("/oauth/change/{username}", response_model=schemas.User,tags=["用户管理"],summary="修改密码")
def update_users(username:str,newpassword:str, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    if current_user.authority!='1' and username!=current_user.username:
        raise HTTPException(status_code=401, detail=" Unauthorized")
    newuser=models.User(username=current_user.username,password=newpassword,is_active=current_user.is_active,authority=current_user.authority,pics=current_user.pics)
    users = crud.modify_user(db, newuser)
    return users


@app.put("/oauth/update/{username}", response_model=schemas.User,tags=["用户管理"],summary="更新用户")
def update_users(newuser:schemas.User, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    if current_user.authority=='1':
        users = crud.modify_user(db, newuser)
        return users
    else:
        raise HTTPException(status_code=401, detail=" Unauthorized")


@app.get("/oauth/show/{username}", response_model=schemas.User,tags=["用户管理"],summary="获取用户")


#给管理员查看用户信息的
def read_user(username: str, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    if current_user.authority=='0':
        raise HTTPException(status_code=401, detail=" Unauthorized")
    db_user = crud.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete('/oauth/delete/user/{username}',tags=["用户管理"],summary="删除用户")
async def delete_user(username:str,db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    if username==current_user.username or current_user.authority=='1':
        db_user=crud.get_user(db=db,username=username)
        if not db_user:
            raise HTTPException(status_code=400, detail="No this user")
        else:
            path = pathlib.Path('userdata/'+current_user.username)
            if path.exists():
                shutil.rmtree(path)
            return crud.drop_user(db=db,username=username)
    else:
        raise HTTPException(status_code=401, detail=" Unauthorized")
        
@app.get('/oauth/upload_number/',tags=["文件管理"],summary="获取用户已上传图片数量")
async def download_file(db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    num = crud.get_user_last_pic(db,current_user.username)
    return {"The_last_pic":num}
   
@app.post("/oauth/upload/{username}/",tags=["文件管理"],summary="用户上传")
async def create_upload_file(files: List[UploadFile], db: Session = Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    flag=0
    list1=[]
    path = pathlib.Path('userdata/'+current_user.username+'/input')
    if not path.exists():
        path.mkdir()
    for file in files:
        picname=file.filename
        db_pic = crud.get_user_pic(db=db,username=current_user.username,picname=picname)
        if db_pic:
            flag=1
            list1.append(file.filename)
            res = await file.read()#读取文件内容
            with open(path.joinpath(file.filename), "wb") as f:#按文件名写入文件
                f.write(res)
        else:
            res = await file.read()#读取文件内容
            with open(path.joinpath(file.filename), "wb") as f:#按文件名写入文件
                f.write(res)
            
            pic1=models.Pic(picname=file.filename,owner_id=current_user.username)
            crud.create_user_pic(db=db, pic=pic1)

    if flag==1:
        detail=""
        for i in list1:
            detail=detail+i+" "
        return {"message": detail+" 被覆盖"}
    else:  
        return {"message": "success"}


@app.get('/oauth/download/origin/{username}/',tags=["文件管理"],summary="原始文件下载")
async def download_file(picname:str,db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    path=pathlib.Path('userdata/'+current_user.username+'/input')#文件保存的根目录
    if not path.exists():
        raise HTTPException(status_code=401, detail="No file to download")
    db_file=crud.get_user_pic(db=db,username=current_user.username,picname=picname)#查找文件记录
    if db_file:
        #按文件保存路径找到并发送文件
        return FileResponse(path=path.joinpath(db_file.picname),filename=db_file.picname)
    raise HTTPException(status_code=401, detail="No file to download")
    

@app.get('/oauth/download/{username}/',tags=["文件管理"],summary="打码文件下载")
async def download_file(picname:str,db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    path=pathlib.Path('userdata/'+current_user.username+'/output')#文件保存的根目录
    if not path.exists():
        raise HTTPException(status_code=401, detail="No file to download")
    db_file=crud.get_user_pic(db=db,username=current_user.username,picname=picname)#查找文件记录
    if db_file:
        #按文件保存路径找到并发送文件
        return FileResponse(path=path.joinpath(db_file.picname),filename=db_file.picname)
    raise HTTPException(status_code=401, detail="No file to download")

@app.post('/oauth/mult_download/{username}/',tags=["文件管理"],summary="批量下载打码文件")
async def mult_download(piclist:list[str],db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    path=pathlib.Path('userdata/'+current_user.username+'/output')#文件保存的根目录
    if not path.exists():
        raise HTTPException(status_code=401, detail="No file to download")
    zip_file_name = "pictures.zip"
    with zipfile.ZipFile(zip_file_name, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for picname in piclist:
            db_file=crud.get_user_pic(db=db,username=current_user.username,picname=picname)#查找文件记录
            if db_file:
                zf.write(path.joinpath(picname), arcname=picname)
                #按文件保存路径找到并发送文件
    return FileResponse(path=pathlib.Path(zip_file_name),filename=zip_file_name)


@app.get('/oauth/showall/{username}/',tags=["文件管理"],summary="显示所有图片")
async def download_file(db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    path1=pathlib.Path('userdata/'+current_user.username+'/input')#文件保存的根目录
    path2=pathlib.Path('userdata/'+current_user.username+'/output')#文件保存的根目录
    if not path1.exists():
        raise HTTPException(status_code=401, detail="No file to download")
    if not path2.exists():
        raise HTTPException(status_code=401, detail="No file to download")
    list1=[]
    list2=[]
    db_file=crud.show_pics(db=db,user=current_user)#查找文件记录
    if db_file:
        i = 0
        while i<len(db_file):
            filename=db_file[i]
            list1.append(filetoimageurl(pathlib.Path('userdata/'+current_user.username+'/input/'+filename)))
            pathtemp=pathlib.Path('userdata/'+current_user.username+'/output/'+filename)
            if not pathtemp.exists():
                list2.append(filetoimageurl(pathlib.Path('static/1.png')))
            else:
                list2.append(filetoimageurl(pathlib.Path('userdata/'+current_user.username+'/output/'+filename)))
            i=i+1
        return {"input":list1,"output":list2}
    raise HTTPException(status_code=401, detail="No file to show")


@app.get("/oauth/show/{username}/pics/{picname}", response_model=schemas.Pic,tags=["文件管理"],summary="文件查询")
def read_pic(picname: str,db: Session = Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    db_pic = crud.get_user_pic(db=db,username=current_user.username,picname=picname)
    if db_pic is None:
        raise HTTPException(status_code=404, detail="Pic not found")
    return db_pic


@app.delete('/oauth/delete/{username}/pics/{picname}',tags=["文件管理"],summary="删除文件")
async def delete_file(picname:str,db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    path1=pathlib.Path('userdata/'+current_user.username+'/input')
    if not path1.exists():
        raise HTTPException(status_code=500, detail="Failed to delete this file")
    path2=pathlib.Path('userdata/'+current_user.username+'/output')
    if not path2.exists():
        raise HTTPException(status_code=500, detail="Failed to delete this file")
    db_file=crud.get_user_pic(db=db,username=current_user.username,picname=picname)
    if not db_file:
        raise HTTPException(status_code=400, detail="No this file")
    else:
        path1=path1.joinpath(db_file.picname)#路径从目录移动到目录下的文件
        if path1.exists():
            try:
                path1.unlink()#删除文件
            except:
                raise HTTPException(status_code=500, detail="Failed to delete this file")
        path2=path2.joinpath(db_file.picname)#路径从目录移动到目录下的文件
        if path2.exists():
            try:
                path2.unlink()#删除文件
            except:
                raise HTTPException(status_code=500, detail="Failed to delete this file")
        '''
        path.unlink()#可能需要修改文件夹权限才能删除文件
        linux 系统可以用代码控制，Windows系统需要打开资源管理器手动修改
        '''
    return crud.drop_file(db=db,pic=db_file)

@app.post("/mult_image/base64/words/free",tags=["信息识别"],summary="批量进行图片处理")
async def mult_execute(x1:int=-1,y1:int=-1,x2:int=-1,y2:int=-1,style:int = 1,mosasize:int = 30,piclist:list[str] = [],name:str="",db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    if piclist==[]:
        HTTPException(status_code=401, detail="No file to process")
    for picname in piclist:
        result =await image_word_base64(x1,y1,x2,y2,style,mosasize,picname,name,db,current_user)
        list1 = []
        list2 = []
        list1.append(result['outfolder'])
        list2.append(result['sucess'])
    return {"outfolder": list1,"sucess":list2}

#name是敏感词语库的名称
@app.post("/image/base64/words/free",tags=["信息识别"],summary="免费敏感词库信息识别")
async def image_word_base64(x1:int=-1,y1:int=-1,x2:int=-1,y2:int=-1,style:int = 1,mosasize:int = 30,picname: str="",name:str="",db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    if picname=="":
        raise HTTPException(status_code=400, detail="No this file")  
    word_list=crud.show_words(name=name,user=current_user,db=db)
    if word_list==0:
        word_list=[]
    if name=="":
        word_list=[]
    file=pathlib.Path('userdata/'+current_user.username+'/input/'+picname)
    if x1==-1 and y1==-1:
        if x2==-1 and y2==-1:
            x1=0
            y1=0
            img_pillow = Image.open(file)
            x2 = img_pillow.width  # 图片宽度
            y2 = img_pillow.height     
    base64 = path_to_base64_cropping(file, x1, y1, x2, y2)
    result_dict=await main_async.use_image_base64_word_async(base64,word_list)
    result_dict = dict_crop(result_dict, x1, y1)
    location = []
    temp_list = []
    if result_dict['all_char_location']!=-1:
        for i in result_dict['all_char_location']:
            temp_list=[]
            for j in i['location'].values():
                temp_list.append(j)
            location.append(temp_list)
    result = await mosaic_for_multpic([picname],location,style,mosasize,current_user)
    return {"outfolder": result['outfolder'],"sucess":result['sucess']}


@app.post("/image/base64/words/baidu",tags=["信息识别"],summary="收费敏感词库信息识别")
async def image_word_base64_baidu(x1:int=-1,y1:int=-1,x2:int=-1,y2:int=-1,style:int = 1,mosasize:int = 30,picname: str="",name:str="",db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    if picname=="":
        raise HTTPException(status_code=400, detail="No this file")  
    word_list=crud.show_words(name=name,user=current_user,db=db)
    if word_list==0:
        word_list=[]
    if name=="":
        word_list=[]
    file=pathlib.Path('userdata/'+current_user.username+'/input/'+picname)
    if x1==-1 and y1==-1:
        if x2==-1 and y2==-1:
            x1=0
            y1=0
            img_pillow = Image.open(file)
            x2 = img_pillow.width  # 图片宽度
            y2 = img_pillow.height
    base64=path_to_base64_cropping(file,x1,y1,x2,y2)
    result_dict=await main_async.use_image_base64_word_baidu_async_one(base64, word_list)
    result_dict=dict_crop(result_dict,x1,y1)
    location = []
    temp_list = []
    if result_dict['all_char_location']!=-1:
        for i in result_dict['all_char_location']:
            temp_list=[]
            for j in i['location'].values():
                temp_list.append(j)
            location.append(temp_list)
    result = await mosaic_for_multpic([picname],location,style,mosasize,current_user)
    return {"outfolder": result['outfolder'],"sucess":result['sucess']}


#临时敏感词
@app.post("/image/base64/word/free",tags=["信息识别"],summary="免费临时敏感词信息识别")
async def image_word_base64(x1:int=-1,y1:int=-1,x2:int=-1,y2:int=-1,style:int = 1,mosasize:int = 30,picname: str="",name:str="",db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    if picname=="":
        raise HTTPException(status_code=400, detail="No this file")
    word_list=[name]
    file=pathlib.Path('userdata/'+current_user.username+'/input/'+picname)
    if x1==-1 and y1==-1:
        if x2==-1 and y2==-1:
            x1=0
            y1=0
            img_pillow = Image.open(file)
            x2 = img_pillow.width  # 图片宽度
            y2 = img_pillow.height
    base64 = path_to_base64_cropping(file, x1, y1, x2, y2)
    result_dict=await main_async.use_image_base64_word_async(base64,word_list)
    location = []
    temp_list = []
    if result_dict['all_char_location']!=-1:
        for i in result_dict['all_char_location']:
            temp_list=[]
            for j in i['location'].values():
                temp_list.append(j)
            location.append(temp_list)
    result = await mosaic_for_multpic([picname],location,style,mosasize,current_user)
    return {"outfolder": result['outfolder'],"sucess":result['sucess']}


@app.post("/image/base64/word/baidu",tags=["信息识别"],summary="收费临时敏感词信息识别")
async def image_word_base64_baidu(x1:int=-1,y1:int=-1,x2:int=-1,y2:int=-1,style:int = 1,mosasize:int = 30,picname: str="",name:str="",db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    if picname=="":
        raise HTTPException(status_code=400, detail="No this file")
    word_list=[name]
    file=pathlib.Path('userdata/'+current_user.username+'/input/'+picname)
    if x1==-1 and y1==-1:
        if x2==-1 and y2==-1:
            x1=0
            y1=0
            img_pillow = Image.open(file)
            x2 = img_pillow.width  # 图片宽度
            y2 = img_pillow.height
    base64=path_to_base64_cropping(file,x1,y1,x2,y2)
    result_dict=await main_async.use_image_base64_word_baidu_async_one(base64, word_list)
    result_dict=dict_crop(result_dict,x1,y1)
    location = []
    temp_list = []
    if result_dict['all_char_location']!=-1:
        for i in result_dict['all_char_location']:
            temp_list=[]
            for j in i['location'].values():
                temp_list.append(j)
            location.append(temp_list)
    result = await mosaic_for_multpic([picname],location,style,mosasize,current_user)
    return {"outfolder": result['outfolder'],"sucess":result['sucess']}


#敏感词库的crud
@app.post("/oauth/register/{username}/words", response_model=schemas.Word,tags=["敏感词库"],summary="创建词库")
def create_words(name:str, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    db_words = crud.get_words(db, name=name,user=current_user)
    if db_words:
        raise HTTPException(status_code=400, detail="The 词库 has already been registered")
    return crud.create_words(db=db, name=name,user=current_user)


@app.post("/oauth/register/{username}/words/word", response_model=schemas.Word,tags=["敏感词库"],summary="添加敏感词")
def create_word(name:str, word:str,db: Session = Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    db_words = crud.get_words(db, name=name,user=current_user)
    if db_words:
        db_word = crud.get_word(db, name=name,word=word,user=current_user)
        if db_word:
            raise HTTPException(status_code=400, detail="The 敏感词 has already been registered")
        return crud.create_word(db=db, name=name,user=current_user,word=word)
    else:
        raise HTTPException(status_code=400, detail="没有该词库")


@app.get("/oauth/show/{username}/words",tags=["敏感词库"],summary="显示已有敏感词库")
async def read_words(current_user: models.User = Depends(get_current_active_user),db: Session = Depends(get_db)):
    word_list=crud.show_diction(user=current_user,db=db)
    if word_list==0:
        raise HTTPException(status_code=400, detail="No this 词库")
    return word_list


@app.get("/oauth/show/{username}/word",tags=["敏感词库"],summary="显示已有敏感词")
async def read_word(name:str,current_user: models.User = Depends(get_current_active_user),db: Session = Depends(get_db)):
    word_list=crud.show_words(name=name,user=current_user,db=db)
    if word_list==0:
        raise HTTPException(status_code=400, detail="No this 词库")
    return word_list


@app.delete('/oauth/delete/{username}/words',tags=["敏感词库"],summary="删除敏感词库")
async def delete_words(name:str,db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    db_words=crud.get_words(db, name=name,user=current_user)
    if db_words:
        return crud.drop_words(db=db,name=name,user=current_user)
    else:
        raise HTTPException(status_code=400, detail="No 这个词库")
    

@app.delete('/oauth/delete/{username}/words/word',tags=["敏感词库"],summary="删除敏感词")
async def delete_word(name:str,word:str,db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    db_words=crud.get_words(db, name=name,user=current_user)
    if db_words:
        db_word = crud.get_word(db, name=name,word=word,user=current_user)
        if db_word:
            return crud.drop_word(db=db,name=name,user=current_user,word=word)
        else:
            raise HTTPException(status_code=400, detail="No 这个敏感词")
    else:
        raise HTTPException(status_code=400, detail="No 这个词库")


#后端显示文件
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
    openapi_url=app.openapi_url,
    title=app.title+" - 后端接口文档",
    oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
    swagger_js_url="https://cdn.staticfile.net/swagger-ui/5.11.0/swagger-ui-bundle.min.js",
    swagger_css_url="https://cdn.staticfile.net/swagger-ui/5.11.0/swagger-ui.min.css",

 )
@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

@app.get("/")
async def root():
    return {"message": "Hello World"}
