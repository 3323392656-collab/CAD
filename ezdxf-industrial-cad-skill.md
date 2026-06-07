# CAD-SKILL: ezdxf 工业设备2D工程图绘制

## 概述
这个SKILL用于快速生成工业热学系统中常见设备的**2D工程图纸**（AutoCAD DXF格式），包括：
- 熔盐储罐俯视图/侧视图
- 工业锅炉工程图
- 换热器结构图
- 管道布置图

## 快速开始

### 安装依赖
```bash
pip install ezdxf
```

### 基础用法
```python
import ezdxf
from industrial_cad_designer import (
    draw_salt_tank,
    draw_boiler,
    draw_heat_exchanger
)

# 生成熔盐储罐工程图
doc = draw_salt_tank(
    diameter=1000,      # 直径 mm
    height=2000,        # 高度 mm
    scale=1/50          # 图纸比例
)

# 保存为DXF（可在AutoCAD中打开）
doc.saveas('salt_tank_drawing.dxf')
```

---

## 核心API参考

### ezdxf 基础操作

| 操作 | 代码 | 说明 |
|------|------|------|
| 新建文档 | `ezdxf.new('R2010')` | 创建R2010标准DXF |
| 获取画布 | `doc.modelspace()` | 获取模型空间 |
| 添加直线 | `.add_line((x1,y1), (x2,y2))` | 画直线 |
| 添加圆 | `.add_circle((x,y), r)` | 画圆 |
| 添加圆弧 | `.add_arc((x,y), r, start, end)` | 画圆弧 |
| 添加文字 | `.add_text('text', height=10)` | 添加标注文字 |
| 添加多边形 | `.add_lwpolyline(points, close=True)` | 画多边形 |
| 新建图层 | `doc.layers.add('Layer1', color=1)` | 创建新图层 |
| 保存文件 | `doc.saveas('output.dxf')` | 导出DXF文件 |

---

## 完整示例代码

详见 `industrial_cad_designer.py` 文件

---

## 图层约定

| 图层名称 | 颜色 | 用途 | 线宽 |
|---------|------|------|------|
| OUTLINE | 1(黑) | 主轮廓线 | 粗(35) |
| DIMENSION | 2(红) | 尺寸标注 | 中(15) |
| CENTER | 3(绿) | 中心线 | 细(13) |
| HIDDEN | 4(蓝) | 隐线 | 细(13) |
| TEXT | 7(白) | 文字说明 | 无 |
| GRID | 8(灰) | 辅助网格 | 无 |

---

## 应用示例

### 示例1：生成标准工程图集
```python
# 生成所有工程图
doc1 = draw_salt_tank(diameter=1000, height=2000)
doc1.saveas('tank_drawing.dxf')

doc2 = draw_boiler(length=2000, diameter=1000)
doc2.saveas('boiler_drawing.dxf')

doc3 = draw_heat_exchanger(shell_diameter=500, shell_length=1500)
doc3.saveas('he_drawing.dxf')

print("✓ 所有工程图已生成！")
```

### 示例2：批量参数化绘图
```python
sizes = [
    {'diameter': 800, 'height': 1500, 'name': 'small'},
    {'diameter': 1000, 'height': 2000, 'name': 'medium'},
    {'diameter': 1200, 'height': 2500, 'name': 'large'}
]

for size in sizes:
    doc = draw_salt_tank(diameter=size['diameter'], height=size['height'])
    doc.saveas(f"tank_{size['name']}.dxf")
```

### 示例3：自定义工程图
```python
import ezdxf

# 创建自己的DXF
doc = ezdxf.new('R2010')
msp = doc.modelspace()

# 添加图层
doc.layers.add('CUSTOM', color=5)

# 绘制内容
msp.add_line((0, 0), (100, 100), dxfattribs={'layer': 'CUSTOM'})
msp.add_circle((50, 50), 30, dxfattribs={'layer': 'CUSTOM'})
msp.add_text('Custom Drawing', height=20, dxfattribs={'layer': 'CUSTOM'})

# 保存
doc.saveas('custom_drawing.dxf')
```

---

## 工程图纸标准

### 视图组织
- **侧视图**（左）：展示设备高度、直径、接管位置
- **俯视图**（右）：展示接管分布、管道布置
- **详图**：特殊部位的放大图

### 标注规范
- 所有尺寸使用 mm 为单位
- 重要尺寸用红色标注
- 公差和注记用TEXT图层

### 线型约定
- **实线**：可见轮廓
- **虚线**：隐线（内部结构）
- **中心线**：对称中心、旋转轴
- **细线**：辅助线、尺寸线

---

## 参考资源

- 📖 [ezdxf 官方文档](https://ezdxf.mozman.at/)
- 📘 [ezdxf API参考](https://ezdxf.mozman.at/docs/api/index.html)
- 🔗 [AutoCAD DXF格式规范](https://www.autodesk.com/techpubs/autocad/acad2023/dxf/)

---

## 快速启动

```bash
# 1. 安装
pip install ezdxf

# 2. 复制 industrial_cad_designer.py

# 3. 运行示例
python industrial_cad_designer.py

# 4. 在AutoCAD或CAD看图软件中打开生成的.dxf文件
```
