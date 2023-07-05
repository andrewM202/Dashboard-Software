from flask import render_template, Blueprint, send_from_directory, request, make_response, jsonify
from flask_login import  current_user
from flask_security import login_required
from models import (SavedCharts, SavedDashboards, SavedTexts, SavedImages, 
    db, SavedNetworks, SavedTimelines, TimelineDate, ItemInDashboard, NetworkNode, 
    NetworkEdge, SavedTables, ChartDataset)
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
def update_save_chart(data=None):
    data_originally_none = True
    datasets = []
    labels = []
    if data is None:
        data = request.form.to_dict()
        data_originally_none = True
        datasets = loads(data["data[datasets]"])
        labels = loads(data["data[labels]"])
    else:
        data_originally_none = False
        datasets = loads(data["data"]["datasets"])
        labels = loads(data["data"]["labels"])
        
    
    to_save_datasets = []
    for dataset in datasets:
        to_save_datasets.append(ChartDataset(
            background_color = str(dataset['backgroundColor'])
            ,border_color = str(dataset['borderColor'])
            ,bar_thickness = str(dataset['barThickness'])
            ,data = dataset['data']
            ,fill = str(dataset['fill'])
            ,label = str(dataset['label'])
            ,pointBackgroundColor = str(dataset['pointBackgroundColor'])
            ,pointRadius = str(dataset['pointRadius'])
        ))
    
    # Check if this chart already exists
    # If it does, update otherwise save
    if len(SavedCharts.objects(chart_id=data['chart_id'])) > 0:
        print("Save chart")
        
        # Update dashboard
        SavedCharts.objects(chart_id=str(data['chart_id'])).update(   
            background_color = str(data['background_color'])

            ,chart_type = str(data['chart_type'])
            ,legend_enabled = str(data['legend_enabled'])
            
            ,yaxes_scale_label = str(data['yaxes_scale_label'])
            ,xaxes_scale_label = str(data['xaxes_scale_label'])
            
            ,yaxes_scale_label_enabled = str(data['yaxes_scale_label_enabled'])
            ,xaxes_scale_label_enabled = str(data['xaxes_scale_label_enabled'])

            ,yaxes_gridlines_color = str(data['yaxes_gridlines_color'])
            ,xaxes_gridlines_color = str(data['xaxes_gridlines_color'])
            
            ,yaxes_scalelabel_color = str(data['yaxes_scalelabel_color'])
            ,xaxes_scalelabel_color = str(data['xaxes_scalelabel_color'])
            
            ,legend_font_color = str(data['legend_font_color'])
            
            ,yaxes_tick_color = str(data['yaxes_tick_color'])
            ,xaxes_tick_color = str(data['xaxes_tick_color'])
            
            ,yaxes_gridline_enabled = str(data['yaxes_gridline_enabled'])
            ,xaxes_gridline_enabled = str(data['xaxes_gridline_enabled'])
            
            ,title_fontsize = str(data['title_fontsize'])
            ,title_fontcolor = str(data['title_fontcolor'])
            ,title_text = str(data['title_text'])
            ,title_enabled = str(data['title_enabled'])
            
            ,default_font_family = str(data['default_font_family'])
            
            ,chart_padding = str(data['chart_padding'])
            
            ,datasets = to_save_datasets
            ,labels = labels
            
            ,deleted = False
        )
    else:
        # Store data in database
        SavedCharts(  
            chart_id = str(data['chart_id'])
            ,background_color = str(data['background_color'])

            ,chart_type = str(data['chart_type'])
            ,legend_enabled = str(data['legend_enabled'])
            
            ,yaxes_scale_label = str(data['yaxes_scale_label'])
            ,xaxes_scale_label = str(data['xaxes_scale_label'])
            
            ,yaxes_scale_label_enabled = str(data['yaxes_scale_label_enabled'])
            ,xaxes_scale_label_enabled = str(data['xaxes_scale_label_enabled'])

            ,yaxes_gridlines_color = str(data['yaxes_gridlines_color'])
            ,xaxes_gridlines_color = str(data['xaxes_gridlines_color'])
            
            ,yaxes_scalelabel_color = str(data['yaxes_scalelabel_color'])
            ,xaxes_scalelabel_color = str(data['xaxes_scalelabel_color'])
            
            ,legend_font_color = str(data['legend_font_color'])
            
            ,yaxes_tick_color = str(data['yaxes_tick_color'])
            ,xaxes_tick_color = str(data['xaxes_tick_color'])
            
            ,yaxes_gridline_enabled = str(data['yaxes_gridline_enabled'])
            ,xaxes_gridline_enabled = str(data['xaxes_gridline_enabled'])
            
            ,title_fontsize = str(data['title_fontsize'])
            ,title_fontcolor = str(data['title_fontcolor'])
            ,title_text = str(data['title_text'])
            ,title_enabled = str(data['title_enabled'])
            
            ,default_font_family = str(data['default_font_family'])
            
            ,chart_padding = str(data['chart_padding'])
            
            ,datasets = to_save_datasets
            ,labels = labels
            
            ,deleted = False
        ).save()
    
    if data_originally_none:
        return 'Success'
    else:
        return SavedCharts.objects(chart_id=data['chart_id'])[0].id


@bp.route("/admin/networks", methods=["GET"])
@login_required
def get_networks():
    networks = loads(SavedNetworks.objects().to_json())
    for i in range(0, len(networks)):
        for node_index in range(0, len(networks[i]['nodes'])):
            new_json = NetworkNode.objects(id=networks[i]['nodes'][node_index]["$oid"])[0].to_json()  
            networks[i]['nodes'][node_index] = loads(new_json)
            
        for edge_index in range(0, len(networks[i]['edges'])):
            new_json = loads(NetworkEdge.objects(id=networks[i]['edges'][edge_index]["$oid"])[0].to_json())
            new_json["source_node"] = NetworkNode.objects(id=new_json["source_node"]["$oid"])[0].label
            new_json["target_node"] = NetworkNode.objects(id=new_json["target_node"]["$oid"])[0].label
            networks[i]['edges'][edge_index] = new_json
            
    return json_util.dumps(networks)



@bp.route("/admin/charts", methods=["GET"])
@login_required
def get_charts():
    return SavedCharts.objects.filter(deleted=False).to_json()



@bp.route("/admin/timelines", methods=["GET"])
@login_required
def get_timelines():
    return SavedTimelines.objects.to_json()



@bp.route("/admin/tables-preliminary", methods=["GET"])
@login_required
def get_tables():
    return SavedTables.objects.to_json()



@bp.route("/admin/images", methods=["GET"])
@login_required
def get_images():
    return SavedImages.objects.filter().to_json()



@bp.route("/admin/save-table", methods=["POST"])
@login_required
def save_table(new_data=None):
    data_originally_none = True
    if new_data is None:
        # Get request data
        new_data = request.form.to_dict()
        data_originally_none = True
    else:
        data_originally_none = False
        
    # Get data from dict
    uuid = new_data['uuid']
    title = new_data["tableName"]
    color = new_data['tableColor']
    top = new_data['top']
    right = new_data['right']
    width = new_data['width']
    height = new_data['height']
    # Save table to database if it doesn't exist
    if len(SavedTables.objects(table_id=uuid)) == 0:
        SavedTables(
            table_id = uuid
            ,title = title
            ,background_color = color
            ,width = width
            ,height = height
            ,top = top
            ,right = right
            ,column_names = loads(new_data["columnNames"])
            ,data = loads(new_data["data"])
        ).save()
    # Update the data if it does exist
    else:
        SavedTables.objects(table_id=uuid).update(
            title = title
            ,background_color = color
            ,width = width
            ,height = height
            ,top = top
            ,right = right
            ,column_names = loads(new_data["columnNames"])
            ,data = loads(new_data["data"])
        )
        
    if data_originally_none:
        return 'success'
    else:
        return SavedTables.objects(table_id=uuid)[0].id



@bp.route("/admin/save-timeline", methods=["POST"])
@login_required
def save_timeline(new_data=None):
    data_originally_none = True
    if new_data is None:
        # Get request data
        new_data = request.form.to_dict()
        data_originally_none = True
    else:
        data_originally_none = False
    
    if data_originally_none:
        for data in new_data:
            data = loads(data)
            # Get data now that its processed
            uuid = data['uuid']
            title = data['title']
            color = data['color']
            items = data['timeline_items']
            # Check if this timeline has already been saved
            if len(SavedTimelines.objects(timeline_id=uuid)) > 0:
                dates_processed = []
                for item in items:
                    new_date = TimelineDate(
                        date_id = item['uuid']
                        ,date = item['date']
                        ,text = item['content']
                    )
                    dates_processed.append(new_date)
                SavedTimelines.objects(timeline_id=uuid).update(
                    color = color
                    ,title = title     
                    ,dates = dates_processed 
                )
            else:
                dates_processed = []
                for item in items:
                    new_date = TimelineDate(
                        date_id = item['uuid']
                        ,date = item['date']
                        ,text = item['content']
                    )
                    dates_processed.append(new_date)
                SavedTimelines(
                    timeline_id = uuid
                    ,color = color
                    ,title = title
                    ,dates = dates_processed
                ).save()
    else:
        data = new_data
        # Get data now that its processed
        uuid = data['uuid']
        title = data['title']
        color = data['color']
        items = data['timeline_items']
        # Check if this timeline has already been saved
        if len(SavedTimelines.objects(timeline_id=uuid)) > 0:
            dates_processed = []
            for item in items:
                new_date = TimelineDate(
                    date_id = item['uuid']
                    ,date = item['date']
                    ,text = item['content']
                )
                dates_processed.append(new_date)
            SavedTimelines.objects(timeline_id=uuid).update(
                color = color
                ,title = title     
                ,dates = dates_processed 
            )
        else:
            dates_processed = []
            for item in items:
                new_date = TimelineDate(
                    date_id = item['uuid']
                    ,date = item['date']
                    ,text = item['content']
                )
                dates_processed.append(new_date)
            SavedTimelines(
                timeline_id = uuid
                ,color = color
                ,title = title
                ,dates = dates_processed
            ).save()
 
    if data_originally_none:
        return 'success'
    else:
        return SavedTimelines.objects(timeline_id=data['uuid'])[0].id       



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
                    return "Error saving image"
                        
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
    


def save_image_helper(data):
    title = data['title']
    
    if len(SavedImages.objects(image_id=data['image_id'])) == 0:
        # Store data in database
        SavedImages(
            image_id = data['image_id']
            ,title = title
            ,image_type = ""
        ).save()
    else:
        # Update data in database
        SavedImages.objects(image_id=data['image_id']).update(  
            title = title
        )                                             
        
    return SavedImages.objects(image_id=data['image_id'])[0].id



@bp.route("/admin/save-image", methods=["POST"])
@login_required
def save_image():
    data = request.form.to_dict()
    title = data['title']
    
    if len(SavedImages.objects(image_id=data['image_id'])) == 0:
        # Store data in database
        SavedImages(
            image_id = data['image_id']
            ,title = title
            ,image_type = ""
        ).save()
    else:
        # Update data in database
        SavedImages.objects(image_id=data['image_id']).update(  
            title = title
        )                                             
        
    return "Sucess"
    
    
    
@bp.route("/admin/delete-network", methods=["DELETE"])
@login_required
def delete_network():
    """ Delete a network and all associated nodes, edges """ 
    data = request.form.to_dict()
    for string in data:
        # Data is sent as a string inside an object, parse it
        data = loads(string)
        # Get data
        network_id = data["item_id"]
        # Delete all associated edges
        for edge in SavedNetworks.objects(network_id=network_id)[0].edges:
            edge.delete()
        # Delete all associated nodes
        for node in SavedNetworks.objects(network_id=network_id)[0].nodes:
            node.delete()
        # Delete the network
        SavedNetworks.objects(network_id=network_id).delete()
        
    return "success"



@bp.route("/admin/delete-table", methods=["DELETE"])
@login_required
def delete_table():
    """ Delete a table and all associated columns, rows """
    data = request.form.to_dict()
    for string in data:
        # Data is sent as a string inside an object, parse it
        data = loads(string)
        # Get data
        table_id = data["item_id"]
        # Delete the table
        SavedTables.objects(table_id=table_id).delete()
        
    return "success"



@bp.route("/admin/delete-timeline", methods=["DELETE"])
@login_required
def timeline():
    """ Delete a timeline """
    data = request.form.to_dict()
    for string in data:
        # Data is sent as a string inside an object, parse it
        data = loads(string)
        # Get data
        timeline_id = data["item_id"]
        # Delete the table
        SavedTimelines.objects(timeline_id=timeline_id).delete()
        
    return "success"


    
@bp.route("/admin/save-network", methods=["POST"])
@login_required
def save_network(data=None):
    data_originally_none = True
    if data is None:
        data = request.form.to_dict()
        data_originally_none = True
    else:
        data_originally_none = False
        
    for string in data:
        if data_originally_none:
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
                new_node = NetworkNode(
                    uuid = str(node["attributes"]["uuid"])
                    ,linked_network_id = str(new_network.id)
                    ,label = str(node["attributes"]["label"])
                    ,key = str(node["key"])
                    ,x_pos = str(node["attributes"]["x"])
                    ,y_pos = str(node["attributes"]["y"])
                    ,node_size = str(node["attributes"]["size"])
                    ,color = node["attributes"]["default-color"]
                    ,additional_info = node["attributes"]["additional-information"]
                ).save()
                network_nodes.append(new_node)
                
            for edge in data["edges"]:
                new_edge = NetworkEdge(
                    uuid = str(edge["attributes"]["uuid"])
                    ,edge_size = str(edge["attributes"]["size"])
                    ,color = edge["attributes"]["default-color"]
                    ,edge_type = edge["attributes"]["type"]
                    ,source_node = NetworkNode.objects(key=str(edge["source"]), linked_network_id=str(new_network.id))[0]
                    ,target_node = NetworkNode.objects(key=str(edge["target"]), linked_network_id=str(new_network.id))[0]
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
                ,title_text = network_title
            )
            
            network_edges = []
            network_nodes = []
            
            for node in data["nodes"]:
                # Save node if it doesn't exist
                if len(NetworkNode.objects(uuid=str(node["attributes"]["uuid"]))) == 0:
                    new_node = NetworkNode(
                        linked_network_id = str(SavedNetworks.objects(network_id = network_id)[0].id)
                        ,uuid = str(node["attributes"]["uuid"])
                        ,label = str(node["attributes"]["label"])
                        ,key = str(node["key"])
                        ,x_pos = str(node["attributes"]["x"])
                        ,y_pos = str(node["attributes"]["y"])
                        ,node_size = str(node["attributes"]["size"])
                        ,color = str(node["attributes"]["default-color"])
                        ,additional_info = str(node["attributes"]["additional-information"])
                    ).save()
                    network_nodes.append(new_node)
                # Update node if it does exist
                else:
                    NetworkNode.objects(uuid=str(node["attributes"]["uuid"]), linked_network_id=str(SavedNetworks.objects(network_id = network_id)[0].id)).update(
                        label = str(node["attributes"]["label"])
                        ,node_size = str(node["attributes"]["size"])
                        ,key = str(node["key"])
                        ,x_pos = str(node["attributes"]["x"])
                        ,y_pos = str(node["attributes"]["y"])
                        ,color = str(node["attributes"]["default-color"])
                        ,additional_info = str(node["attributes"]["additional-information"])
                    )
                    network_nodes.append(NetworkNode.objects(uuid=str(node["attributes"]["uuid"]))[0])
                
            for edge in data["edges"]:
                # Save edge if it doesn't exist
                if len(NetworkEdge.objects(uuid=str(edge["attributes"]["uuid"]))) == 0:
                    new_edge = NetworkEdge(
                        edge_size = str(edge["attributes"]["size"])
                        ,uuid = str(edge["attributes"]["uuid"])
                        ,color = edge["attributes"]["default-color"]
                        ,edge_type = edge["attributes"]["type"]
                        ,source_node = NetworkNode.objects(key=edge["source"], linked_network_id=str(SavedNetworks.objects(network_id = network_id)[0].id))[0]
                        ,target_node = NetworkNode.objects(key=edge["target"], linked_network_id=str(SavedNetworks.objects(network_id = network_id)[0].id))[0]
                    ).save()
                    network_edges.append(new_edge)
                # Update edge if it does exist
                else:
                    NetworkEdge.objects(uuid=str(edge["attributes"]["uuid"])).update(
                        edge_size = str(edge["attributes"]["size"])
                        ,color = edge["attributes"]["default-color"]
                        ,edge_type = edge["attributes"]["type"]
                        ,source_node = NetworkNode.objects(key=edge["source"], linked_network_id=str(SavedNetworks.objects(network_id = network_id)[0].id))[0]
                        ,target_node = NetworkNode.objects(key=edge["target"], linked_network_id=str(SavedNetworks.objects(network_id = network_id)[0].id))[0]
                    )
                    network_edges.append(NetworkEdge.objects(uuid=str(edge["attributes"]["uuid"]))[0])

            SavedNetworks.objects(id=str(SavedNetworks.objects(network_id = network_id)[0].id)).update(
                nodes = network_nodes
                ,edges = network_edges   
            )
            
    if data_originally_none:
        return 'success'
    else:
        return SavedNetworks.objects(network_id=network_id)[0].id
    
    return 'success'



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
            result = update_save_chart(chart)
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
            result = save_image_helper(image)
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
                
        for table in data["tables"]:
            # Save our table if it is not already saved in the database
            result = save_table(table)
            # Save the entry to the ItemInDashboard collection
            if len(ItemInDashboard.objects(item_id=str(result), dashboard_reference=SavedDashboards.objects(id=dashboard_id)[0].id)) == 0:
                ItemInDashboard(
                    dashboard_reference = SavedDashboards.objects(id=dashboard_id)[0]
                    ,item_id = str(result)
                    ,item_type = "table"
                    ,width = str(table['width'])
                    ,height = str(table['height'])
                    ,top = str(table['top'])
                    ,right = str(table['right'])
                ).save()
            else:
                # If we are updating we need all of the preference dashboard references as well
                ItemInDashboard.objects(item_id=str(result), dashboard_reference=SavedDashboards.objects(id=dashboard_id)[0].id).update(
                    item_id = str(result)
                    ,item_type = "table"
                    ,width = str(table['width'])
                    ,height = str(table['height'])
                    ,top = str(table['top'])
                    ,right = str(table['right'])
                )
            
        for network in data["networks"]:
            # Save our network if it is not already saved in the database
            result = save_network(network)
            # Save the entry to the ItemInDashboard collection
            if len(ItemInDashboard.objects(item_id=str(result), dashboard_reference=SavedDashboards.objects(id=dashboard_id)[0].id)) == 0:
                ItemInDashboard(
                    dashboard_reference = SavedDashboards.objects(id=dashboard_id)[0]
                    ,item_id = str(result)
                    ,item_type = "network"
                    ,width = str(network['width'])
                    ,height = str(network['height'])
                    ,top = str(network['top'])
                    ,right = str(network['right'])
                ).save()
            else:
                # If we are updating we need all of the preference dashboard references as well
                ItemInDashboard.objects(item_id=str(result), dashboard_reference=SavedDashboards.objects(id=dashboard_id)[0].id).update(
                    item_id = str(result)
                    ,item_type = "network"
                    ,width = str(network['width'])
                    ,height = str(network['height'])
                    ,top = str(network['top'])
                    ,right = str(network['right'])
                )
            
        for timeline in data["timelines"]:
            # Save our timeline if it is not already saved in the database
            result = save_timeline(timeline)
            # Save the entry to the ItemInDashboard collection
            if len(ItemInDashboard.objects(item_id=str(result), dashboard_reference=SavedDashboards.objects(id=dashboard_id)[0].id)) == 0:
                ItemInDashboard(
                    dashboard_reference = SavedDashboards.objects(id=dashboard_id)[0]
                    ,item_id = str(result)
                    ,item_type = "timeline"
                    ,width = str(timeline['width'])
                    ,height = str(timeline['height'])
                    ,top = str(timeline['top'])
                    ,right = str(timeline['right'])
                ).save()
            else:
                # If we are updating we need all of the preference dashboard references as well
                ItemInDashboard.objects(item_id=str(result), dashboard_reference=SavedDashboards.objects(id=dashboard_id)[0].id).update(
                    item_id = str(result)
                    ,item_type = "timeline"
                    ,width = str(timeline['width'])
                    ,height = str(timeline['height'])
                    ,top = str(timeline['top'])
                    ,right = str(timeline['right'])
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



@bp.route("/admin/networks/get_networks_by_dashboard_id/<dashboard_id>", methods=["GET"])
@login_required
def retrieve_networks_by_dashboard_id(dashboard_id):
    # Get our dashboard
    dashboard = SavedDashboards.objects(id=dashboard_id).to_json()
    return_networks = []
    dashboard = loads(dashboard)[0]
    # Loop through all of our dashboard network items
    for item in ItemInDashboard.objects(dashboard_reference=dashboard_id, item_type="network"):
        # Get the image object for this
        network_data = loads(SavedNetworks.objects(id=item.item_id).to_json())
        for i in range(0, len(network_data)):
            for node_index in range(0, len(network_data[i]['nodes'])):
                new_json = NetworkNode.objects(id=network_data[i]['nodes'][node_index]["$oid"])[0].to_json()  
                network_data[i]['nodes'][node_index] = loads(new_json)
                
            for edge_index in range(0, len(network_data[i]['edges'])):
                new_json = loads(NetworkEdge.objects(id=network_data[i]['edges'][edge_index]["$oid"])[0].to_json())
                new_json["source_node"] = NetworkNode.objects(id=new_json["source_node"]["$oid"])[0].label
                new_json["target_node"] = NetworkNode.objects(id=new_json["target_node"]["$oid"])[0].label
                network_data[i]['edges'][edge_index] = new_json
        network_data = network_data[0]
        # Add the extra dashboard-specific information to network_data
        network_data["width"] = item.width
        network_data["height"] = item.height
        network_data["top"] = item.top
        network_data["right"] = item.right
        return_networks.append(network_data)
        
        networks = loads(SavedNetworks.objects().to_json())
        
    # Return our networks
    return json_util.dumps(return_networks)


@bp.route("/admin/timelines/get_timelines_by_dashboard_id/<dashboard_id>", methods=["GET"])
@login_required
def retrieve_timelines_by_dashboard_id(dashboard_id):
    # Get our dashboard
    dashboard = SavedDashboards.objects(id=dashboard_id).to_json()
    return_timelines = []
    dashboard = loads(dashboard)[0]
    # Loop through all of our dashboard timeline items
    for item in ItemInDashboard.objects(dashboard_reference=dashboard_id, item_type="timeline"):
        # Get the image object for this
        timeline_data = loads(SavedTimelines.objects(id=item.item_id).to_json())[0]
        # Add the extra dashboard-specific information to timeline_data
        timeline_data["width"] = item.width
        timeline_data["height"] = item.height
        timeline_data["top"] = item.top
        timeline_data["right"] = item.right
        return_timelines.append(timeline_data)
        
    # Return our timelines
    return json_util.dumps(return_timelines)



@bp.route("/admin/tables/get_tables_by_dashboard_id/<dashboard_id>", methods=["GET"])
@login_required
def retrieve_tables_by_dashboard_id(dashboard_id):
    # Get our dashboard
    dashboard = SavedDashboards.objects(id=dashboard_id).to_json()
    return_tables = []
    dashboard = loads(dashboard)[0]
    # Loop through all of our dashboard table items
    for item in ItemInDashboard.objects(dashboard_reference=dashboard_id, item_type="table"):
        # Get the image object for this
        table_data = loads(SavedTables.objects(id=item.item_id).to_json())[0]
        # Add the extra dashboard-specific information to table_data
        table_data["width"] = item.width
        table_data["height"] = item.height
        table_data["top"] = item.top
        table_data["right"] = item.right
        return_tables.append(table_data)
        
    # Return our tables
    return json_util.dumps(return_tables)
    
    

@bp.route("/admin/delete-chart", methods=["DELETE"])
@login_required
def delete_chart():
    data = request.form.to_dict()
    for string in data:
        # Data is sent as a string inside an object, parse it
        data = loads(string)
        # Get data
        chart_id = data["item_id"]
        # Delete our chart if it is not used in any dashboards
        if len(ItemInDashboard.objects(item_id=chart_id)) > 0:
            # Chart is in use, just mark is for deletion later 
            # when the dashboard is used
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
        
        # Get all of the items in the dashboard
        for item in ItemInDashboard.objects(dashboard_reference=dashboard_id):
            # Get the item type
            item_type = item.item_type
            # Get the item id
            item_id = item.item_id
            # Delete the item
            if item_type == "chart":
                SavedCharts.objects(chart_id=item_id).delete()
            elif item_type == "text":
                SavedTexts.objects(text_id=item_id).delete()
            elif item_type == "image":
                image = SavedImages.objects(id=item_id)[0]
                # Delete our image from the file system
                image_id = image.image_id
                ext = image.image_type
                SavedImages.objects(id=item_id).delete()
                print(f"{image_id}.{ext}")
                if path.exists(path.join(image_storage_path, f"{image_id}.{ext}")):
                    remove(path.join(image_storage_path, f"{image_id}.{ext}"))
                    
        # Delete our items in dashboard
        ItemInDashboard.objects(dashboard_reference=dashboard_id).delete()
  
        # Delete our dashboard
        SavedDashboards.objects(id=dashboard_id).delete()
        return "Success"
    
    return 'Success'