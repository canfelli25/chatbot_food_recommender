from django.conf import settings
from django.urls import path
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import TutorialBotView

urlpatterns = [
	path('webhooks/tutorial/', csrf_exempt(TutorialBotView.as_view())),
]