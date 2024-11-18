from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


crm_openapi = openapi.Info(
    title="Snippets API",
    default_version='v1',
    description="Test description",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="contact@snippets.local"),
    license=openapi.License(name="BSD License"),
)
schema_view = get_schema_view(
    crm_openapi,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

