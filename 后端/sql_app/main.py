import pathlib
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
models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url=None,redoc_url=None,title="PM")

fastapi_cdn_host.patch_docs(app, favicon_url='/static/hospital.svg')

def crop_image(image_path, x, y, width, height):
    # 打开图片
    img = Image.open(image_path)
    # 裁剪图片
    cropped_img = img.crop((x, y, x + width, y + height))
    # 显示裁剪后的图片（可选）
    cropped_img.show()
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

#todo
@app.post("/token",tags=["用户管理"],summary="登录用户")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    dbuser = crud.get_user(db, form_data.username)
    if not dbuser:
        raise HTTPException(status_code=400, detail="Incorrect username")
    fpwd=form_data.password
    if not fpwd == dbuser.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    return {"access_token": dbuser.uname, "token_type": "bearer"}


@app.post("/oauth/register", response_model=schemas.User,tags=["用户管理"],summary="注册用户")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, uname=user.uname)
    if db_user:
        raise HTTPException(status_code=400, detail="The ID has already been registered")
    return crud.create_user(db=db, user=user)


@app.get("/oauth/me",tags=["用户管理"],summary="查看当前用户")
async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

@app.get("/oauth/", response_model=list[schemas.User],tags=["用户管理"],summary="查看用户列表")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    if current_user.authority=='0':
        raise HTTPException(status_code=401, detail=" Unauthorized")
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.put("/oauth/change/{uname}", response_model=schemas.User,tags=["用户管理"],summary="修改密码")
def update_users(newpassword:str, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    newuser=models.User(uname=current_user.uname,password=newpassword,is_active=current_user.is_active,authority=current_user.authority,pics=current_user.pics)
    users = crud.modify_user(db, newuser)
    return users


@app.put("/oauth/update/{uname}", response_model=schemas.User,tags=["用户管理"],summary="更新用户")
def update_users(newuser:schemas.User, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    if current_user.authority=='1':
        users = crud.modify_user(db, newuser)
        return users
    else:
        raise HTTPException(status_code=401, detail=" Unauthorized")

@app.get("/oauth/show/{uname}", response_model=schemas.User,tags=["用户管理"],summary="获取用户")
#给管理员查看用户信息的
def read_user(uname: str, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    if current_user.authority=='0':
        raise HTTPException(status_code=401, detail=" Unauthorized")
    db_user = crud.get_user(db, uname=uname)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete('/oauth/delete/user/{uname}',tags=["用户管理"],summary="删除用户")
async def delete_user(uname:str,db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    if uname==current_user.uname or current_user.authority=='1':
        db_user=crud.get_user(db=db,uname=uname)
        if not db_user:
            raise HTTPException(status_code=400, detail="No this user")
        else:
            return crud.drop_user(db=db,uname=uname)
    else:
        raise HTTPException(status_code=401, detail=" Unauthorized")
        
@app.post("/opencv/",tags=["图片处理"],summary="调用opencv打码处理批量图片")
async def mosaic_for_multpic(mosadata:mosaic.MosaData):
    num = mosaic.mul_mosaic(mosadata = mosadata)
    return {"outfolder": mosaic.PATH +mosadata.path+'\\output',"sucess":num}

@app.post("/oauth/upload/{uname}/",tags=["文件管理"],summary="用户上传")
async def create_upload_file(files: List[UploadFile], db: Session = Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    flag=0
    list1=[]
    path = pathlib.Path('userdata/'+current_user.uname)
    if not path.exists():
        path.mkdir()
    for file in files:
        picname=file.filename
        db_pic = crud.get_user_pic(db=db,uname=current_user.uname,picname=picname)
        if db_pic:
            flag=1
            list1.append(file.filename)
        else:
            res = await file.read()#读取文件内容
            with open(path.joinpath(file.filename), "wb") as f:#按文件名写入文件
                f.write(res)
            
            pic1=models.Pic(picname=file.filename,owner_id=current_user.uname)
            crud.create_user_pic(db=db, pic=pic1)

    if flag==1:
        detail=""
        for i in list1:
            detail=detail+i+" "
        return {"message": "fail"}
    else:  
        return {"message": "success"}

@app.get('/oauth/download/{uname}/',tags=["文件管理"],summary="文件下载")
async def download_file(picname:str,db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    path=pathlib.Path('userdata/'+current_user.uname)#文件保存的根目录
    db_file=crud.get_user_pic(db=db,uname=current_user.uname,picname=picname)#查找文件记录
    if db_file:
        #按文件保存路径找到并发送文件
        return FileResponse(path=path.joinpath(db_file.picname),filename=db_file.picname)


@app.get("/oauth/show/{uname}/pics/{picname}", response_model=schemas.Pic,tags=["文件管理"],summary="文件查询")
def read_pic(picname: str,db: Session = Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    db_pic = crud.get_user_pic(db=db,uname=current_user.uname,picname=picname)
    if db_pic is None:
        raise HTTPException(status_code=404, detail="Pic not found")
    return db_pic

@app.delete('/oauth/delete/{uname}/pics/{picname}',tags=["文件管理"],summary="删除文件")
async def delete_file(picname:str,db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    path=pathlib.Path('userdata/'+current_user.uname)
    db_file=crud.get_user_pic(db=db,uname=current_user.uname,picname=picname)
    if not db_file:
        raise HTTPException(status_code=400, detail="No this file")
    else:
        path=path.joinpath(db_file.picname)#路径从目录移动到目录下的文件
        print(path)
        if path.exists():
            try:
                path.unlink()#删除文件
            except:
                raise HTTPException(status_code=500, detail="Failed to delete this file")
        '''
        path.unlink()#可能需要修改文件夹权限才能删除文件
        linux 系统可以用代码控制，Windows系统需要打开资源管理器手动修改
        '''
    return crud.drop_file(db=db,pic=db_file)

#name是敏感词语库的名称
@app.post("/image/base64/words/free",tags=["信息识别"],summary="敏感词库信息识别1")
async def image_word_base64(picname: str,name:str="",db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    word_list=crud.show_words(name=name,user=current_user,db=db)
    if word_list==0:
        word_list=[]
    if name=="":
        word_list=[]
    file=pathlib.Path('userdata/'+current_user.username+'/'+picname)
    base64=filetobase64(file)
    result_dict=await main_async.use_image_base64_word_async(base64,word_list)
    return {"len_words_result": result_dict['len_words_result'],
            "all_line_position":result_dict['all_line_position'],
            "all_char_location":result_dict['all_char_location'],}


@app.post("/image/url/words/free",tags=["信息识别"],summary="敏感词库信息识别2")
async def image_word_url(picname: str,name:str="",db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    word_list=crud.show_words(name=name,user=current_user,db=db)
    if word_list==0:
        word_list=[]
    file=pathlib.Path('userdata/'+current_user.username+'/'+picname)
    image_url=filetoimageurl(file)
    result_dict=await main_async.use_image_url_word_async(image_url,word_list)
    return {"len_words_result": result_dict['len_words_result'],
            "all_line_position":result_dict['all_line_position'],
            "all_char_location":result_dict['all_char_location'],}


@app.post("/image/base64/words/baidu",tags=["信息识别"],summary="敏感词库信息识别3")
async def image_word_base64_baidu(picname: str,name:str="",db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    word_list=crud.show_words(name=name,user=current_user,db=db)
    if word_list==0:
        word_list=[]
    if name=="":
        word_list=[]
    file=pathlib.Path('userdata/'+current_user.username+'/'+picname)
    base64=filetobase64(file)
    result_dict=await main_async.use_image_base64_word_baidu_async_one(base64, word_list)
    return {"len_words_result": result_dict['len_words_result'],
            "all_line_position":result_dict['all_line_position'],
            "all_char_location":result_dict['all_char_location'],}


@app.post("/image/url/words/baidu",tags=["信息识别"],summary="敏感词库信息识别4")
async def image_word_url_baidu(picname: str,name:str="",db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    word_list=crud.show_words(name=name,user=current_user,db=db)
    if word_list==0:
        word_list=[]
    file=pathlib.Path('userdata/'+current_user.username+'/'+picname)
    image_url=filetoimageurl(file)
    result_dict=await main_async.use_image_url_word_baidu_async_one(image_url, word_list)
    return {"len_words_result": result_dict['len_words_result'],
            "all_line_position":result_dict['all_line_position'],
            "all_char_location":result_dict['all_char_location'], }


@app.post("/image/base64/word/free",tags=["信息识别"],summary="敏感词信息识别1")
async def image_word_base64(picname: str,name:str="",db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    word_list=[name]
    file=pathlib.Path('userdata/'+current_user.username+'/'+picname)
    base64=filetobase64(file)
    result_dict=await main_async.use_image_base64_word_async(base64,word_list)
    return {"len_words_result": result_dict['len_words_result'],
            "all_line_position":result_dict['all_line_position'],
            "all_char_location":result_dict['all_char_location'],}


@app.post("/image/url/word/free",tags=["信息识别"],summary="敏感词信息识别2")
async def image_word_url(picname: str,name:str="",db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    word_list=[name]
    file=pathlib.Path('userdata/'+current_user.username+'/'+picname)
    image_url=filetoimageurl(file)
    result_dict=await main_async.use_image_url_word_async(image_url,word_list)
    return {"len_words_result": result_dict['len_words_result'],
            "all_line_position":result_dict['all_line_position'],
            "all_char_location":result_dict['all_char_location'],}


@app.post("/image/base64/word/baidu",tags=["信息识别"],summary="敏感词信息识别3")
async def image_word_base64_baidu(picname: str,name:str="",db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    word_list=[name]
    file=pathlib.Path('userdata/'+current_user.username+'/'+picname)
    base64=filetobase64(file)
    result_dict=await main_async.use_image_base64_word_baidu_async_one(base64, word_list)
    return {"len_words_result": result_dict['len_words_result'],
            "all_line_position":result_dict['all_line_position'],
            "all_char_location":result_dict['all_char_location'],}


@app.post("/image/url/word/baidu",tags=["信息识别"],summary="敏感词信息识别4")
async def image_word_url_baidu(picname: str,name:str="",db:Session=Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    word_list=[name]
    file=pathlib.Path('userdata/'+current_user.username+'/'+picname)
    image_url=filetoimageurl(file)
    result_dict=await main_async.use_image_url_word_baidu_async_one(image_url, word_list)
    return {"len_words_result": result_dict['len_words_result'],
            "all_line_position":result_dict['all_line_position'],
            "all_char_location":result_dict['all_char_location'], }


#敏感词库的
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

@app.get("/oauth/show/{username}/words",tags=["敏感词库"],summary="显示已有敏感词")
async def read_words(name:str,current_user: models.User = Depends(get_current_active_user),db: Session = Depends(get_db)):
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
