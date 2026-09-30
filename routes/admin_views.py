from flask import Blueprint, redirect, render_template, url_for

admin_views_bp = Blueprint("admin_views", __name__, url_prefix="/admin")


@admin_views_bp.get("/")
def dashboard():
    return redirect(url_for("admin_views.inventario"))


@admin_views_bp.get("/inventario")
def inventario():
    return render_template("admin/dashboard.html")


@admin_views_bp.get("/productos")
def productos():
    return render_template("admin/productos.html")
