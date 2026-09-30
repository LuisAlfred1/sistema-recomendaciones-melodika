from flask import Blueprint, render_template

admin_views_bp = Blueprint("admin_views", __name__, url_prefix="/admin")


@admin_views_bp.get("/")
def dashboard():
    return render_template("admin/dashboard.html")


@admin_views_bp.get("/productos")
def productos():
    return render_template("admin/productos.html")