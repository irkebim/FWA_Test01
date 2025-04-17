import bpy

class IRKEBIM_PT_import_image_panel(bpy.types.Panel):
    """Import Image 패널"""
    bl_label = "Image Import"
    bl_idname = "IRKEBIM_PT_import_image_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'IRKE BIM'

    def draw(self, context):
        layout = self.layout
        layout.operator("irkebim.import_image", text="Import Image")
