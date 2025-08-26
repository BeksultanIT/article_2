from django.urls import path

from api_v2.views import ArticleView, get_token_view, CommentView

app_name = 'v2'

urlpatterns = [
    path('articles/', ArticleView.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleView.as_view(), name='article'),
    path('get-csrf/', get_token_view, name='get-csrf'),
    path('articles/<int:article_id>/comments/', CommentView.as_view(), name='comments'),
    path('articles/<int:article_id>/comments/<int:pk>/', CommentView.as_view(), name='comment'),

]
