from django.shortcuts import render_to_response, RequestContext
from apps.schema import models
from django.db.models import get_app, get_models
from pygraphviz import *
import os
from django_schema_explorer.settings import (
    EXCLUDE_LIST,URL_ROOT,TABLE_DESCRIPTION_MODEL as table_desc,FIELD_DESCRIPTION_MODEL as field_desc)
from django.apps import apps


def get_table_fields(modelname, for_table=None):
    model=getattr(models, modelname)

    #Get fields and their data
    fields=[]
    for field in model._meta.get_fields():

        #Exclude reverse related fields
        if field.auto_created==True:continue

        #Exclude fields that point to hidden tables
        try:
            if field.rel.to.__name__ in EXCLUDE_LIST:continue               
        except:None

        #Field name
        field_data={'name':field.name}

        #Field data types
        #Convert django internal types to mysql data types
        field_type=field.get_internal_type()
        if field_type=='CharField':
            field_data['field_type']='varchar'
        elif field_type in ['IntegerField','PositiveIntegerField','ForeignKey','ManyToManyField']:
            field_data['field_type']='int'
        elif field_type in ['FloatField','DecimalField']:
            field_data['field_type']='double'
        elif field_type=='DateField':
            field_data['field_type']='date'
        elif field_type=='DateTimeField':
            field_data['field_type']='datetime'
        elif field_type=='TextField':
            field_data['field_type']='text'
        elif field_type=='AutoField':
            field_data['field_type']='int(auto increment)'
        elif field_type in ['BooleanField','NullBooleanField']:
            field_data['field_type']='tinyint'

        
        if for_table:
            #Get db_column name as it may be different from the model field name
            if field.db_column:
                db_column=field.db_column
            else:
                db_column=field.name                
            field_data['db_column']=db_column

            #Get referenced tables, exclude references to django authentication database
            try:
                rel_table=field.rel.to._meta.db_table
                if not rel_table=='auth_group':
                    field_data['referenced_table']=rel_table                   
            except:None

            #Get field description from field description table if it is defined in settings
            if field_desc is not '':
                try:
                    table_desc_model=getattr(models, table_desc)
                    desc_table=table_desc_model.objects.get(name=model._meta.db_table)
                except:None
                try:
                    field_desc_model=getattr(models, field_desc)
                    desc_field=field_desc_model.objects.get(table_id=desc_table.id, name=db_column)
                except:
                    try:
                        field_desc_model=getattr(models, field_desc)
                        desc_field=field_desc_model.objects.get(table_id=desc_table.id, name=db_column+'_id')  
                    except:
                        field_data['description']=''
                        fields.append(field_data)
                        continue

                field_data['description']=desc_field.description


        fields.append(field_data)

    return fields



def schema(request, table=None):
    table_list=[]
    model_list={}
    for model in apps.get_models():
        if model.__name__ in EXCLUDE_LIST:continue            
        model_list[model._meta.db_table]=model.__name__
        table_list.append(model._meta.db_table)

    request_dict={'url_root':URL_ROOT,'table_list':table_list}
    if table:
        if table in table_list:
            request_dict['table']=table
            #Get general table description 
            try:
                table_desc_model=getattr(models, table_desc)
                desc_table=table_desc_model.objects.get(name=table)
                request_dict['contents']=desc_table.contents
                request_dict['description']=desc_table.description
            except:None

            #Get all reverse related table names, map relations
            referencing_tables=[]
            relations=[]
            for ref_model in apps.get_models():
                #Exclude hidden tables
                if ref_model.__name__ in EXCLUDE_LIST:continue                  

                fields=ref_model._meta.get_fields()
                for field in fields:
                    try:
                        if field.rel.to._meta.db_table==table:
                            if ref_model._meta.db_table==table:
                                #Self relations
                                relations.append("    "+table+":"+field.name+":w->"+table+":id:w;")
                                continue
                            if ref_model._meta.db_table not in referencing_tables:
                                referencing_tables.append(ref_model._meta.db_table)
                            relations.append("    "+ref_model._meta.db_table+":"+field.name+"->"+table+":id;")
                    except:None   
            request_dict['referencing_tables']=referencing_tables

            #Get field information for displaying in table
            request_dict['fields']=get_table_fields(model_list[table], for_table=True)

            #If field and table description models are defined in settings, show the description column in table
            if field_desc is not '' and table_desc is not '':
                request_dict['field_desc']=True

            #Create graph

            #Variables
            header_color = "#bacbe4"
            content_color1 = "#eeeeee"
            content_color2 = "#ffffff"
            table_border = 1
            cell_border = 0
            cell_spacing = 0
            name_align = "left"
            type_align = "left"
            
            referenced_tables=[]

            #Map relations to referenced tables
            for field in request_dict['fields']:
                if 'referenced_table' in field:
                    #Exclude self relations
                    if field['referenced_table']==table:continue                        

                    referenced_tables.append(field['referenced_table'])
                    relations.append("    "+table+":"+field['name']+"->"+field['referenced_table']+":id;")
                     
            #Create the list of tables to be displayed on the graph           
            graph_table_list=referencing_tables + referenced_tables
            graph_table_list.append(table)

            #Create .dot file
            if len(graph_table_list)>1:

                dot = open(os.path.join(os.path.dirname(__file__),'graph.dot'), 'w')

                print("digraph " + table + " {", file=dot);
                print("    node [shape=plaintext, fontsize=7, fontname=" + '"' + "sans-serif" + '"' + "];", file=dot)
                print("    nodesep=0.10;", file=dot)
                #if there is 1 table or less in each rank, draw ranks left to right instead of top to bottom
                if len(referencing_tables)<2 and len(referenced_tables)<2:
                    print("    rankdir=LR;", file=dot)
                print("    compound=true;", file=dot)
                print("    ratio=fill;", file=dot)
                print("    edge [penwidth=1.0, style=solid];", file=dot)
                for graph_table in graph_table_list:
                    print("    " + graph_table + " [href=" + '"' + "http://" + URL_ROOT + "/" + graph_table + '/"'
                        + ", label=<<TABLE BORDER=" + '"' + str(table_border) + '"'
                        + " CELLBORDER=" + '"' + str(cell_border)+ '"'
                        + " CELLSPACING=" + '"' + str(cell_spacing) + '"'
                        + " BGCOLOR=" + '"' + content_color1 + '"' + ">", end='', file=dot)
                    # Table header
                    print("<TR><TD COLSPAN=" + '"' + str(2) + '"' + " PORT=" + '"'
                          + graph_table + '"' + " BGCOLOR=" + '"' + header_color
                          + '"' + "><B>" + graph_table
                          + "</B></TD></TR>", end='', file=dot)
                    #Table rows
                    fields=get_table_fields(model_list[graph_table])
                    alt_row = 0;
                    for field in fields:
                        #Field name
                        print("<TR><TD ALIGN=" + '"' + name_align + '"' + " PORT="
                              + '"' + field['name'] + '"', end='', file=dot);
                        if alt_row == 1:
                            print(" BGCOLOR=" + '"' + content_color2 + '"', end='', file=dot)
                        print(">" + field['name'] + "</TD>", end='', file=dot);
                        #Field type
                        print("<TD ALIGN=" + '"' + type_align + '"', end='', file=dot); 
                        if alt_row == 1:
                            print(" BGCOLOR=" + '"' + content_color2 + '"', end='', file=dot)
                        print(">" + field['field_type'] + "</TD></TR>", end='', file=dot);
                        alt_row = 1 - alt_row;
                    print("</TABLE>>];", file=dot);

                #Relation arrows
                for relation in relations:
                    print(relation, file=dot);
                print("}", file=dot)

                dot.close()

                #Create svg image file
                G=AGraph(strict=False, directed=True)
                G.read(os.path.join(os.path.dirname(__file__),'graph.dot'))
                s=G.string()
                G.layout(prog="dot")
                G.draw(os.path.join(os.path.dirname(__file__),"../../django_schema_explorer/static/schema_imgs/"+table + ".svg"))

                request_dict['graph_file']=table + ".svg"

        #If nonexisting table is requested in url
        else:
            request_dict['error']='No access to table %s' %table


    return render_to_response('index.html',request_dict, RequestContext(request))




