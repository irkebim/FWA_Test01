import bpy

class PlaneSettingsProperty(bpy.types.PropertyGroup):
    plane_width: bpy.props.FloatProperty(
        name="Plane Width (m)",
        default=2.0,
        min=0.01,
    )
    plane_opacity: bpy.props.FloatProperty(
        name="Opacity",
        default=0.5,
        min=0.0,
        max=1.0,
    )

def register():
    # bpy.utils.register_class(PlaneSettingsProperty)  ❌ (주석처리 or 삭제)
    bpy.types.Scene.plane_settings = bpy.props.PointerProperty(type=PlaneSettingsProperty)

def unregister():
    # bpy.utils.unregister_class(PlaneSettingsProperty)  ❌ (주석처리 or 삭제)
    del bpy.types.Scene.plane_settings