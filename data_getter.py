import JianshuResearchTools as jrt
from datetime import datetime

def GetUserData(user_url):
    result = {}
    
    user_json_data = jrt.basic_apis.GetUserJsonDataApi(user_url)
    result["uid"] = user_json_data["id"]
    result["uslug"] = user_json_data["slug"]
    result["user_url"] = jrt.convert.UserSlugToUserUrl(result["uslug"])
    result["name"] = user_json_data["nickname"]
    result["gender"] = {
        0: "未知（0）", 
        1: "男", 
        2: "女", 
        3: "未知（3）"
    }[user_json_data["gender"]]
    result["badges"] = [badge["text"] for badge in user_json_data["badges"]]
    result["avatar_url"] = user_json_data["avatar"]
    result["background_image_url"] = user_json_data["background_image"]
    result["followings_count"] = user_json_data["following_users_count"]
    result["fans_count"] = user_json_data["followers_count"]
    result["total_wordage"] = user_json_data["total_wordage"]
    result["total_likes_count"] = user_json_data["total_likes_count"]
    result["FP_count"] = user_json_data["jsd_balance"] / 1000
    result["total_assets"] = jrt.user.GetUserAssetsCount(user_url)
    result["FTN_count"] = round(result["total_assets"] - result["FP_count"], 3)
    result["last_update_time"] = datetime.fromtimestamp(user_json_data["last_updated_at"])
    result["introduction_text"] = jrt.user.GetUserIntroductionText(user_url)

    return result

def GetArticleData(article_url):
    result = {}
    
    article_json_data = jrt.basic_apis.GetArticleJsonDataApi(article_url)
    result["aid"] = article_json_data["id"]
    result["aslug"] = article_json_data["slug"]
    result["title"] = article_json_data["public_title"]
    result["wordage"] = article_json_data["wordage"]
    result["FP_count"] = article_json_data["total_fp_amount"] / 1000
    result["likes_count"] = article_json_data["likes_count"]
    result["comments_count"] = article_json_data["public_comment_count"]
    result["most_valuable_comments_count"] = article_json_data["featured_comments_count"]
    result["paid_type"] = {
        "free": "文集中的免费文章", 
        "fbook_free": "免费连载中的免费文章", 
        "pbook_free": "付费连载中的免费文章", 
        "paid": "文集中的付费文章", 
        "fbook_paid": "免费连载中的付费文章", 
        "pbook_paid": "付费连载中的付费文章"
    }[article_json_data["paid_type"]]
    result["nid"] = article_json_data["notebook_id"]
    result["commentable"] = article_json_data["commentable"]
    result["reprintable"] = article_json_data["reprintable"]
    result["publish_time"] = datetime.fromisoformat(article_json_data["first_shared_at"])
    result["update_time"] = datetime.fromtimestamp(article_json_data["last_updated_at"])
    result["description"] = article_json_data["description"]
    
    return result

def GetUserAllArticlesNameAndUrl(user_url):
    result = {}
    page = 1
    
    while True:
        articles_data = jrt.user.GetUserArticlesInfo(user_url, page=page, count=200)
        if articles_data == []:
            break
        result.update({article["title"]: jrt.convert.ArticleSlugToArticleUrl(article["aslug"]) \
                 for article in articles_data})  # 生成新的字典并与原字典合并
        page += 1
    
    return result