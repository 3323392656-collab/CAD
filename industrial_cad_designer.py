"""
CAD-SKILL: Industrial Equipment 2D Engineering Drawings with ezdxf
ezdxf 工业设备2D工程图绘制技能

设备类型：
- 熔盐储罐 (Molten Salt Tank)
- 工业锅炉 (Industrial Boiler)  
- 管式换热器 (Tubular Heat Exchanger)

DXF格式优势：
✓ 原生AutoCAD格式，兼容性最好
✓ 可在任何CAD软件中打开编辑
✓ 轻量级，易于版本控制
✓ 支持精确标注和多图层管理
"""

import ezdxf
import math


class IndustrialCADDesigner:
    """工业设备2D工程图设计器"""
    
    # ========== 图层配置 ==========
    LAYER_CONFIG = {
        'OUTLINE': {'color': 1, 'linetype': 'Continuous', 'lineweight': 35},      # 黑色，粗线
        'DIMENSION': {'color': 2, 'linetype': 'Continuous', 'lineweight': 15},    # 红色
        'CENTER': {'color': 3, 'linetype': 'CENTER', 'lineweight': 13},           # 绿色，中心线
        'HIDDEN': {'color': 4, 'linetype': 'DASHED', 'lineweight': 13},           # 蓝色，隐线
        'TEXT': {'color': 7, 'linetype': 'Continuous', 'lineweight': 0},          # 白色
        'GRID': {'color': 8, 'linetype': 'Continuous', 'lineweight': 0},          # 灰色
    }
    
    @staticmethod
    def _create_base_doc(title="工程图"):
        """创建基础DXF文档并初始化图层"""
        doc = ezdxf.new('R2010')
        msp = doc.modelspace()
        
        # 初始化所有图层
        for layer_name, config in IndustrialCADDesigner.LAYER_CONFIG.items():
            if layer_name not in doc.layers:
                doc.layers.add(layer_name, **config)
        
        return doc, msp
    
    @staticmethod
    def draw_title_block(msp, x=0, y=0, title="工程图", width=1000, height=150):
        """绘制标题栏"""
        # 边框
        msp.add_lwpolyline([
            (x, y), (x + width, y), (x + width, y + height), (x, y + height)
        ], close=True, dxfattribs={'layer': 'OUTLINE'})
        
        # 标题
        msp.add_text(title, height=20, dxfattribs={'layer': 'TEXT'})\
            .set_pos((x + width/2 - 100, y + height/2 + 30))
        
        # 比例和日期
        msp.add_text('比例: 1:50', height=8, dxfattribs={'layer': 'TEXT'})\
            .set_pos((x + width - 150, y + 20))
    
    @staticmethod
    def create_salt_tank_drawing(
        diameter=1000,
        height=2000,
        wall_thickness=10,
        nozzle_count=3,
        scale=1/50
    ):
        """
        绘制熔盐储罐工程图（侧视图+俯视图+详图）
        
        参数：
            diameter: 外直径 (mm)
            height: 高度 (mm)
            wall_thickness: 壁厚 (mm)
            nozzle_count: 接管数量
            scale: 绘图比例
        
        返回：
            ezdxf Document对象
        """
        doc, msp = IndustrialCADDesigner._create_base_doc('熔盐储罐工程图')
        
        r = diameter / 2
        r_inner = r - wall_thickness
        
        # ========== 左侧视图（侧视图） ==========
        origin_x, origin_y = 100, 300
        
        # 1. 储罐主体（矩形代表圆柱）
        msp.add_line((origin_x, origin_y), (origin_x + diameter*scale, origin_y),
                     dxfattribs={'layer': 'OUTLINE', 'lineweight': 35})
        msp.add_line((origin_x, origin_y + height*scale),
                     (origin_x + diameter*scale, origin_y + height*scale),
                     dxfattribs={'layer': 'OUTLINE', 'lineweight': 35})
        msp.add_line((origin_x, origin_y), (origin_x, origin_y + height*scale),
                     dxfattribs={'layer': 'OUTLINE', 'lineweight': 35})
        msp.add_line((origin_x + diameter*scale, origin_y),
                     (origin_x + diameter*scale, origin_y + height*scale),
                     dxfattribs={'layer': 'OUTLINE', 'lineweight': 35})
        
        # 2. 顶部半球形封头
        arc_x = origin_x + r*scale
        arc_y = origin_y + height*scale
        msp.add_arc((arc_x, arc_y), radius=r*scale, start_angle=0, end_angle=180,
                    dxfattribs={'layer': 'OUTLINE', 'lineweight': 35})
        
        # 3. 内壁厚线
        msp.add_line((origin_x + wall_thickness*scale, origin_y + wall_thickness*scale),
                     (origin_x + wall_thickness*scale, origin_y + height*scale - 50*scale),
                     dxfattribs={'layer': 'HIDDEN'})
        msp.add_line((origin_x + diameter*scale - wall_thickness*scale, origin_y + wall_thickness*scale),
                     (origin_x + diameter*scale - wall_thickness*scale, origin_y + height*scale - 50*scale),
                     dxfattribs={'layer': 'HIDDEN'})
        
        # 4. 接管（3个，均匀分布）
        nozzle_diameter = 100
        nozzle_length = 150
        for i in range(nozzle_count):
            nozzle_y = origin_y + height*scale * (i+1) / (nozzle_count+1)
            
            # 接管体
            msp.add_line((origin_x + diameter*scale, nozzle_y),
                         (origin_x + diameter*scale + nozzle_length*scale, nozzle_y),
                         dxfattribs={'layer': 'OUTLINE'})
            
            # 法兰
            flange_w = 100*scale
            flange_h = 80*scale
            msp.add_lwpolyline([
                (origin_x + diameter*scale + nozzle_length*scale - flange_w/2, nozzle_y - flange_h/2),
                (origin_x + diameter*scale + nozzle_length*scale + flange_w/2, nozzle_y - flange_h/2),
                (origin_x + diameter*scale + nozzle_length*scale + flange_w/2, nozzle_y + flange_h/2),
                (origin_x + diameter*scale + nozzle_length*scale - flange_w/2, nozzle_y + flange_h/2),
            ], close=True, dxfattribs={'layer': 'OUTLINE'})
        
        # 5. 中心线
        msp.add_line((origin_x - 50*scale, origin_y + height*scale/2),
                     (origin_x + diameter*scale + 200*scale, origin_y + height*scale/2),
                     dxfattribs={'layer': 'CENTER'})
        
        # 6. 尺寸标注 - 高度
        msp.add_text('H', height=8, dxfattribs={'layer': 'DIMENSION'})\
            .set_pos((origin_x - 60*scale, origin_y + height*scale/2 - 10*scale))
        msp.add_text(f'{height}', height=10, dxfattribs={'layer': 'DIMENSION'})\
            .set_pos((origin_x - 100*scale, origin_y + height*scale/2 - 25*scale))
        
        # 7. 尺寸标注 - 直径
        msp.add_text('D', height=8, dxfattribs={'layer': 'DIMENSION'})\
            .set_pos((origin_x + diameter*scale/2 - 20*scale, origin_y - 40*scale))
        msp.add_text(f'{diameter}', height=10, dxfattribs={'layer': 'DIMENSION'})\
            .set_pos((origin_x + diameter*scale/2 - 40*scale, origin_y - 55*scale))
        
        # ========== 右侧视图（俯视图） ==========
        view_x, view_y = 600, 300
        
        # 1. 外圆
        msp.add_circle((view_x + r*scale, view_y + r*scale), r*scale,
                       dxfattribs={'layer': 'OUTLINE', 'lineweight': 35})
        
        # 2. 内圆（显示壁厚）
        msp.add_circle((view_x + r*scale, view_y + r*scale), r_inner*scale,
                       dxfattribs={'layer': 'HIDDEN'})
        
        # 3. 接管（俯视）
        for i in range(nozzle_count):
            angle = (i * 360 / nozzle_count) + 90  # 起始角度90度
            angle_rad = math.radians(angle)
            
            # 接管中心线
            x1 = view_x + r*scale + (r + 50)*scale * math.cos(angle_rad)
            y1 = view_y + r*scale + (r + 50)*scale * math.sin(angle_rad)
            
            x2 = view_x + r*scale + (r - 50)*scale * math.cos(angle_rad)
            y2 = view_y + r*scale + (r - 50)*scale * math.sin(angle_rad)
            
            msp.add_line((x1, y1), (x2, y2), dxfattribs={'layer': 'OUTLINE'})
            
            # 接管外圆
            msp.add_circle((x1, y1), 50*scale, dxfattribs={'layer': 'OUTLINE'})
            
            # 接管内圆
            msp.add_circle((x1, y1), 40*scale, dxfattribs={'layer': 'HIDDEN'})
        
        # 4. 中心十字
        msp.add_line((view_x + r*scale - 100*scale, view_y + r*scale),
                     (view_x + r*scale + 100*scale, view_y + r*scale),
                     dxfattribs={'layer': 'CENTER'})
        msp.add_line((view_x + r*scale, view_y + r*scale - 100*scale),
                     (view_x + r*scale, view_y + r*scale + 100*scale),
                     dxfattribs={'layer': 'CENTER'})
        
        # ========== 标题栏 ==========
        IndustrialCADDesigner.draw_title_block(
            msp, x=0, y=0,
            title='熔盐储罐工程图',
            width=1000, height=200
        )
        
        # 规格说明
        msp.add_text(f'规格: Φ{diameter}×{height} mm', height=9,
                     dxfattribs={'layer': 'TEXT'}).set_pos((100, 80))
        msp.add_text(f'壁厚: {wall_thickness} mm | 接管: {nozzle_count}个', height=9,
                     dxfattribs={'layer': 'TEXT'}).set_pos((100, 50))
        
        return doc
    
    @staticmethod
    def create_boiler_drawing(
        length=2000,
        diameter=1000,
        wall_thickness=12,
        scale=1/50
    ):
        """
        绘制工业锅炉工程图
        """
        doc, msp = IndustrialCADDesigner._create_base_doc('工业锅炉工程图')
        
        r = diameter / 2
        origin_x, origin_y = 100, 400
        
        # 1. 主圆柱体
        msp.add_line((origin_x, origin_y), (origin_x + length*scale, origin_y),
                     dxfattribs={'layer': 'OUTLINE', 'lineweight': 35})
        msp.add_line((origin_x, origin_y + diameter*scale),
                     (origin_x + length*scale, origin_y + diameter*scale),
                     dxfattribs={'layer': 'OUTLINE', 'lineweight': 35})
        
        # 2. 椭圆形封头（左）
        segments = 30
        for i in range(segments + 1):
            angle_deg = i * 180 / segments
            angle_rad = math.radians(angle_deg)
            x = origin_x - (r - 30)*scale * math.cos(angle_rad)
            y = origin_y + r*scale/2 + (r - 30)*scale * math.sin(angle_rad)
            
            if i == 0:
                x_prev, y_prev = x, y
            else:
                msp.add_line((x_prev, y_prev), (x, y),
                            dxfattribs={'layer': 'OUTLINE', 'lineweight': 35})
                x_prev, y_prev = x, y
        
        # 3. 椭圆形封头（右）
        for i in range(segments + 1):
            angle_deg = i * 180 / segments
            angle_rad = math.radians(angle_deg)
            x = origin_x + length*scale + (r - 30)*scale * math.cos(angle_rad)
            y = origin_y + r*scale/2 + (r - 30)*scale * math.sin(angle_rad)
            
            if i == 0:
                x_prev, y_prev = x, y
            else:
                msp.add_line((x_prev, y_prev), (x, y),
                            dxfattribs={'layer': 'OUTLINE', 'lineweight': 35})
                x_prev, y_prev = x, y
        
        # 4. 进出口集管（上下各2个）
        header_positions = [
            (origin_x + length*scale/4, 50, '进水'),
            (origin_x + 3*length*scale/4, 50, '进水'),
            (origin_x + length*scale/4, -50, '出水'),
            (origin_x + 3*length*scale/4, -50, '出水'),
        ]
        
        for x_pos, y_offset, label in header_positions:
            y_pos = origin_y + diameter*scale/2 + y_offset*scale
            
            # 管线
            msp.add_line((x_pos, y_pos), (x_pos, y_pos + 120*scale),
                        dxfattribs={'layer': 'OUTLINE'})
            
            # 法兰
            msp.add_circle((x_pos, y_pos + 120*scale), 30*scale,
                          dxfattribs={'layer': 'OUTLINE'})
            
            # 标注
            msp.add_text(label, height=7, dxfattribs={'layer': 'TEXT'})\
                .set_pos((x_pos - 15*scale, y_pos + 130*scale))
        
        # 5. 标注
        msp.add_text(f'长: {length}mm', height=10, dxfattribs={'layer': 'DIMENSION'})\
            .set_pos((origin_x + length*scale/2 - 100, origin_y - 80*scale))
        msp.add_text(f'径: {diameter}mm', height=10, dxfattribs={'layer': 'DIMENSION'})\
            .set_pos((origin_x - 120*scale, origin_y + diameter*scale/2))
        
        # 6. 标题栏
        IndustrialCADDesigner.draw_title_block(
            msp, x=0, y=0,
            title='工业锅炉工程图',
            width=1000, height=200
        )
        
        msp.add_text(f'规格: Φ{diameter}×{length} mm', height=9,
                     dxfattribs={'layer': 'TEXT'}).set_pos((100, 80))
        
        return doc
    
    @staticmethod
    def create_heat_exchanger_drawing(
        shell_diameter=500,
        shell_length=1500,
        tube_diameter=20,
        tube_count=36,
        scale=1/50
    ):
        """
        绘制管式换热器工程图
        """
        doc, msp = IndustrialCADDesigner._create_base_doc('管式换热器工程图')
        
        r = shell_diameter / 2
        origin_x, origin_y = 150, 400
        
        # 1. 壳体
        msp.add_line((origin_x, origin_y), (origin_x + shell_length*scale, origin_y),
                     dxfattribs={'layer': 'OUTLINE', 'lineweight': 35})
        msp.add_line((origin_x, origin_y + shell_diameter*scale),
                     (origin_x + shell_length*scale, origin_y + shell_diameter*scale),
                     dxfattribs={'layer': 'OUTLINE', 'lineweight': 35})
        
        # 2. 换热管（阵列小圆）
        tube_rows = 6
        tube_cols = int(tube_count / 6)
        
        for i in range(tube_rows):
            y = origin_y + (i+1)*shell_diameter*scale/(tube_rows+1)
            for j in range(tube_cols):
                x = origin_x + (j+1)*shell_length*scale/(tube_cols+1)
                msp.add_circle((x, y), tube_diameter*scale/2,
                              dxfattribs={'layer': 'TEXT'})
        
        # 3. 端板
        msp.add_lwpolyline([
            (origin_x - 20*scale, origin_y - 10*scale),
            (origin_x - 20*scale, origin_y + shell_diameter*scale + 10*scale),
            (origin_x - 15*scale, origin_y + shell_diameter*scale + 10*scale),
            (origin_x - 15*scale, origin_y - 10*scale),
        ], close=True, dxfattribs={'layer': 'OUTLINE'})
        
        msp.add_lwpolyline([
            (origin_x + shell_length*scale + 20*scale, origin_y - 10*scale),
            (origin_x + shell_length*scale + 20*scale, origin_y + shell_diameter*scale + 10*scale),
            (origin_x + shell_length*scale + 15*scale, origin_y + shell_diameter*scale + 10*scale),
            (origin_x + shell_length*scale + 15*scale, origin_y - 10*scale),
        ], close=True, dxfattribs={'layer': 'OUTLINE'})
        
        # 4. 进出口
        inlet_y = origin_y + shell_diameter*scale/2 + 80*scale
        outlet_y = origin_y + shell_diameter*scale/2 - 80*scale
        
        # 进水
        msp.add_line((origin_x - 80*scale, inlet_y), (origin_x - 80*scale, inlet_y + 80*scale),
                     dxfattribs={'layer': 'OUTLINE'})
        msp.add_circle((origin_x - 80*scale, inlet_y + 80*scale), 30*scale,
                      dxfattribs={'layer': 'OUTLINE'})
        msp.add_text('进', height=8, dxfattribs={'layer': 'TEXT'})\
            .set_pos((origin_x - 95*scale, inlet_y + 85*scale))
        
        # 出水
        msp.add_line((origin_x + shell_length*scale + 80*scale, outlet_y),
                     (origin_x + shell_length*scale + 80*scale, outlet_y - 80*scale),
                     dxfattribs={'layer': 'OUTLINE'})
        msp.add_circle((origin_x + shell_length*scale + 80*scale, outlet_y - 80*scale), 30*scale,
                      dxfattribs={'layer': 'OUTLINE'})
        msp.add_text('出', height=8, dxfattribs={'layer': 'TEXT'})\
            .set_pos((origin_x + shell_length*scale + 65*scale, outlet_y - 85*scale))
        
        # 5. 标题栏
        IndustrialCADDesigner.draw_title_block(
            msp, x=0, y=0,
            title='管式换热器工程图',
            width=1000, height=200
        )
        
        msp.add_text(f'规格: Φ{shell_diameter}×{shell_length} mm | 管数: {tube_count}',
                     height=9, dxfattribs={'layer': 'TEXT'}).set_pos((100, 80))
        
        return doc


# ============ 便捷函数 ============

def draw_salt_tank(**kwargs):
    """绘制熔盐储罐工程图"""
    return IndustrialCADDesigner.create_salt_tank_drawing(**kwargs)


def draw_boiler(**kwargs):
    """绘制工业锅炉工程图"""
    return IndustrialCADDesigner.create_boiler_drawing(**kwargs)


def draw_heat_exchanger(**kwargs):
    """绘制管式换热器工程图"""
    return IndustrialCADDesigner.create_heat_exchanger_drawing(**kwargs)


# ============ 使用示例 ============

if __name__ == '__main__':
    print("=" * 70)
    print("ezdxf 工业设备工程图生成 - SKILL 演示")
    print("=" * 70)
    
    # 示例1：熔盐储罐
    print("\n[1/3] 生成熔盐储罐工程图...")
    doc1 = draw_salt_tank(diameter=1000, height=2000, nozzle_count=3)
    doc1.saveas('salt_tank_drawing.dxf')
    print("✓ salt_tank_drawing.dxf 已生成")
    
    # 示例2：工业锅炉
    print("\n[2/3] 生成工业锅炉工程图...")
    doc2 = draw_boiler(length=2000, diameter=1000)
    doc2.saveas('boiler_drawing.dxf')
    print("✓ boiler_drawing.dxf 已生成")
    
    # 示例3：管式换热器
    print("\n[3/3] 生成管式换热器工程图...")
    doc3 = draw_heat_exchanger(shell_diameter=500, shell_length=1500, tube_count=36)
    doc3.saveas('heat_exchanger_drawing.dxf')
    print("✓ heat_exchanger_drawing.dxf 已生成")
    
    print("\n" + "=" * 70)
    print("✓ 所有工程图已成功生成！")
    print("  可在 AutoCAD、LibreCAD 或其他CAD软件中打开 .dxf 文件")
    print("=" * 70)
