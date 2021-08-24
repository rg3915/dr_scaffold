import os
import pytest  
import tempfile  
from os import path, system
from dr_scaffold.generators import Generator, pluralize, file_api
from dr_scaffold.management.commands import dr_scaffold
from dr_scaffold.scaffold_templates import serializer_templates, model_templates
from unittest import TestCase, mock


class TestGenerator(TestCase):
    tmpfilepath = os.path.join(tempfile.gettempdir(), "tmp-testfile")
    tmpdirpath = tempfile.mkdtemp()
    generator = Generator("blog", "Article", ("title:charfield", "body:textfield"))

    def setUp(self):
        for f in ['models.py', 'serializers.py', 'admin.py', 'urls.py', 'views.py']:
            with open(os.path.join(self.tmpdirpath, f), 'x') as file:
                file.close()
        
    def tearDown(self):
        for f in ['models.py', 'serializers.py', 'admin.py', 'urls.py', 'views.py']:
            os.remove(f'{self.tmpdirpath}/{f}')
    
    def test_pluralize(self):
        assert pluralize("article") == 'articles'
        assert pluralize("category") == 'categories'
        assert pluralize("post") == 'posts'

    def test_init(self):
        g = self.generator
        assert g.app_name == "blog"
        assert g.MAIN_DIR == "./"
        assert g.model_name == "Article"

    def test_add_setup_imports(self):
        g = self.generator
        file_paths = (self.tmpdirpath+'/models.py',)
        matching_imports = (serializer_templates.SETUP,)
        g.add_setup_imports(file_paths, matching_imports)
        with open(file_paths[0], 'r+') as file:
            body = ''.join(line for line in file.readlines())
        assert body == serializer_templates.SETUP

    def test_setup_files(self):
        g = Generator(f"{self.tmpdirpath}/blog", "Article", ("title:charfield", "body:textfield"))
        #making the appdir the temp folder for test purpose
        g.appdir = self.tmpdirpath
        g.setup_files()
        files = [f for f in os.listdir(self.tmpdirpath)]
        with open(self.tmpdirpath+'/models.py', 'r+') as file:
            body = ''.join(line for line in file.readlines())      
        assert len(files) == 5
        assert ("from django.db import models" in body) == True

    def test_get_fields_string(self):
        g = self.generator
        fields_string = g.get_fields_string(g.fields)
        string = model_templates.CHARFIELD % dict(name ="title") + model_templates.TEXTFIELD % dict(name="body")
        assert fields_string == string

    def test_get_model_string(self):
        g = self.generator
        fields_string = g.get_fields_string(fields = g.fields)
        model_string = g.get_model_string()
        string = model_templates.MODEL % ("Article", fields_string, "Articles")
        assert model_string == string

    def test_generate_models(self):
        g = Generator(f"{self.tmpdirpath}/blog", "Article", ("title:charfield", "body:textfield"))
        #making the appdir the temp folder for test purpose
        g.appdir = self.tmpdirpath
        g.generate_models()      
        with open(f"{g.appdir}/models.py", 'r+') as file:
            body = ''.join(line for line in file.readlines())
        assert ('Article' in body) == True
        assert ('Articles' in body) == True
        assert ('title' in body) == True
        assert ('body' in body) == True
      
    def test_get_admin_parts(self):
        g = Generator(f"{self.tmpdirpath}/blog", "Article", ("title:charfield",))
        head, body = g.get_admin_parts()
        assert ("import Article" in head) == True
        assert ("@admin.register(Article)" in body) == True

    def test_register_models_to_admin(self):
        g = Generator(f"{self.tmpdirpath}/blog", "Article", ("title:charfield",))
        g.appdir = self.tmpdirpath
        g.register_models_to_admin()
        with open(f"{g.appdir}/admin.py", 'r+') as file:
            body = ''.join(line for line in file.readlines())
        assert ("import Article" in body) == True
        assert ("@admin.register(Article)" in body) == True

    def test_get_viewset_parts(self):
        g = Generator(f"{self.tmpdirpath}/blog", "Article", ("title:charfield",))
        head, body = g.get_viewset_parts()
        assert ("import Article" in head) == True
        assert ("class ArticleViewSet" in body) == True

    def test_generate_views(self):
        g = Generator(f"{self.tmpdirpath}/blog", "Article", ("title:charfield",))
        #making the appdir the temp folder for test purpose
        g.appdir = self.tmpdirpath
        g.generate_views()      
        with open(f"{g.appdir}/views.py", 'r+') as file:
            body = ''.join(line for line in file.readlines())
        assert ('import Article' in body) == True
        assert ('ArticleViewSet' in body) == True
        assert ('ArticleSerializer' in body) == True

    def test_get_serializer_parts(self):
        g = Generator(f"{self.tmpdirpath}/blog", "Article", ("title:charfield",))
        head, body = g.get_serializer_parts()
        assert ("import Article" in head) == True
        assert ("class ArticleSerializer" in body) == True

    def test_generate_serializer(self):
        g = Generator(f"{self.tmpdirpath}/blog", "Article", ("title:charfield",))
        #making the appdir the temp folder for test purpose
        g.appdir = self.tmpdirpath
        g.generate_serializers()      
        with open(f"{g.appdir}/serializers.py", 'r+') as file:
            body = ''.join(line for line in file.readlines())
        assert ('import Article' in body) == True
        assert ('ArticleSerializer' in body) == True

    def test_get_url_parts(self):
        g = Generator(f"{self.tmpdirpath}/blog", "Article", ("title:charfield",))
        head, body = g.get_url_parts()
        assert ("import ArticleViewSet" in head) == True
        assert (", ArticleViewSet)" in body) == True

    @mock.patch('dr_scaffold.file_api.replace_file_chunk')
    def test_generate_urls(self, mock_replace_chunk):
        g = Generator(f"{self.tmpdirpath}/blog", "Article", ("title:charfield",))
        #making the appdir the temp folder for test purpose
        g.appdir = self.tmpdirpath
        g.generate_urls()      
        with open(f"{g.appdir}/urls.py", 'r+') as file:
            body = ''.join(line for line in file.readlines())
        assert ('import ArticleViewSet' in body) == True
        assert (', ArticleViewSet)' in body) == True
        #test : if url have been added we won't add it again
        g = Generator(f"{self.tmpdirpath}/blog", "Article", ("title:charfield",))
        #making the appdir the temp folder for test purpose
        g.appdir = self.tmpdirpath
        g.generate_urls()  
        with open(f"{g.appdir}/urls.py", 'r+') as file:
            body = ''.join(line for line in file.readlines())
        assert body.count('import ArticleViewSet') == 1
        assert body.count(', ArticleViewSet)') == 1
        #test : if when creating another resource we replace the url_patterns
        g = Generator(f"{self.tmpdirpath}/blog", "Author", ("name:charfield",))
        #making the appdir the temp folder for test purpose
        g.appdir = self.tmpdirpath
        g.generate_urls() 
        mock_replace_chunk.assert_called()


    @mock.patch('dr_scaffold.generators.Generator.generate_api')
    def test_generate_api(self, mock_generate_api):
        g = Generator(f"{self.tmpdirpath}/blog", "Article", ("title:charfield",))
        g.generate_api()
        mock_generate_api.assert_called()

    @mock.patch('dr_scaffold.generators.Generator.run')
    def test_run(self, mock_run):
        g = Generator(f"{self.tmpdirpath}/blog", "Article", ("title:charfield",))
        g.run()
        mock_run.assert_called()

    @mock.patch('dr_scaffold.generators.Generator.generate_app')
    def test_generate_app(self, mock_generate_app):
        g = Generator(f"{self.tmpdirpath}/blog", "Article", ("title:charfield",))
        g.generate_app()
        mock_generate_app.assert_called()