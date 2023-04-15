from flask import render_template, Blueprint, send_from_directory, request
from flask_login import  current_user
from flask_security import login_required
from models import SavedDashboards

bp = Blueprint("dashboard", __name__)

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

@bp.route("/admin/save-chart", methods=['POST'])
@login_required
def save_chart():
    data = request.form.to_dict()
    
    # Check if this chart already exists
    # If it does, update otherwise save
    if len(SavedDashboards.objects(dashboard_id=data['dashboard_id'])) > 0:
        # Update dashboard
        SavedDashboards.objects(dashboard_id=data['dashboard_id']).update(   
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
        )
    else:
        # Store data in database
        SavedDashboards(  
            dashboard_id = data['dashboard_id']
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
        ).save()
    
    return 'Success'

@bp.route("/admin/charts", methods=["GET"])
@login_required
def get_charts():
    return SavedDashboards.objects.to_json()