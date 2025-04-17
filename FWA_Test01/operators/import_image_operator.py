import bpy
import os

class IRKEBIM_OT_import_image(bpy.types.Operator):
    """이미지를 불러오고 'ImportedImages' 컬렉션에 등록합니다."""
    bl_idname = "irkebim.import_image"
    bl_label = "Import Image"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        filepath = self.filepath
        if not filepath:
            self.report({'ERROR'}, "파일 경로가 유효하지 않습니다.")
            return {'CANCELLED'}

        filename = os.path.basename(filepath)
        image_name = os.path.splitext(filename)[0]

        try:
            image = bpy.data.images.load(filepath, check_existing=True)
        except Exception as e:
            self.report({'ERROR'}, f"이미지 로드 실패: {e}")
            return {'CANCELLED'}

        imported_col = bpy.data.collections.get('ImportedImages')
        if imported_col is None:
            imported_col = bpy.data.collections.new('ImportedImages')
            context.scene.collection.children.link(imported_col)

        empty = bpy.data.objects.new(name=image_name, object_data=None)
        empty.empty_display_type = 'IMAGE'
        empty.data = image
        imported_col.objects.link(empty)
        empty.location = (0, 0, 0)

        self.report({'INFO'}, f"이미지 '{image_name}' 임포트 완료")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
