from flask import render_template, Blueprint, send_from_directory, request, make_response, jsonify
from flask_login import  current_user
from flask_security import login_required
from models import (SavedCharts, SavedDashboards, SavedTexts, SavedImages, 
    db, SavedNetworks, ItemInDashboard, NetworkNode, NetworkEdge)
from os import environ, path, remove
from bson import json_util
from bson.objectid import ObjectId
from json import loads 
from werkzeug.utils import secure_filename
import base64 # For images

bp = Blueprint("dashboard", __name__)

db_name = environ['MONGODB_DB']
collections = db.get_database(db_name).list_collection_names()
image_storage_path = "./image_store"

@bp.route("/admin/dashboard")
@login_required
def dashboard():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/maps")
@login_required
def maps():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/dashboard/people")
@login_required
def people_dashboard():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/tables")
@login_required
def tables():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/dashboard-reviser")
@login_required
def dashboard_reviser():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/dashboard-designer")
@login_required
def dashboard_designer():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/chart-designer")
@login_required
def chart_designer():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/update-save-chart", methods=['POST'])
@login_required
def update_save_chart():
    data = request.form.to_dict()
    
    # Check if this chart already exists
    # If it does, update otherwise save
    if len(SavedCharts.objects(chart_id=data['chart_id'])) > 0:
        print("Save chart")
        # Update dashboard
        SavedCharts.objects(chart_id=data['chart_id']).update(   
            background_color = data['background_color']

            ,chart_type = data['chart_type']
            ,legend_enabled = data['legend_enabled']
            
            ,yaxes_scale_label = data['yaxes_scale_label']
            ,xaxes_scale_label = data['xaxes_scale_label']
            
            ,yaxes_scale_label_enabled = data['yaxes_scale_label_enabled']
            ,xaxes_scale_label_enabled = data['xaxes_scale_label_enabled']

            ,yaxes_gridlines_color = data['yaxes_gridlines_color']
            ,xaxes_gridlines_color = data['xaxes_gridlines_color']
            
            ,yaxes_scalelabel_color = data['yaxes_scalelabel_color']
            ,xaxes_scalelabel_color = data['xaxes_scalelabel_color']
            
            ,legend_font_color = data['legend_font_color']
            
            ,yaxes_tick_color = data['yaxes_tick_color']
            ,xaxes_tick_color = data['xaxes_tick_color']
            
            ,yaxes_gridline_enabled = data['yaxes_gridline_enabled']
            ,xaxes_gridline_enabled = data['xaxes_gridline_enabled']
            
            ,title_fontsize = data['title_fontsize']
            ,title_fontcolor = data['title_fontcolor']
            ,title_text = data['title_text']
            ,title_enabled = data['title_enabled']
            
            ,default_font_family = data['default_font_family']
            
            ,chart_padding = data['chart_padding']
            ,deleted = False
        )
    else:
        # Store data in database
        SavedCharts(  
            chart_id = data['chart_id']
            ,background_color = data['background_color']

            ,chart_type = data['chart_type']
            ,legend_enabled = data['legend_enabled']
            
            ,yaxes_scale_label = data['yaxes_scale_label']
            ,xaxes_scale_label = data['xaxes_scale_label']
            
            ,yaxes_scale_label_enabled = data['yaxes_scale_label_enabled']
            ,xaxes_scale_label_enabled = data['xaxes_scale_label_enabled']

            ,yaxes_gridlines_color = data['yaxes_gridlines_color']
            ,xaxes_gridlines_color = data['xaxes_gridlines_color']
            
            ,yaxes_scalelabel_color = data['yaxes_scalelabel_color']
            ,xaxes_scalelabel_color = data['xaxes_scalelabel_color']
            
            ,legend_font_color = data['legend_font_color']
            
            ,yaxes_tick_color = data['yaxes_tick_color']
            ,xaxes_tick_color = data['xaxes_tick_color']
            
            ,yaxes_gridline_enabled = data['yaxes_gridline_enabled']
            ,xaxes_gridline_enabled = data['xaxes_gridline_enabled']
            
            ,title_fontsize = data['title_fontsize']
            ,title_fontcolor = data['title_fontcolor']
            ,title_text = data['title_text']
            ,title_enabled = data['title_enabled']
            
            ,default_font_family = data['default_font_family']
            
            ,chart_padding = data['chart_padding']
            
            ,deleted = False
        ).save()
    
    return 'Success'


@bp.route("/admin/networks", methods=["GET"])
@login_required
def get_networks():
    # print(SavedNetworks.objects())
    networks = loads(SavedNetworks.objects().to_json())
    for i in range(0, len(networks)):
        for node_index in range(0, len(networks[i]['nodes'])):
            new_json = NetworkNode.objects(id=networks[i]['nodes'][node_index]["$oid"]).to_json()  
            networks[i]['nodes'][node_index] = loads(new_json)
            
        for edge_index in range(0, len(networks[i]['edges'])):
            new_json = NetworkEdge.objects(id=networks[i]['edges'][edge_index]["$oid"]).to_json()  
            networks[i]['edges'][edge_index] = loads(new_json)
            
    return json_util.dumps(networks)



@bp.route("/admin/charts", methods=["GET"])
@login_required
def get_charts():
    return SavedCharts.objects.filter(deleted=False).to_json()



@bp.route("/admin/save-chart")
@login_required
def save_chart(data):
    data = data["data"]
    id = ""
    if len(SavedCharts.objects(chart_id=data['chart_id'])) == 0:
        # Store data in database
        SavedCharts(  
            chart_id = data['chart_id']
            ,background_color = data['background_color']

            ,chart_type = data['chart_type']
            ,legend_enabled = str(data['legend_enabled'])
            
            ,yaxes_scale_label = data['yaxes_scale_label']
            ,xaxes_scale_label = data['xaxes_scale_label']
            
            ,yaxes_scale_label_enabled = str(data['yaxes_scale_label_enabled'])
            ,xaxes_scale_label_enabled = str(data['xaxes_scale_label_enabled'])

            ,yaxes_gridlines_color = data['yaxes_gridlines_color']
            ,xaxes_gridlines_color = data['xaxes_gridlines_color']
            
            ,yaxes_scalelabel_color = data['yaxes_scalelabel_color']
            ,xaxes_scalelabel_color = data['xaxes_scalelabel_color']
            
            ,legend_font_color = data['legend_font_color']
            
            ,yaxes_tick_color = data['yaxes_tick_color']
            ,xaxes_tick_color = data['xaxes_tick_color']
            
            ,yaxes_gridline_enabled = str(data['yaxes_gridline_enabled'])
            ,xaxes_gridline_enabled = str(data['xaxes_gridline_enabled'])
            
            ,title_fontsize = str(data['title_fontsize'])
            ,title_fontcolor = data['title_fontcolor']
            ,title_text = data['title_text']
            ,title_enabled = str(data['title_enabled'])
            
            ,default_font_family = data['default_font_family']
            
            ,chart_padding = str(data['chart_padding'])
            
            ,deleted = False
        ).save()
    else:
        # Update data in database
        SavedCharts.objects(chart_id=data['chart_id']).update(  
            background_color = data['background_color']

            ,chart_type = data['chart_type']
            ,legend_enabled = str(data['legend_enabled'])
            
            ,yaxes_scale_label = data['yaxes_scale_label']
            ,xaxes_scale_label = data['xaxes_scale_label']
            
            ,yaxes_scale_label_enabled = str(data['yaxes_scale_label_enabled'])
            ,xaxes_scale_label_enabled = str(data['xaxes_scale_label_enabled'])

            ,yaxes_gridlines_color = data['yaxes_gridlines_color']
            ,xaxes_gridlines_color = data['xaxes_gridlines_color']
            
            ,yaxes_scalelabel_color = data['yaxes_scalelabel_color']
            ,xaxes_scalelabel_color = data['xaxes_scalelabel_color']
            
            ,legend_font_color = data['legend_font_color']
            
            ,yaxes_tick_color = data['yaxes_tick_color']
            ,xaxes_tick_color = data['xaxes_tick_color']
            
            ,yaxes_gridline_enabled = str(data['yaxes_gridline_enabled'])
            ,xaxes_gridline_enabled = str(data['xaxes_gridline_enabled'])
            
            ,title_fontsize = str(data['title_fontsize'])
            ,title_fontcolor = data['title_fontcolor']
            ,title_text = data['title_text']
            ,title_enabled = str(data['title_enabled'])
            
            ,default_font_family = data['default_font_family']
            
            ,chart_padding = str(data['chart_padding'])
            
            ,deleted = False
        )
    return SavedCharts.objects(chart_id=data['chart_id'])[0].id



@bp.route("/admin/save-text")
@login_required
def save_text(data):
    width = data['width']
    height = data['height']
    top = data['top']
    right = data['right']
    text = data["text"]
    font_size = data['font_size']
    color = data['color']
    font_family = data['font_family']
    if len(SavedTexts.objects(text_id=data['text_id'])) == 0:
        # Store data in database
        SavedTexts(
            text_id = data['text_id']
            ,text = text
            ,font_size = font_size
            ,color = color
            ,font_family = font_family
            ,width = str(width)
            ,height = str(height)
            ,top = str(top)
            ,right = str(right)
        ).save()
    else:
        # Update data in database
        SavedTexts.objects(text_id=data['text_id']).update(  
            text = text
            ,font_size = font_size
            ,color = color
            ,font_family = font_family
            ,width = str(width)
            ,height = str(height)
            ,top = str(top)
            ,right = str(right)
        )                                             
    return SavedTexts.objects(text_id=data['text_id'])[0].id
    
    
    
def allowed_file(filename):
    """ Whether or not an image file is the correct extension """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'svg']
    
    
    
@bp.route("/admin/upload-image", methods=["POST"])
@login_required
def upload_image():
    try:
        file = request.files["file"]
        
        image_id = request.headers['image-id']
        
        if secure_filename(file.filename):
            if file and allowed_file(file.filename):
                extension = file.filename.rsplit('.', 1)[1].lower()
                
                # Make sure this image has already been uploaded
                if not len(SavedImages.objects(image_id=image_id)) > 0:
                    print("Error Saving Image")
                    return 'Error Saving Image'
                
                # First try to remove the file if it already exists for the image
                try:
                    for ext in ['png', 'jpg', 'jpeg', 'svg']:
                        if path.exists(path.join(image_storage_path, f"{image_id}.{ext}")):
                            remove(path.join(image_storage_path, f"{image_id}.{ext}"))
                except Exception as e:
                    print(e)
                        
                try: 
                    # save file to specified directory
                    file.save(path.join(image_storage_path, f"{image_id}.{extension}"))
                    # Update the image mongo object with the extesion type
                    SavedImages.objects(image_id=image_id).update(
                        image_type = extension
                    )
                except Exception as e:
                    print(e)
                    return "Error saving image"
                
                print("Successful Save")
                return "Successfully Saved"
            print("Error2")
            return 'Error Saving Image'
        print("Error")
        return 'Error Saving Image'
    except Exception as e:    
        print(e)
        return 'Error Saving Image'
    
    
    
@bp.route("/admin/get-image/<image_name>", methods=["GET"])
@login_required
def get_image(image_name):
    try:
        with open(path.join(image_storage_path, f"{image_name}"), "rb") as f:
            image_binary = f.read()
            
            extension = image_name.rsplit('.')[1].lower()

            response = make_response(base64.b64encode(image_binary))
            response.headers.set('Content-Type', 'image/gif')
            response.headers.set('Content-Disposition', 'attachment', filename=f'image.{extension}')
            return response
        
        return "Error retrieving image"
    except Exception as e:
        return f"Error retrieving image: {e}" 
    


@bp.route("/admin/save-image", methods=["POST"])
@login_required
def save_image(data):
    width = data['width']
    height = data['height']
    top = data['top']
    right = data['right']
    title = data['title']
    
    if len(SavedImages.objects(image_id=data['image_id'])) == 0:
        # Store data in database
        SavedImages(
            image_id = data['image_id']
            ,title = title
            ,width = str(width)
            ,height = str(height)
            ,top = str(top)
            ,right = str(right)
            ,image_type = ""
        ).save()
    else:
        # Update data in database
        SavedImages.objects(image_id=data['image_id']).update(  
            title = title
            ,width = str(width)
            ,height = str(height)
            ,top = str(top)
            ,right = str(right)
        )                                             
        
    return SavedImages.objects(image_id=data['image_id'])[0].id
    
    
    
@bp.route("/admin/save-network", methods=["POST"])
@login_required
def save_network():
    data = request.form.to_dict()
    # print(data)
    
    for string in data:
        # Data is sent as a string inside an object, parse it
        data = loads(string)
    
        network_id = data['uuid']
        network_width = data["width"]
        network_height =  data["height"]
        network_top = data["top"]
        network_right = data["right"]
        network_title = data["name"]
        network_color = data["color"]
        
        if len(SavedNetworks.objects(network_id=network_id)) == 0:
            new_network = SavedNetworks(
                network_id = network_id
                ,width = network_width
                ,height = network_height
                ,top = network_top
                ,right = network_right
                ,background_color = network_color
                ,title_text = network_title
            ).save()
            
            network_edges = []
            network_nodes = []
            
            for node in data["nodes"]:
                # print(node)
                # print()
                
                new_node = NetworkNode(
                    linked_network_id = str(new_network.id)
                    ,label = node["attributes"]["label"]
                    ,x_pos = str(node["attributes"]["x"])
                    ,y_pos = str(node["attributes"]["y"])
                    ,size = str(node["attributes"]["size"])
                    ,color = node["attributes"]["default-color"]
                    ,additional_info = node["attributes"]["additional-information"]
                ).save()
                network_nodes.append(new_node)
                
            for edge in data["edges"]:
                # print(edge)
                # print()
                
                new_edge = NetworkEdge(
                    size = str(edge["attributes"]["size"])
                    ,color = edge["attributes"]["default-color"]
                    ,edge_type = edge["attributes"]["type"]
                    ,source_node = NetworkNode.objects(label=edge["source"], linked_network_id=str(new_network.id))[0]
                    ,target_node = NetworkNode.objects(label=edge["target"], linked_network_id=str(new_network.id))[0]
                ).save()
                network_edges.append(new_edge)
                
            SavedNetworks.objects(id=str(new_network.id)).update(
                nodes = network_nodes
                ,edges = network_edges   
            )
        else: 
            SavedNetworks.objects(network_id = network_id).update(
                width = network_width
                ,height = network_height
                ,top = network_top
                ,right = network_right
                ,background_color = network_color
            )
            
            network_edges = []
            network_nodes = []
            
            # for node in data["nodes"]:
            #     # print(node)
            #     # print()
                
            #     new_node = NetworkNode(
            #         linked_network_id = str(new_network.id)
            #         ,label = node["attributes"]["label"]
            #         ,x_pos = str(node["attributes"]["x"])
            #         ,y_pos = str(node["attributes"]["y"])
            #         ,size = str(node["attributes"]["size"])
            #         ,color = node["attributes"]["default-color"]
            #         ,additional_info = node["attributes"]["additional-information"]
            #     ).save()
            #     network_nodes.append(new_node)
                
            # for edge in data["edges"]:
            #     # print(edge)
            #     # print()
                
            #     new_edge = NetworkEdge(
            #         size = str(edge["attributes"]["size"])
            #         ,color = edge["attributes"]["default-color"]
            #         ,edge_type = edge["attributes"]["type"]
            #         ,source_node = NetworkNode.objects(label=edge["source"], linked_network_id=str(new_network.id))[0]
            #         ,target_node = NetworkNode.objects(label=edge["target"], linked_network_id=str(new_network.id))[0]
            #     ).save()
            #     network_edges.append(new_edge)
                
            # SavedNetworks.objects(id=str(new_network.id)).update(
            #     nodes = network_nodes
            #     ,edges = network_edges   
            # )
    
    return ''



@bp.route("/admin/save-dashboard", methods=['POST'])
@login_required
def save_dashboard():
    data = request.form.to_dict()
    
    for string in data:
        # Data is sent as a string inside an object, parse it
        data = loads(string)
        # Get data
        dashboard_title = data["dashboard_title"]
        dashboard_height = data["dashboard_height"]
        dashboard_id = data["dashboard_id"]
        dashboard_color = data["dashboard_color"]
        
        print(f"DASH ID: {dashboard_id}")
        
        # Check if dashboard already exists
        # Save our dashboard
        if dashboard_id == "":
            dashboard_id = SavedDashboards(
                dashboard_title = dashboard_title
                ,dashboard_height = dashboard_height
                ,dashboard_color = dashboard_color
            ).save()
            dashboard_id = dashboard_id.id
        elif len(SavedDashboards.objects(id=dashboard_id)) == 0:
            dashboard_id = SavedDashboards(
                dashboard_title = dashboard_title
                ,dashboard_height = dashboard_height
                ,dashboard_color = dashboard_color
            ).save()
            dashboard_id = dashboard_id.id
        else:
            # Othewise update our dashboard
            SavedDashboards.objects(id=dashboard_id).update(
                dashboard_title = dashboard_title
                ,dashboard_height = dashboard_height
                ,dashboard_color = dashboard_color
            )
        
        # Loop through and save our charts
        for chart in data["charts"]:
            
            # Save our chart if it is not already saved in the database
            result = save_chart(chart)
            # Save the entry to the ItemInDashboard collection
            if len(ItemInDashboard.objects(item_id=str(result), dashboard_reference=SavedDashboards.objects(id=dashboard_id)[0].id)) == 0:
                ItemInDashboard(
                    dashboard_reference = SavedDashboards.objects(id=dashboard_id)[0]
                    ,item_id = str(result)
                    ,item_type = "chart"
                    ,width = str(chart['width'])
                    ,height = str(chart['height'])
                    ,top = str(chart['top'])
                    ,right = str(chart['right'])
                ).save()
            else:
                # If we are updating we need all of the preference dashboard references as well
                ItemInDashboard.objects(item_id=str(result), dashboard_reference=SavedDashboards.objects(id=dashboard_id)[0].id).update(
                    item_id = str(result)
                    ,item_type = "chart"
                    ,width = str(chart['width'])
                    ,height = str(chart['height'])
                    ,top = str(chart['top'])
                    ,right = str(chart['right'])
                )
            
        for text in data["texts"]:
            # Save our text if it is not already saved in the database
            result = save_text(text)
            # Save the entry to the ItemInDashboard collection
            if len(ItemInDashboard.objects(item_id=str(result), dashboard_reference=SavedDashboards.objects(id=dashboard_id)[0].id)) == 0:
                ItemInDashboard(
                    dashboard_reference = SavedDashboards.objects(id=dashboard_id)[0]
                    ,item_id = str(result)
                    ,item_type = "text"
                    ,width = str(text['width'])
                    ,height = str(text['height'])
                    ,top = str(text['top'])
                    ,right = str(text['right'])
                ).save()
            else:
                # If we are updating we need all of the preference dashboard references as well
                ItemInDashboard.objects(item_id=str(result), dashboard_reference=SavedDashboards.objects(id=dashboard_id)[0].id).update(
                    item_id = str(result)
                    ,item_type = "text"
                    ,width = str(text['width'])
                    ,height = str(text['height'])
                    ,top = str(text['top'])
                    ,right = str(text['right'])
                )
                   
            
        for image in data["images"]:
            # Save our image if it is not already saved in the database
            result = save_image(image)
            # Save the entry to the ItemInDashboard collection
            if len(ItemInDashboard.objects(item_id=str(result), dashboard_reference=SavedDashboards.objects(id=dashboard_id)[0].id)) == 0:
                ItemInDashboard(
                    dashboard_reference = SavedDashboards.objects(id=dashboard_id)[0]
                    ,item_id = str(result)
                    ,item_type = "image"
                    ,width = str(image['width'])
                    ,height = str(image['height'])
                    ,top = str(image['top'])
                    ,right = str(image['right'])
                ).save()
            else:
                # If we are updating we need all of the preference dashboard references as well
                ItemInDashboard.objects(item_id=str(result), dashboard_reference=SavedDashboards.objects(id=dashboard_id)[0].id).update(
                    item_id = str(result)
                    ,item_type = "image"
                    ,width = str(image['width'])
                    ,height = str(image['height'])
                    ,top = str(image['top'])
                    ,right = str(image['right'])
                )
                   
            
    return {"status": "success", "dashboard_id": str(dashboard_id)}



@bp.route("/admin/dashboards/get_all_dashboards", methods=["GET"])
@login_required
def retrieve_dashboards():
    # Get all dashboards
    dashboards = SavedDashboards.objects.to_json()
    # Return both
    return dashboards



@bp.route("/admin/charts/get_charts_by_dashboard_id/<dashboard_id>", methods=["GET"])
@login_required
def retrieve_charts_by_dashboard_id(dashboard_id):
    # Get our dashboard
    dashboard = SavedDashboards.objects(id=dashboard_id).to_json()
    return_charts = []
    dashboard = loads(dashboard)[0]
    # Loop through all of our dashboard chart items
    for item in ItemInDashboard.objects(dashboard_reference=dashboard_id, item_type="chart"):
        # Get the chart object for this
        chart_data = loads(SavedCharts.objects(id=item.item_id).to_json())[0]
        # Add the extra dashboard-specific information to chart_data
        chart_data["width"] = item.width
        chart_data["height"] = item.height
        chart_data["top"] = item.top
        chart_data["right"] = item.right
        return_charts.append(chart_data)
        
    # Return our charts
    return json_util.dumps(return_charts)



@bp.route("/admin/texts/get_texts_by_dashboard_id/<dashboard_id>", methods=["GET"])
@login_required
def retrieve_texts_by_dashboard_id(dashboard_id):
    # Get our dashboard
    dashboard = SavedDashboards.objects(id=dashboard_id).to_json()
    return_texts = []
    dashboard = loads(dashboard)[0]
    # Loop through all of our dashboard text items
    for item in ItemInDashboard.objects(dashboard_reference=dashboard_id, item_type="text"):
        # Get the text object for this
        text_data = loads(SavedTexts.objects(id=item.item_id).to_json())[0]
        # Add the extra dashboard-specific information to text_data
        text_data["width"] = item.width
        text_data["height"] = item.height
        text_data["top"] = item.top
        text_data["right"] = item.right
        return_texts.append(text_data)
        
    # Return our texts
    return json_util.dumps(return_texts)



@bp.route("/admin/images/get_images_by_dashboard_id/<dashboard_id>", methods=["GET"])
@login_required
def retrieve_images_by_dashboard_id(dashboard_id):
    # Get our dashboard
    dashboard = SavedDashboards.objects(id=dashboard_id).to_json()
    return_images = []
    dashboard = loads(dashboard)[0]
    # Loop through all of our dashboard image items
    for item in ItemInDashboard.objects(dashboard_reference=dashboard_id, item_type="image"):
        # Get the image object for this
        image_data = loads(SavedImages.objects(id=item.item_id).to_json())[0]
        # Add the extra dashboard-specific information to image_data
        image_data["width"] = item.width
        image_data["height"] = item.height
        image_data["top"] = item.top
        image_data["right"] = item.right
        return_images.append(image_data)
        
    # Return our images
    return json_util.dumps(return_images)
    
    

@bp.route("/admin/delete-chart", methods=["DELETE"])
@login_required
def delete_chart():
    data = request.form.to_dict()
    for string in data:
        # Data is sent as a string inside an object, parse it
        data = loads(string)
        # Get data
        chart_id = data["chart_id"]
        # Delete our chart if it is not used in any dashboards
        for dashboard in SavedDashboards.objects:
            for chart in dashboard["dashboard_charts"]:
                charts = SavedCharts.objects(id=chart.id)
                if len(charts) > 0:
                    chart = charts[0]
                    if chart.chart_id == chart_id:
                        # Chart is in use, just mark is for deletion later 
                        # when the dashboard is used
                        print("Marking for deletion")
                        SavedCharts.objects(chart_id=chart_id).update(
                            deleted = True
                        )
                        return "Success"
     
    print("Regular deleted")
    # If we don't find the chart in any dashboards, delete it   
    SavedCharts.objects(chart_id=chart_id).delete()
    
    return 'Success'
    


@bp.route("/admin/delete-dashboard", methods=["DELETE"])
@login_required
def delete_dashboard():
    data = request.form.to_dict()
    for string in data:
        # Data is sent as a string inside an object, parse it
        data = loads(string)
        # Get data
        dashboard_id = data["dashboard_id"]
        # Delete charts in our dashboard if they were previously marked for deleted. 
        # Right now if a user delete a chart, it isn't actually deleted from the database, 
        # just marked for deletion until the dashboard it is used in is deleted.
        for chart in SavedDashboards.objects(id=dashboard_id)[0]["dashboard_charts"]:
            SavedCharts.objects(id=chart.id, deleted=True).delete()
        # Delete our texts
        for text in SavedDashboards.objects(id=dashboard_id)[0]["dashboard_texts"]:
            SavedTexts.objects(id=text.id).delete()
        # Delete our images
        for image in SavedDashboards.objects(id=dashboard_id)[0]["dashboard_images"]:
            SavedImages.objects(id=image.id).delete()
            # Delete our image from the file system
            image_id = image.image_id
            ext = image.image_type
            print(f"{image_id}.{ext}")
            if path.exists(path.join(image_storage_path, f"{image_id}.{ext}")):
                remove(path.join(image_storage_path, f"{image_id}.{ext}"))
        
        # Delete our dashboard
        SavedDashboards.objects(id=dashboard_id).delete()
        return "Success"
    
    return 'Success'