# Add OpeanAPI documentation and SwaggerUI to your Django Rest Framework project

Here is step-by-step recipe on how to add auto generated documentation for your REST API in OpenAPI format and enable SwaggerUI. The recipe is based on [Document your API](https://www.django-rest-framework.org/topics/documenting-your-api/) tutorial from Django Rest Framework.

## Step 1: Create documentation application

```bash
python manage.py startapp docs
```

## Step 2. Register documentation endpoints

Create `urls.py` in the `api_docs` application:

```python
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework import renderers

urlpatterns = [
    path('docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema-yaml'}
    ), name='swagger-ui'),
    path('openapi.yaml', get_schema_view(
            title="Best API Service",
            renderer_classes=[renderers.OpenAPIRenderer]
        ), name='openapi-schema-yaml'),
    path('openapi.json', get_schema_view(
            title="Best API Service",
            renderer_classes = [renderers.JSONOpenAPIRenderer], 
        ), name='openapi-schema-json'),
]
```

This will register three endpoints:

- `/openapi.json` - OpenAPI documentation in JSON format
- `/openapi.yaml` - OpenAPI documentation in YAML format
- `/docs` - Swagger UI, based on the `openapi.yaml`



## Step 3. Create the Swagger UI template

Create a `swagger-ui.html` file in the `api_docs` application's *templates* directory:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Swagger</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="//unpkg.com/swagger-ui-dist@3/swagger-ui.css" />
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
    <script>
    const ui = SwaggerUIBundle({
        url: "{% url schema_url %}",
        dom_id: '#swagger-ui',
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout",
        requestInterceptor: (request) => {
          request.headers['X-CSRFToken'] = "{{ csrf_token }}"
          return request;
        }
      })
    </script>
  </body>
</html>
```

## Step 4. Register the `api_docs` application with the Django project

To register the  `api_docs` application in the Django project you need to modify the project's `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'docs',
    # ...
]

```

## Step 5. Add documentation URLs to Django project `urls`

Modify the `urls.py` file for your Django project. Make sure in contains `include('api_docs.urls')`:

```python
from django.urls import path, include

urlpatterns = [
    # ...
    path('', include('api_docs.urls')),
    # ...
]
```

