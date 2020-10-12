# Document REST APIs based on Python Django's Rest Framework Function Views

When using object-oriented implementation for your REST API, most of the documentation can be generated automatically from serializers and models you have created.

When using function based views, you have almost no flexibility for creating OpenAPI documentation for your REST API.

The typical signature for a view function is:

```python
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def hello_world(request):
    '''
    get: get greeting
    post: post a greeting
    '''
    return Response({"message": "Hello, world!"})
```

The `@api_view` decorator wraps your view function into an `APIView` subclass. You can define description for all the methods, supported by the function in the function's docstring. This is practically all the supported documentation.

Fortunately Django Rest Framework provides an extension point through the `@schema`  decorator. I have created a quick and easy solution for OpenAPI generation, based on the `@schema` decorator. 

## Custom AutoSchema class

The solution parses the view function docstring and uses it in the process of the automatic documentation generation. 

The following `AutoDocstringSchema` class parses the yaml from the view docstring and returns the operations and components defined.  To build the documentation, the `AutoSchema` methods are invoked first and the result is combined with the documentation from the docstring.

If the docstring fails to parse as yaml, it is ignored.

```python
class AutoDocstringSchema(AutoSchema):

    @property
    def documentation(self):
        if not hasattr(self, '_documentation'):
            try:
                self._documentation = yaml.safe_load(self.view.__doc__)
            except yaml.scanner.ScannerError:
                self._documentation = {}
        return self._documentation

    def get_components(self, path, method):
        components = super().get_components(path, method)
        doc_components = self.documentation.get('components', {})
        components.update(doc_components)
        return components

    def get_operation(self, path, method):
        operation = super().get_operation( path, method)
        doc_operation = self.documentation.get(method.lower(), {})
        operation.update(doc_operation)
        return operation
```

Here is an example of function views, documented using yaml docstring:

```python
@api_view(['GET'])
@schema(AutoDocstringSchema())
def list_todos(request):
    '''
    get:
      description: List todo items, stored in the database.
      summary: List todo items
    '''
    # ...
    
@api_view(['GET'])
@schema(AutoDocstringSchema())
def get_todo_item(request, id):
    '''
    get:
      description: Retrieve a todo item definition
      summary: Retrieve todo item
      parameters:
         - name: id
           in: path
           description: ToDo item ID
           schema:
              type: string
      responses:
         '200':
            description: Todo item successfully retrieved
            content:
               'application/json': {}
    '''
    # ...
```

Multiple request methods are supported. You can have a view function whish supports GET, POST, etc. requests at the same time. To document any of them, you define corresponding documentation, using lowercase method name.

You can also add definitions for components. If your docstring has `components` section, the components defined in this section will be added to the API components.

## Reference

* Django Rest Framework - [Schema](https://www.django-rest-framework.org/api-guide/schemas)
* Django Rest Framework - [Document your API](https://www.django-rest-framework.org/topics/documenting-your-api/)
* [OpenAPI Specification v.3.0.2](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md)