Nested Serialization in Django REST Framework
###############################################

.. post:: 2023-09-16 18:00:00
   :tags: django,django rest framework,drf,serialization
   :category: django
   :author: ivan
   :language: en

In case you are serializing a model with relationships the default ModelSerializer behavior is
to provide the primary key of the relationship target. In case you need to serialize the target object
not just the primary key, you have (at least) two options: explicit nested serializer and implicit
nested serializer using `depth`.

.. contents:: Table of Contents
   :local:
   :depth: 3

Default Relationship Serialization
************************************

In our e-learning example project, `Course` model has a relationship with `Subject` via
the `subject` field.

.. code-block:: json
   :caption: Default serialization serializes only the primary key

   {
      "id": 6,
      "title": "Django Rest Framework 101",
      "slug": "drf-101",
      "overview": "string",
      "created": "2023-09-13T17:57:29.033182Z",
      "owner": 1,
      "subject": 1
   }


Explicit Nested Django Rest Framework Serializer
****************************************************

We can explicitly create `subject` field for the `CourseSerializer` with a type of `SubjectSerializer`:

.. code-block:: python
   :caption: couses/serializers.py
   :linenos:

   from rest_framework import serializers

   from .models import Course, Subject
   from core.fields import UniqueKeyRelatedField


   class SubjectSerializer(serializers.ModelSerializer):
      class Meta:
         model = Subject
         fields = "__all__"


   class CourseSerializer(serializers.ModelSerializer):
      subject = SubjectSerializer()

      class Meta:
         model = Course
         fields = "__all__"

Django Rest Framework will serialize the relationship using the `SubjectSerializer`'s output:

.. code-block:: json

   {
      "id": 6,
      "subject": {
         "id": 1,
         "title": "Software Development",
         "slug": "soft-dev"
      },
      "title": "Django Rest Framework 101",
      "slug": "drf-101",
      "overview": "string",
      "created": "2023-09-13T17:57:29.033182Z",
      "owner": 1
   }


Implicit Nested Django Rest Framework Serializer using `depth`
****************************************************************

Another approcach could be to specify a positive `depth` attribute to the `Course` serializer's `Meta` class:

.. code-block:: python
   :caption: courses/serializers.py
   :emphasize-lines: 4

   class CourseSerializer(serializers.ModelSerializer):
      class Meta:
         model = Course
         depth = 1
         fields = "__all__"

.. code-block:: json

   {
      "id": 6,
      "title": "Django Rest Framework 101",
      "slug": "drf-101",
      "overview": "string",
      "created": "2023-09-13T17:57:29.033182Z",
      "owner": {
         "id": 1,
         "password": "you-do-not-need-to-know",
         "last_login": null,
         "is_superuser": true,
         "username": "ivang",
         "first_name": "",
         "last_name": "",
         "email": "",
         "is_staff": true,
         "is_active": true,
         "date_joined": "2023-09-13T17:21:09.158970Z",
         "groups": [],
         "user_permissions": []
      },
      "subject": {
         "id": 1,
         "title": "Software Development",
         "slug": "soft-dev"
      }
   }

Under the hood Django Rest Framework has created a serializer for the two relationship fields in our `Course` model.
This approach has some caveats:

- The nested serializer always includs all the fileds from the relationship's target model. You cannot exclude fields from the relationship seriaizer.
  One way to change this behavior is to override the `.build_nested_field()` method of the serializer (see `here <https://www.django-rest-framework.org/api-guide/serializers/#the-field_class-and-field_kwargs-api>`__).
- All relationships, which are present in the serializer are serialized using implicit nested serializer. For example, we want
  to provide only the owner id, not to serialize the whole object. We could achieve this by specifying `PrimaryKeyRelatedField` field:

  .. code-block:: python
      :caption: courses/serializers.py
      :linenos:
      :emphasize-lines: 2

      class CourseSerializer(serializers.ModelSerializer):
         owner = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())

         class Meta:
            model = Course
            depth = 1
            fields = "__all__"

  This would serialize the `owner` relationship using the primary key of the target model:

  .. code-block:: json

      {
         "id": 6,
         "owner": 1,
         "title": "Django Rest Framework 101",
         "slug": "drf-101",
         "overview": "string",
         "created": "2023-09-13T17:57:29.033182Z",
         "subject": {
            "id": 1,
            "title": "Software Development",
            "slug": "soft-dev"
         }
      }


Additional Information
***************************

For additional information you can refer to following:

- `Specifying nested serialization <https://www.django-rest-framework.org/api-guide/serializers/#specifying-nested-serialization>`__ in Django Rest Framework
- `Nested Serializers <https://testdriven.io/blog/drf-serializers/#nested-serializers>`__ from testdriven.io blog post provides in-depth discussion on Django Rest Framework serialization
