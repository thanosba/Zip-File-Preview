import zipfile
import datetime
import os
import json


archive_name = 'data.zip' #raw_input('Enter file path: ')

    


TEMPLATE_TPL = """
<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title></title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link rel="stylesheet" href="css/bootstrap.min.css">
        <link rel="stylesheet" href="css/tree-styles.css">
        <style>
            body {
                padding-top: 150px;
                padding-bottom: 20px;
            }
        </style>
        <link rel="stylesheet" href="css/bootstrap-theme.min.css">
        <link rel="stylesheet" href="css/main.css">

  
    </head>
    <body>
        <!--[if lt IE 7]>
            <p class="browsehappy">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> to improve your experience.</p>
        <![endif]-->
    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Tree View</a>
        </div>
        <div class="navbar-collapse collapse">
          
        </div><!--/.navbar-collapse -->
      </div>
    </div>

    <div class="container">
      <!-- Example row of columns -->
        <div class="row">
            <div class="col-md-6">

            <div class="panel panel-default">
              <div class="panel-heading">
                <h3 class="panel-title">Zip Files Preview</h3>
              </div>
              <div class="file_info"><p><span><i class="glyphicon glyphicon-compressed"></i></span> {{ archive_name }} <span class="pull-right">Size: <b> {# Here should be the total size of the ziped folder #}Mb</b></span></p>
                          <hr>
              </div>
              <div class="panel-body">
              
              <div class="tree">
               
                <ul>
                    {%- for t in tree recursive %}
                        <li><span class="li_wrap">
                        	<span><i class="glyphicon {{ 'glyphicon-folder-close' if t.type == 'folder' else 'glyphicon-file'}}"></i> {{ t.name }}</span>
                        	{% if t.type != 'folder' %}
                        		<span class="pull-right">{{ t.size|filesizeformat }} </span> 
                        	{% endif %}
                        	</span>
                        {%- if t.children -%}
                            <ul>{{ loop(t.children) }}</ul>
                        {%- endif %}
                        </li>
                    {%- endfor %}
                    </ul>
           	  </div> 

                

              </div> <!-- panel-body close -->
            </div> <!-- panel panel-default close -->

            </div> <!-- col-md-6 close -->
        </div>

      <hr>

      <footer>
        <p>&copy; Tree View 2014</p>
      </footer>
    </div> <!-- /container -->        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
        <script>window.jQuery || document.write('<script src="js/vendor/jquery-1.11.0.min.js"><\/script>')</script>

        <script src="js/vendor/bootstrap.min.js"></script>
        <script src="js/vendor/modernizr-2.6.2-respond-1.1.0.min.js"></script>
        <script type="text/javascript" src="js/tree.js"></script>
        <script src="js/plugins.js"></script>
        <script src="js/main.js"></script>

        <!-- Google Analytics: change UA-XXXXX-X to be your site's ID. -->
        <script>
            (function(b,o,i,l,e,r){b.GoogleAnalyticsObject=l;b[l]||(b[l]=
            function(){(b[l].q=b[l].q||[]).push(arguments)});b[l].l=+new Date;
            e=o.createElement(i);r=o.getElementsByTagName(i)[0];
            e.src='//www.google-analytics.com/analytics.js';
            r.parentNode.insertBefore(e,r)}(window,document,'script','ga'));
            ga('create','UA-XXXXX-X');ga('send','pageview');
        </script>
    </body>
</html>


"""
    
def print_template(archive_name, tree):
    from jinja2 import Template
    template = Template(TEMPLATE_TPL)
    print template.render(tree=tree, archive_name=archive_name)


def make_tree(archive_name):
    zf = zipfile.ZipFile(archive_name)
    
    tree = {'type': 'folder', 'id': -1, 'children': {}}
    

    for i, info in enumerate(zf.infolist()):
        comps = info.filename.split(os.sep)

        node = tree
        for c in comps:
            if c not in node['children']:
                if c == '':
                    node['type'] = 'folder'
                    continue
                node['children'][c] = {'name': c, 'type': 'item', 'id': 'item%s' % i, 'children': {}}
            node = node['children'][c]

        node['size'] = info.file_size

    return tree


def children_to_list(node):
    if node['type'] == 'item':
        del node['children']
    else:
        node['children'] =  list(node['children'].values())
        node['children'].sort(key=lambda x: x['name'])
        node['children'] = map(children_to_list, node['children'])
    return node
        
if __name__ == '__main__':

    tree = children_to_list(make_tree(archive_name))['children']

    print_template(archive_name, tree)


