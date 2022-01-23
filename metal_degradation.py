bl_info = {
    "name": "Metal Degradation",
    "author": "Adam Polivka",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Shader Editor > Sidebar > Metal Degradation",
    "description": "Adds metal degradation group to active material",
    "warning": "",
    "doc_url": "",
    "category": "Add Node Group",
}

import bpy
        
class metalDegradationNodePanel(bpy.types.Panel):
    bl_label = "Metal degradation"
    bl_idname = "NODE_PT_SE_polivad1"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Metal Degradation'
    
    def draw(self, context):
        layout = self.layout
        
        mat = bpy.context.active_object.active_material

        row = layout.row()
        row.label(text = "Adds metal degradation network to current material.", icon = 'KEYTYPE_EXTREME_VEC')
        row = layout.row()
        row.operator('node.metal_degradation_network')
        
def createCorrosionShaderGroup(context):
    
    mat = bpy.context.active_object.active_material
        
    mat.use_nodes = True
        
    # Create corrosion group
    corrosion = bpy.data.node_groups.new('Corrosion', 'ShaderNodeTree')

    # Corrosion input
    corrosion_inputs_node = corrosion.nodes.new('NodeGroupInput')
    corrosion.inputs.new('NodeSocketFloat', 'Crack height')
    corrosion.inputs.new('NodeSocketFloat', 'Crack size')
    corrosion.inputs.new('NodeSocketFloat', 'Bumpiness')
    corrosion_inputs_node.location = (-1500, -400)
    corrosion_inputs_node.select = False
        
    # Corrosion ouput
    corrosion_outputs_node = corrosion.nodes.new('NodeGroupOutput')
    corrosion.outputs.new('NodeSocketShader', 'CorrosionShader')
    corrosion.outputs.new('NodeSocketColor', 'Color')
    corrosion_outputs_node.location = (650, 100)
    corrosion_outputs_node.select = False
    
    # Corrosion input adjuster bump1
    multiply1 = corrosion.nodes.new('ShaderNodeMath')
    multiply1.operation = 'MULTIPLY'
    multiply1.inputs[1].default_value = 0.1
    multiply1.location = (-1050, -350)
    multiply1.select = False
    
    # Corrosion input adjuster bump2
    multiply2 = corrosion.nodes.new('ShaderNodeMath')
    multiply2.operation = 'MULTIPLY'
    multiply2.inputs[1].default_value = 0.01
    multiply2.location = (-1250, -500)
    multiply2.select = False
        
    # Texture Coordinate
    tex_coord = corrosion.nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1100, 0)
    tex_coord.select = False
        
    # Mapping
    mapping = corrosion.nodes.new('ShaderNodeMapping')
    mapping.location = (-850, 0)
    mapping.select = False
        
    # Noise Texture 1
    tex_noise1 = corrosion.nodes.new('ShaderNodeTexNoise')
    tex_noise1.inputs[2].default_value = 5
    tex_noise1.inputs[3].default_value = 16
    tex_noise1.inputs[5].default_value = 0.2
    tex_noise1.location = (-650, -100)
    tex_noise1.select = False
        
    # Color ramp 1
    # Creates "rusty" color on the object
    val_to_rgb1 = corrosion.nodes.new('ShaderNodeValToRGB')
    val_to_rgb1.location = (-450, 100)
        
    val_to_rgb1_elements = val_to_rgb1.color_ramp.elements
    val_to_rgb1_elements[0].color = (0, 0, 0, 1)
    val_to_rgb1_elements[0].position = 0
    val_to_rgb1_elements[1].color = (1, 0.321, 0.163, 1)
    val_to_rgb1_elements[1].position = 0.427
    val_to_rgb1_elements.new(2)
    val_to_rgb1_elements[2].color = (0.5, 0.024, 0, 1)
    val_to_rgb1_elements[2].position = 0.45
    val_to_rgb1_elements.new(3)
    val_to_rgb1_elements[3].color = (1, 1, 1, 1)
    val_to_rgb1_elements[3].position = 0.673
    val_to_rgb1.select = False
        
    # Color ramp 2
    # Used as bump map height adjuster
    val_to_rgb2 = corrosion.nodes.new('ShaderNodeValToRGB')
    val_to_rgb2_elements = val_to_rgb2.color_ramp.elements
    val_to_rgb2_elements[0].color = (0, 0, 0, 1)
    val_to_rgb2_elements[0].position = 0
    val_to_rgb2_elements[1].color = (1, 1, 1, 1)
    val_to_rgb2_elements[1].position = 0.5
    val_to_rgb2.location = (-450, -150)        
    val_to_rgb2.select = False
                       
    # Noise Texture 2
    tex_noise2 = corrosion.nodes.new('ShaderNodeTexNoise')
    tex_noise2.inputs[2].default_value = 20
    tex_noise2.inputs[3].default_value = 16
    tex_noise2.location = (-900, -550)
    tex_noise2.select = False
        
    # Noise Texture 3
    tex_noise3 = corrosion.nodes.new('ShaderNodeTexNoise')
    tex_noise3.inputs[2].default_value = 50
    tex_noise3.inputs[3].default_value = 16
    tex_noise3.location = (-650, -500)
    tex_noise3.select = False
        
    # Bump map1
    bump1 = corrosion.nodes.new('ShaderNodeBump')
    bump1.location = (-400, -450)
    bump1.inputs[0].default_value = 0.085
    bump1.select = False
        
    # Bump map2
    bump2 = corrosion.nodes.new('ShaderNodeBump')
    bump2.inputs[0].default_value = 0.35
    bump2.location = (-100, -275)
    bump2.select = False
        
    # Principled BSDF
    principled = corrosion.nodes.new('ShaderNodeBsdfPrincipled')
    principled.inputs[4].default_value = 1
    principled.location = (125, 0)
    principled.select = False
        
    # Create Links
    corrosion.links.new(tex_coord.outputs[3], mapping.inputs[0])
    corrosion.links.new(mapping.outputs[0], tex_noise1.inputs[0])
    corrosion.links.new(tex_noise1.outputs[1], val_to_rgb1.inputs[0])
    corrosion.links.new(tex_noise1.outputs[1], val_to_rgb2.inputs[0])
        
    corrosion.links.new(tex_noise2.outputs[1], tex_noise3.inputs[0])
    corrosion.links.new(tex_noise3.outputs[1], bump1.inputs[2])
    corrosion.links.new(val_to_rgb1.outputs[0], principled.inputs[0])
    corrosion.links.new(val_to_rgb2.outputs[0], bump2.inputs[2])
    corrosion.links.new(bump1.outputs[0], bump2.inputs[5])
    corrosion.links.new(bump2.outputs[0], principled.inputs[19])
    
    corrosion.links.new(corrosion_inputs_node.outputs[0], multiply1.inputs[0])
    corrosion.links.new(corrosion_inputs_node.outputs[1], tex_noise1.inputs[2])
    corrosion.links.new(corrosion_inputs_node.outputs[2], multiply2.inputs[0])
    corrosion.links.new(multiply1.outputs[0], bump2.inputs[0])
    corrosion.links.new(multiply2.outputs[0], bump1.inputs[0])
        
    corrosion.links.new(principled.outputs[0], corrosion_outputs_node.inputs[0])
    corrosion.links.new(tex_noise1.outputs[1], corrosion_outputs_node.inputs[1])
    
    return corrosion
        
        
def createMetalWearMaskMixer(context):
    
    mat = bpy.context.active_object.active_material
    
    metal_wear_mask_group = bpy.data.node_groups.new('MetalWearmixer', 'ShaderNodeTree')
    
    
    metal_wear_mask_group_inputs = metal_wear_mask_group.nodes.new('NodeGroupInput')
    metal_wear_mask_group.inputs.new("NodeSocketFloat", "MaskValue")
    metal_wear_mask_group.inputs.new("NodeSocketFloat", "Degradation index")
    metal_wear_mask_group_inputs.location = (-300, -250)
    
    substract = metal_wear_mask_group.nodes.new('ShaderNodeMath')
    substract.operation = 'SUBTRACT'
    substract.inputs[1].default_value = 0.28
    substract.location = (-100, 0)
    substract.select = False
    
    maximum = metal_wear_mask_group.nodes.new('ShaderNodeMath')
    maximum.operation = 'MAXIMUM'
    maximum.inputs[1].default_value = -1.81
    maximum.location = (100, 50)
    maximum.select = False
    
    multiply = metal_wear_mask_group.nodes.new('ShaderNodeMath')
    multiply.operation = 'MULTIPLY'
    multiply.inputs[1].default_value = 0.01
    multiply.location = (300, 0)
    multiply.select = False
    
    less_than = metal_wear_mask_group.nodes.new('ShaderNodeMath')
    less_than.operation = 'LESS_THAN'
    less_than.location = (550, 150)
    less_than.select = False
    
    val_to_rgb = metal_wear_mask_group.nodes.new('ShaderNodeValToRGB')
    val_to_rgb_elements = val_to_rgb.color_ramp.elements
    val_to_rgb_elements[0].color = (1, 1, 1, 1)
    val_to_rgb_elements[0].position = 0.065
    val_to_rgb_elements[1].color = (0.673, 0.673, 0.673, 1)
    val_to_rgb_elements[1].position = 1
    val_to_rgb.location = (500, 400)
    val_to_rgb.select = False
    
    metal_wear_mask_group_outputs = metal_wear_mask_group.nodes.new('NodeGroupOutput')
    metal_wear_mask_group.outputs.new('NodeSocketFloat', 'Scratch')
    metal_wear_mask_group.outputs.new('NodeSocketFloat', 'Rust')
    metal_wear_mask_group_outputs.location = (800, 250)
    metal_wear_mask_group_outputs.select = False
           
    # Links
    metal_wear_mask_group.links.new(metal_wear_mask_group_inputs.outputs[0], substract.inputs[0])
    metal_wear_mask_group.links.new(metal_wear_mask_group_inputs.outputs[1], multiply.inputs[0])
    metal_wear_mask_group.links.new(substract.outputs[0], maximum.inputs[0])
    metal_wear_mask_group.links.new(maximum.outputs[0], less_than.inputs[0])
    metal_wear_mask_group.links.new(multiply.outputs[0], less_than.inputs[1])    
    metal_wear_mask_group.links.new(multiply.outputs[0], val_to_rgb.inputs[0])
    metal_wear_mask_group.links.new(val_to_rgb.outputs[0], metal_wear_mask_group_outputs.inputs[0])
    metal_wear_mask_group.links.new(less_than.outputs[0], metal_wear_mask_group_outputs.inputs[1])

    return metal_wear_mask_group

def createMetalWearShaderGroup(context):
        
    mat = bpy.context.active_object.active_material
        
    mat.use_nodes = True
    
    # Create metallic wear group
    metal_wear = bpy.data.node_groups.new('Mettalic wear', 'ShaderNodeTree')
        
    # Group output
    metal_wear_outputs_node = metal_wear.nodes.new('NodeGroupOutput')
    metal_wear.outputs.new('NodeSocketShader', 'Shader')
    metal_wear_outputs_node.location = (1500, 150)
    metal_wear_outputs_node.select = False
        
    # Tex Coordiante
    tex_coord = metal_wear.nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-850, -500)
    tex_coord.select = False
        
    # Mapping
    mapping = metal_wear.nodes.new('ShaderNodeMapping')
    mapping.location = (-600, -500)
    mapping.select = False
        
    # Wave Texture 
    tex_wave = metal_wear.nodes.new('ShaderNodeTexWave')
    tex_wave.inputs[1].default_value = 1.4
    tex_wave.inputs[2].default_value = 0.6
    tex_wave.inputs[3].default_value = 0
    tex_wave.location = (-375, -500)
    tex_wave.select = False
        
    # Musgrave Texture 1
    tex_musgrave1 = metal_wear.nodes.new('ShaderNodeTexMusgrave')
    tex_musgrave1.inputs[2].default_value = 5.7
    tex_musgrave1.inputs[3].default_value = 16
    tex_musgrave1.inputs[4].default_value = 0.3
    tex_musgrave1.inputs[5].default_value = 0.5
    tex_musgrave1.location = (-150, 150)
    tex_musgrave1.select = False
        
    # Musgrave Texture 2
    tex_musgrave2 = metal_wear.nodes.new('ShaderNodeTexMusgrave')
    tex_musgrave2.inputs[2].default_value = 8.8
    tex_musgrave2.inputs[3].default_value = 16
    tex_musgrave2.inputs[4].default_value = 0
    tex_musgrave2.inputs[5].default_value = 1.5
    tex_musgrave2.location = (-150, -100)
    tex_musgrave2.select = False
        
    # Musgrave Texture 3
    tex_musgrave3 = metal_wear.nodes.new('ShaderNodeTexMusgrave')
    tex_musgrave3.musgrave_dimensions = '4D'
    tex_musgrave3.inputs[1].default_value = 10.1
    tex_musgrave3.inputs[2].default_value = 3.5
    tex_musgrave3.inputs[3].default_value = 16
    tex_musgrave3.location = (-150, -350)
    tex_musgrave3.select = False
        
    # Noise Texture 1
    tex_noise1 = metal_wear.nodes.new('ShaderNodeTexNoise')
    tex_noise1.inputs[2].default_value = 2.1
    tex_noise1.inputs[3].default_value = 2
    tex_noise1.location = (150, 150)
    tex_noise1.select = False
        
    # Noise Texture 2
    tex_noise2 = metal_wear.nodes.new('ShaderNodeTexNoise')
    tex_noise2.inputs[2].default_value = 2.9
    tex_noise2.location = (150, -150)
    tex_noise2.select = False
        
    # Color ramp 1
    val_to_rgb1 = metal_wear.nodes.new('ShaderNodeValToRGB')
    val_to_rgb1_elements = val_to_rgb1.color_ramp.elements
    val_to_rgb1_elements[0].color = (0, 0, 0, 1)
    val_to_rgb1_elements[0].position = 0
    val_to_rgb1_elements[1].color = (1, 1, 1, 1)
    val_to_rgb1_elements[1].position = 0.455
    val_to_rgb1_elements.new(2)
    val_to_rgb1_elements[2].color = (0, 0, 0, 1)
    val_to_rgb1_elements[2].position = 0.568 
    val_to_rgb1.location = (400, 150)
    val_to_rgb1.select = False
            
    # Color ramp 2
    val_to_rgb2 = metal_wear.nodes.new('ShaderNodeValToRGB')
    val_to_rgb2_elements = val_to_rgb2.color_ramp.elements
    val_to_rgb2_elements[0].color = (1, 1, 1, 1)
    val_to_rgb2_elements[0].position = 0.514
    val_to_rgb2_elements[1].color = (0, 0, 0, 1)
    val_to_rgb2_elements[1].position = 0.714
    val_to_rgb2_elements.new(2)
    val_to_rgb2_elements[2].color = (0.091, 0.091, 0.091, 1)
    val_to_rgb2_elements[2].position = 0.847 
    val_to_rgb2.location = (400, -100)
    val_to_rgb2.select = False
        
    # Mix rgg multiply
    mix_RGB = metal_wear.nodes.new('ShaderNodeMixRGB')
    mix_RGB.blend_type = 'MULTIPLY'
    mix_RGB.inputs[0].default_value = 1
    mix_RGB.location = (800, 100)
    mix_RGB.select = False
        
    # Bump
    bump = metal_wear.nodes.new('ShaderNodeBump')
    bump.inputs[0].default_value = 0.058
    bump.location = (800, -150)
    bump.select = False
        
    # Principled BSFD
    principled = metal_wear.nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (1100, 150)
    principled.select = False
        
        
    # Links
    metal_wear.links.new(tex_coord.outputs[0], mapping.inputs[0])
    metal_wear.links.new(mapping.outputs[0], tex_wave.inputs[0])
    metal_wear.links.new(tex_wave.outputs[1], tex_musgrave3.inputs[5])
    metal_wear.links.new(tex_musgrave1.outputs[0], tex_noise1.inputs[5])
    metal_wear.links.new(tex_musgrave2.outputs[0], tex_noise2.inputs[3])
    metal_wear.links.new(tex_musgrave3.outputs[0], tex_noise2.inputs[5])
    metal_wear.links.new(tex_noise1.outputs[0], val_to_rgb1.inputs[0])
    metal_wear.links.new(tex_noise2.outputs[0], val_to_rgb2.inputs[0])
    metal_wear.links.new(val_to_rgb1.outputs[0], mix_RGB.inputs[1])
    metal_wear.links.new(val_to_rgb2.outputs[0], mix_RGB.inputs[2])
    metal_wear.links.new(val_to_rgb2.outputs[0], bump.inputs[2])
    metal_wear.links.new(mix_RGB.outputs[0], principled.inputs[4])
    metal_wear.links.new(bump.outputs[0], principled.inputs[19])
    metal_wear.links.new(principled.outputs[0], metal_wear_outputs_node.inputs[0])
    
    return metal_wear
        

def addDegradationShaderNetwork(context):
    
    # Get acite otput material to be modified
    node_tree = bpy.context.active_object.active_material.node_tree
      
      
    mat_output = node_tree.nodes.get('Material Output')

    if not mat_output:
        mat_output = node_tree.nodes.new('ShaderNodeOutputMaterial')
        
    # Get shader connected to the material output before adding metal degradation groups
    try:
        last_shader = mat_output.inputs[0].links[0].from_node
    except:
        last_shader = False
        
    # Mix Shader
    # Used to mix previous shader with metal wear shader group
    mix_shader1 = node_tree.nodes.new('ShaderNodeMixShader')
        
    # Mix Shader
    # Used to mix rust with adjusted base metal material
    mix_shader2 = node_tree.nodes.new('ShaderNodeMixShader')

    if last_shader == False:
        glossy = node_tree.nodes.new('ShaderNodeBsdfGlossy')
        glossy.inputs[0].default_value = (0, 0, 1, 1)
            
    # Corrosion
    corrosion_group = createCorrosionShaderGroup(context)
    corrosion_group_node = node_tree.nodes.new('ShaderNodeGroup')
    corrosion_group_node.node_tree = corrosion_group
    corrosion_group_node.inputs[0].default_value = 3.5
    corrosion_group_node.inputs[1].default_value = 5
    corrosion_group_node.inputs[2].default_value = 8.5
    
    # Metal wear
    metal_wear_group = createMetalWearShaderGroup(context)
    metal_wear_group_node = node_tree.nodes.new('ShaderNodeGroup')
    metal_wear_group_node.node_tree = metal_wear_group
    
    # Metal degradation mask mixer
    metal_wear_mask_group = createMetalWearMaskMixer(context)
    metal_wear_mask_group_node = node_tree.nodes.new('ShaderNodeGroup')
    metal_wear_mask_group_node.node_tree = metal_wear_mask_group
    metal_wear_mask_group_node.inputs[1].default_value = 27
    
    # Links
    node_tree.links.new(corrosion_group_node.outputs[0], mix_shader2.inputs[2])
    node_tree.links.new(corrosion_group_node.outputs[1], metal_wear_mask_group_node.inputs[0])
    node_tree.links.new(metal_wear_group_node.outputs[0], mix_shader1.inputs[1])
    node_tree.links.new(metal_wear_mask_group_node.outputs[0], mix_shader1.inputs[0])
    node_tree.links.new(metal_wear_mask_group_node.outputs[1], mix_shader2.inputs[0])
        
    node_tree.links.new(mix_shader1.outputs[0], mix_shader2.inputs[1])
    node_tree.links.new(corrosion_group_node.outputs[0], mix_shader2.inputs[2])
         
    if last_shader != False:
        node_tree.links.new(last_shader.outputs[0], mix_shader1.inputs[2])
    else:
        node_tree.links.new(glossy.outputs[0], mix_shader1.inputs[2])
    
    # Created material to the reset output
    node_tree.links.new(mix_shader2.outputs[0], mat_output.inputs[0])
    
    # Position of the nodes
    mix_shader2.location = (mat_output.location.x - 250, mat_output.location.y)
    mix_shader1.location = (mat_output.location.x - 450, mat_output.location.y + 100)
    metal_wear_group_node.location = (mat_output.location.x - 750, mat_output.location.y + 100)
    corrosion_group_node.location = (mat_output.location.x - 950, mat_output.location.y - 50)
    metal_wear_mask_group_node.location = (mat_output.location.x - 650, mat_output.location.y - 100)
    
    if last_shader == False:
        glossy.location = (mat_output.location.x - 1200, mat_output.location.y + 50)
        

class NODE_OT_METAL_DEGRADATION_SHADER_NETWORK(bpy.types.Operator):
    bl_label = 'Add metal degradation group'
    bl_idname = 'node.metal_degradation_network'
    
    def execute(self, context):
        # Adds metal degradation shader network to current active material
        addDegradationShaderNetwork(context)
        
        return {'FINISHED'}
        
# register         
def register():
    bpy.utils.register_class(metalDegradationNodePanel)
    bpy.utils.register_class(NODE_OT_METAL_DEGRADATION_SHADER_NETWORK)

# unregister
def unregister():
    bpy.utils.unregister_class(metalDegradationNodePanel)
    bpy.utils.unregister_class(NODE_OT_METAL_DEGRADATION_SHADER_NETWORK)
    
if __name__ == "__main__":
    register()