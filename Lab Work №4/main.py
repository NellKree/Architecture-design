from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

app = FastAPI()

# ========== Модели ==========
class User(BaseModel):
    username: str
    email: str
    password: str

class Post(BaseModel):
    user_id: int
    content: str

class Comment(BaseModel):
    post_id: int
    user_id: int
    content: str

class Report(BaseModel):
    reported_user_id: Optional[int] = None
    reported_post_id: Optional[int] = None
    reason: str
    description: Optional[str] = None

# ========== Хранилище данных ==========
users: Dict[int, User] = {}
posts: Dict[int, Post] = {}
comments: Dict[int, Comment] = {}
reports: Dict[int, Report] = {}

user_id_counter = 1
post_id_counter = 1
comment_id_counter = 1
report_id_counter = 1

# ========== Работа с пользователями ==========

@app.post("/users", response_model=User, status_code=201)
def create_user(user: User):
    global user_id_counter
    if any(u.email == user.email for u in users.values()):
        raise HTTPException(status_code=409, detail="User with this email already exists")
    users[user_id_counter] = user
    user_id = user_id_counter
    user_id_counter += 1
    return {"user_id": user_id, **user.dict()}

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, **user.dict()}

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id] = updated_user
    return {"user_id": user_id, **updated_user.dict()}

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]

# ========== Работа с публикациями ==========

@app.post("/posts", response_model=Post, status_code=201)
def create_post(post: Post):
    global post_id_counter
    posts[post_id_counter] = post
    post_id = post_id_counter
    post_id_counter += 1
    return {"post_id": post_id, **post.dict()}

@app.get("/posts/{post_id}", response_model=Post)
def get_post(post_id: int):
    post = posts.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post_id": post_id, **post.dict()}

@app.get("/users/{user_id}/posts", response_model=List[Post])
def get_user_posts(user_id: int):
    user_posts = [post for post in posts.values() if post.user_id == user_id]
    if not user_posts:
        raise HTTPException(status_code=404, detail="No posts found for this user")
    return user_posts

@app.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    del posts[post_id]

# ========== Работа с комментариями ==========

@app.post("/comments", response_model=Comment, status_code=201)
def create_comment(comment: Comment):
    global comment_id_counter
    comments[comment_id_counter] = comment
    comment_id = comment_id_counter
    comment_id_counter += 1
    return {"comment_id": comment_id, **comment.dict()}

@app.delete("/comments/{comment_id}", status_code=204)
def delete_comment(comment_id: int):
    if comment_id not in comments:
        raise HTTPException(status_code=404, detail="Comment not found")
    del comments[comment_id]

# ========== Работа с жалобами ==========

@app.post("/reports", response_model=Report, status_code=201)
def create_report(report: Report):
    global report_id_counter
    reports[report_id_counter] = report
    report_id = report_id_counter
    report_id_counter += 1
    return {"report_id": report_id, **report.dict()}

@app.get("/reports", response_model=List[Report])
def get_reports(status: Optional[str] = None):
    if status:
        filtered_reports = [r for r in reports.values() if r.status == status]
        if not filtered_reports:
            raise HTTPException(status_code=404, detail="No reports found with this status")
        return filtered_reports
    return list(reports.values())

@app.put("/reports/{report_id}", response_model=Report)
def update_report(report_id: int, updated_report: Report):
    if report_id not in reports:
        raise HTTPException(status_code=404, detail="Report not found")
    reports[report_id] = updated_report
    return {"report_id": report_id, **updated_report.dict()}

@app.delete("/reports/{report_id}", status_code=204)
def delete_report(report_id: int):
    if report_id not in reports:
        raise HTTPException(status_code=404, detail="Report not found")
    del reports[report_id]