import os
from time import strftime

import JianshuResearchTools as jrt
from tqdm import tqdm

from data_getter import (GetArticleData, GetUserAllArticlesNameAndUrl,
                         GetUserData)
from db_config import (ArticlesData, CommentsData, UserData, articles_db,
                       comments_db, user_db)
from print_with_color import *


def process_filename(filename):  # 替换操作系统禁止作为文件名的字符
    ban_words = ["\\", "/", ":", "*", "?", "<", ">", "|"]
    for word in ban_words:
        filename = filename.replace(word, "_")
    return filename

def GetArticleAllComments(article_id):
    result = []
    page = 1
    
    while True:
        page_data = jrt.article.GetArticleCommentsData(article_id, page=page)
        if page_data != []:
            result = result + page_data
            page += 1
        else:
            break
    return result

def AddDataToDatabase(table_obj, data):
    table_obj.create(**data)

print("简书用户数据存档工具")

while True:
    choice = input("请选择操作：\n1. 存档用户数据\n2. 存档用户文章数据\n3. 存档用户文章内容\n>>>")
    if choice not in ["1", "2", "3"]:
        print_red("输入错误，请检查")
    else:
        break

while True:
    user_url = input("请输入用户主页 Url：")
    try:
        jrt.assert_funcs.AssertUserUrl(user_url)
    except jrt.exceptions.InputError:
        print_red("您输入的不是有效的简书用户主页 Url，请重新输入")
    else:
        break

print("正在校验用户账号状态")
try:
    jrt.assert_funcs.AssertUserStatusNormal(user_url)
except jrt.exceptions.ResourceError:
    print_red("该用户账号状态异常，无法存档")
    exit()
else:
    print_green("用户账号状态正常")

print("正在创建存档目录")
try:
    os.mkdir("用户数据")
except FileExistsError:
    pass
os.chdir("用户数据")
user_name = jrt.user.GetUserName(user_url)
now_time = strftime(r"%Y%m%d-%H%M%S")
folder_name = user_name + "-" + now_time
os.mkdir(folder_name)
os.chdir(folder_name)
print_green("存档目录创建成功")
print("当前存档目录：{}".format(os.getcwd()))


if choice == "1":
    print("正在连接数据库")
    user_db.create_tables([UserData])
    print_green("连接数据库成功")
    print("开始获取用户数据")
    user_data = GetUserData(user_url)
    AddDataToDatabase(UserData, user_data)
    print_green("数据存档成功")
elif choice == "2":
    print("正在连接数据库")
    articles_db.create_tables([ArticlesData])
    print_green("连接数据库成功")
    print("开始获取文章数据")
    for name, url in tqdm(GetUserAllArticlesNameAndUrl(user_url).items(), unit="article"):
        article_data = GetArticleData(url)
        AddDataToDatabase(ArticlesData, article_data)
    print_green("数据存档成功")
elif choice == "3":
    print_yellow("风险警示：\n未经授权转载、改编他人文章或将其用于商业用途可能构成侵权，将面临法律风险")
    if input("是否继续？(y/n)\n>>>") != "y":
        exit()
    while True:
        format_choice = input("请选择保存格式：\n1. 纯文本\n2. Html\n>>>")
        if format_choice not in ["1", "2"]:
            print_red("输入错误，请检查")
        else:
            break
    while True:
        comment_choice = input("是否包含评论内容？\n1. 是\n2. 否\n>>>")
        if comment_choice not in ["1", "2"]:
            print_red("输入错误，请检查")
        else:
            print("正在连接评论数据库")
            comments_db.create_tables([CommentsData])
            print_green("连接数据库成功")
            break
        
    print("正在获取文章列表")
    articles_name_and_url = GetUserAllArticlesNameAndUrl(user_url)
    print("获取完成，该用户共有 {} 篇文章".format(len(articles_name_and_url)))
    os.mkdir("文章内容")
    os.chdir("文章内容")
    print("开始获取文章内容")
    if format_choice == "1":
        os.mkdir("纯文本")
        os.chdir("纯文本")
        for name, url in tqdm(articles_name_and_url.items(), unit="article"):
            filename = name + "-" + now_time + ".txt"
            article_content = jrt.article.GetArticleText(url)
            with open(process_filename(filename), "w", encoding="utf-8") as file:
                file.write(article_content)
    elif format_choice == "2":
        os.mkdir("Html")
        os.chdir("Html")
        for name, url in tqdm(articles_name_and_url.items(), unit="article"):
            filename = name + "-" + now_time + ".html"
            article_content = jrt.article.GetArticleHtml(url)
            with open(process_filename(filename), "w", encoding="utf-8") as file:
                file.write(article_content)
    
    if comment_choice == "1":
        print("开始获取评论内容")
        os.chdir("..")
        for name, url in tqdm(articles_name_and_url.items(), unit="article"):
            comments_data = GetArticleAllComments(jrt.convert.ArticleUrlToArticleId(url))
            for comment in comments_data:
                for sub_comment in comment["sub_comments"]:  # 处理子评论
                    sub_comment["is_sub_comment"] = True
                    sub_comment["article_name"] = name
                    sub_comment["article_url"] = url
                    sub_comment["uid"] = sub_comment["user"]["uid"]
                    sub_comment["user_name"] = sub_comment["user"]["name"]
                    sub_comment["uslug"] = sub_comment["user"]["uslug"]
                    sub_comment["avatar_url"] = sub_comment["user"]["avatar_url"]
                    del sub_comment["user"]
                    AddDataToDatabase(CommentsData, sub_comment)
                
                # 处理一般评论
                del comment["sub_comments"]
                comment["is_sub_comment"] = False
                comment["article_name"] = name
                comment["article_url"] = url
                comment["uid"] = comment["user"]["uid"]
                comment["user_name"] = comment["user"]["name"]
                comment["uslug"] = comment["user"]["uslug"]
                comment["avatar_url"] = comment["user"]["avatar_url"]
                del comment["user"]
                AddDataToDatabase(CommentsData, comment)

    print_green("数据存档成功")
