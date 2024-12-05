from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    PurposeViewSet, RegisterInformationDataListAPIView, SourceOfInformationViewSet, UniversityViewSet, 
    FilialViewSet, RegionViewSet, ProgramViewSet, RegisterViewSet
)

app_name = "register"


router = DefaultRouter()
router.register(r'purposes', PurposeViewSet)
router.register(r'sources_of_information', SourceOfInformationViewSet)
router.register(r'universities', UniversityViewSet)
router.register(r'filials', FilialViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'programs', ProgramViewSet)
router.register(r'registers', RegisterViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register_information_data/', RegisterInformationDataListAPIView.as_view(), name='register_information_data'),
]
