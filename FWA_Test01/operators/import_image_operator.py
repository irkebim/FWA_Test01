import bpy
import os

class IRKEBIM_OT_import_image(bpy.types.Operator):
    """이미지를 불러오고 평면을 생성하여 매핑합니다."""
    bl_idname = "irkebim.import_image"
    bl_label = "Import Image"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        scene = context.scene
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

        # 컬렉션 준비
        imported_col = bpy.data.collections.get('ImportedImages')
        if imported_col is None:
            imported_col = bpy.data.collections.new('ImportedImages')
            context.scene.collection.children.link(imported_col)

        centerline_col = bpy.data.collections.get('CenterLine')
        if centerline_col is None:
            centerline_col = bpy.data.collections.new('CenterLine')
            context.scene.collection.children.link(centerline_col)

        # Empty 생성 (이미지)
        empty = bpy.data.objects.new(name=image_name, object_data=None)
        empty.empty_display_type = 'IMAGE'
        empty.data = image
        imported_col.objects.link(empty)
        empty.location = (0, 0, 0.001)

        # ✨ Empty 크기 조정
        image_width = image.size[0]
        image_height = image.size[1]
        aspect_ratio = image_width / image_height if image_height != 0 else 1.0

        plane_width = scene.plane_settings.plane_width
        plane_opacity = scene.plane_settings.plane_opacity

        base_width = plane_width
        base_height = base_width / aspect_ratio

        empty.empty_display_size = base_width  # 여기 추가 ✅

        # Plane 생성
        bpy.ops.mesh.primitive_plane_add(size=1)
        plane = context.active_object
        plane.name = image_name + "_Plane"
        plane.scale.x = base_width
        plane.scale.y = base_height

        # 머티리얼 생성 및 적용
        mat = bpy.data.materials.new(name=image_name + "_Mat")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        tex_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
        tex_image.image = image

        mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])
        bsdf.inputs['Alpha'].default_value = plane_opacity
        mat.blend_method = 'BLEND'
        mat.shadow_method = 'NONE'

        plane.data.materials.append(mat)

        # 컬렉션 정리
        context.scene.collection.objects.unlink(plane)
        centerline_col.objects.link(plane)

        plane.location = (0, 0, 0)

        self.report({'INFO'}, f"이미지 및 평면 '{image_name}' 생성 완료")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
