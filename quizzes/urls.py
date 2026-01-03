from django.urls import path, include
from . import views
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register(r'', views.QuizViewSet)

question_router = routers.NestedSimpleRouter(router, r'', lookup='quiz')
question_router.register(r'questions', views.QuestionViewSet, basename='quiz-questions')
# basename='quiz-questions'

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(question_router.urls)),
]