from flask import render_template, Blueprint, send_from_directory, request, make_response
from flask_login import  current_user
from flask_security import login_required
from models import SavedCharts, SavedDashboards, SavedTexts, SavedImages, db
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



@bp.route("/admin/charts", methods=["GET"])
@login_required
def get_charts():
    return SavedCharts.objects.filter(deleted=False).to_json()



@bp.route("/admin/save-chart")
@login_required
def save_chart(data):
    width = data['width']
    height = data['height']
    top = data['top']
    right = data['right']
    data = data["data"]
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
            
            ,width = str(width)
            ,height = str(height)
            ,top = str(top)
            ,right = str(right)
            
            ,deleted = False
        ).save()
        return "Chart Saved"
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
            
            ,width = str(width)
            ,height = str(height)
            ,top = str(top)
            ,right = str(right)
            
            ,deleted = False
        )
        return "Chart Updated"



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
        return "Text Saved"
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
        return "Text Updated"  
    
    
    
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
        return "Image Saved"
    else:
        # Update data in database
        SavedImages.objects(image_id=data['image_id']).update(  
            title = title
            ,width = str(width)
            ,height = str(height)
            ,top = str(top)
            ,right = str(right)
        )                                             
        return "Image Updated" 



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
        
        chart_ids = []
        text_ids = []
        image_ids = []
        
        # Loop through and save our charts
        for chart in data["charts"]:
            # Save our chart if it is not already saved in the database
            result = save_chart(chart)
            # Add the chart's ID to our list
            chart_ids.append(SavedCharts.objects(chart_id=chart["data"]["chart_id"])[0])
            
        for text in data["texts"]:
            # Save our text if it is not already saved in the database
            result = save_text(text)
            # Add the text's ID to our list
            text_ids.append(SavedTexts.objects(text_id=text["text_id"])[0])
            
        for image in data["images"]:
            # Save our image if it is not already saved in the database
            result = save_image(image)
            # Add the image's ID to our list
            image_ids.append(SavedImages.objects(image_id=image["image_id"])[0])
            
        # Check if dashboard already exists
        # Save our dashboard
        if dashboard_id == "":
            SavedDashboards(
                dashboard_title = dashboard_title
                ,dashboard_height = dashboard_height
                ,dashboard_charts = chart_ids
                ,dashboard_texts = text_ids
                ,dashboard_images = image_ids
                ,dashboard_color = dashboard_color
            ).save()
            return "Dashboard Saved"
        if len(SavedDashboards.objects(id=dashboard_id)) == 0:
            SavedDashboards(
                dashboard_title = dashboard_title
                ,dashboard_height = dashboard_height
                ,dashboard_charts = chart_ids
                ,dashboard_texts = text_ids
                ,dashboard_images = image_ids
                ,dashboard_color = dashboard_color
            ).save()
            return "Dashboard Saved"
        else:
            # Othewise update our dashboard
            print("Updating Dashboard")
            SavedDashboards.objects(id=dashboard_id).update(
                dashboard_title = dashboard_title
                ,dashboard_height = dashboard_height
                ,dashboard_charts = chart_ids
                ,dashboard_texts = text_ids
                ,dashboard_images = image_ids
                ,dashboard_color = dashboard_color
            )
    
    return 'Success'



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
    charts = dashboard["dashboard_charts"]
    
    # Loop through charts, add data to return_charts
    for chart in charts:
        chart_data = loads(SavedCharts.objects(id=chart["$oid"]).to_json())[0]
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
    texts = dashboard["dashboard_texts"]
    
    # Loop through texts, add data to texts
    for text in texts:
        text_data = loads(SavedTexts.objects(id=text["$oid"]).to_json())[0]
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
    images = dashboard["dashboard_images"]
    
    # Loop through images, add data to images
    for image in images:
        image_data = loads(SavedImages.objects(id=image["$oid"]).to_json())[0]
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