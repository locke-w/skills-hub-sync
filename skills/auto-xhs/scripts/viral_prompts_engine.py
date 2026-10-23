#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3D 全彩手办爆款生图提示词工程引擎 (Viral Prompts Engine) v5.1

遵循阿里巴巴工程规约：
1. 单一职责原则：负责对标博主风格复刻 (BM-01~05) 与节后工位爆款 (WS-06~10) 提示词的检索、动态注模与校验
2. 双引擎语法红线隔离：MJ V8 (--ar 1:1 --style raw --s 50/60 --v 8 --no English) 与 Gemini (Vertical 3:4 composition... Avoid:) 绝不混淆
3. 零第三方依赖：纯标准库实现 (pathlib, json, argparse, typing, re)
4. 支持三种调用形态：
   - Python 模块直接 import 调用 (函数式 API)
   - CLI 命令行直接执行 (支持 --list / --id / --export-json / --char-dir 动态渲染)
   - HTTP Server 微服务集成 (RESTful API 契约)
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# ==============================================================================
# 爆款提示词常量注册表 (Viral Prompts Registry) - 单一数据源
# ==============================================================================
VIRAL_PROMPT_REGISTRY: List[Dict[str, Any]] = [
    # ---------------- 专区 A: @思念如马3D打印真人手办 风格复刻 (5组) ----------------
    {
        "id": "BM-01",
        "category": "benchmark",
        "title": "【典雅旗袍·东方佳人立像】",
        "subtitle": "致敬爆款《照片定制把旗袍穿进3D打印里～》",
        "engine": "Midjourney V8",
        "aspect_ratio": "1:1",
        "is_cover": False,
        "tag_class": "mj",
        "target_audience": "国风佳人 / 旗袍爱好者 / 婚前留影",
        "prompt_cn": "东方古典刺绣旗袍年轻女性全彩树脂 3D 打印全身手办，立于极简象牙白圆形倒角展示底座上。手办身材修长匀称，淡粉色暗纹织锦旗袍剪裁利落，开衩细节考究。温婉黑发盘髻，嘴角带浅浅温柔笑意。极简暖燕麦色无缝影棚背景，柔光箱人像漫射光，Canon RF 100mm f/8 微距微焦点，呈现树脂表面细腻微哑光漆面与衣物纤维立体浮雕感。",
        "prompt_en": "Macro studio photograph of a 3D physical model, 12.0cm full-body 3D printed painted resin figurine, full-body standing on a minimalist white circular pedestal base, an elegant 28-year-old Chinese woman with gentle smiling eyes, neat dark hair bun, wearing a tailored sculpted soft-pink silk qipao with subtle embroidered damask textures, matte painted resin surface with delicate subsurface scattering, seamless warm oat-beige cyclorama studio backdrop, professional softbox illumination, shot on Canon RF 100mm f/8 macro lens --ar 1:1 --style raw --s 60 --v 8 --no English text, real living human, plastic shine, anime, porcelain doll, western features, room, furniture, outdoor",
        "template_en": "Macro studio photograph of a 3D physical model, {scale_desc} 3D printed painted resin figurine, full-body standing on a minimalist white circular pedestal base, {ifts}, wearing a tailored sculpted {clothing_desc}, matte painted resin surface with delicate subsurface scattering, seamless warm oat-beige cyclorama studio backdrop, professional softbox illumination, shot on Canon RF 100mm f/8 macro lens --ar 1:1 --style raw --s 60 --v 8 --no English text, real living human, plastic shine, anime, porcelain doll, western features, room, furniture, outdoor"
    },
    {
        "id": "BM-02",
        "category": "benchmark",
        "title": "【掌心托举·父母慈颜双尊像】",
        "subtitle": "致敬爆款《把父母做成3D雕像，她说这是她最大的遗憾》",
        "engine": "Gemini / Imagen",
        "aspect_ratio": "3:4",
        "is_cover": True,
        "tag_class": "cover",
        "target_audience": "白发至亲 / 父母双亲纪念 / 孝道感恩",
        "prompt_cn": "成年人温厚的手掌在胸前温柔托起一对微缩 6cm 全彩光敏树脂老夫妻胸像手办。左侧母亲身着米白斜襟棉麻小衫，发髻梳拢整齐，眼角笑纹温和安详；右侧父亲身着洗水灰蓝纽扣衬衫，胡茬泛白，面容慈祥亲切。真实成年人掌纹、指节纹理清晰可见，与微缩手办的面部微雕形成强烈尺度对比。极简浅灰水泥影棚背景柔和虚化，顶部预留干净留白便于小红书标题排版。",
        "prompt_en": "Vertical 3:4 composition. An adult human hand tenderly holding two 6.0cm miniature 3D printed painted resin bust figurines in the palm. The bust on the left is a 70-year-old Chinese mother with silver-threaded dark hair bun, gentle smiling crow's feet, wearing a sculpted white traditional cotton shirt; the bust on the right is a 72-year-old Chinese father with short silver stubble, warm kind smile, wearing a sculpted muted slate-blue buttoned shirt. Realistic palm skin creases and finger details contrasting with the miniature resin sculptures with subtle subsurface scattering finish. Soft blurred neutral studio backdrop. Leave clean negative space in the upper third for a title overlay. Shot on Sony A7R V with 50mm f/2.8 macro lens, authentic warm documentary tone. Avoid: English text, letters, anime, cartoon, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, funeral shrine, incense burner",
        "template_en": "Vertical 3:4 composition. An adult human hand tenderly holding {figurine_anchor} in the palm. Realistic palm skin creases and finger details contrasting with the miniature resin sculptures with subtle subsurface scattering finish. Soft blurred neutral studio backdrop. Leave clean negative space in the upper third for a title overlay. Shot on Sony A7R V with 50mm f/2.8 macro lens, authentic warm documentary tone. Avoid: English text, letters, anime, cartoon, CGI, glossy plastic doll, smooth airbrushed skin, western features, deformed hands, extra fingers, missing fingers, floating objects, funeral shrine, incense burner"
    },
    {
        "id": "BM-03",
        "category": "benchmark",
        "title": "【浪漫定格·白月光婚纱坐姿手办】",
        "subtitle": "致敬爆款《这是我的爱人？太美啦！》",
        "engine": "Midjourney V8",
        "aspect_ratio": "1:1",
        "is_cover": False,
        "tag_class": "mj",
        "target_audience": "情侣纪念 / 结婚一周年 / 伴侣惊喜礼物",
        "prompt_cn": "优雅年轻新娘全彩树脂 3D 打印手办，端庄坐于极简白色几何立方块上，底部紧固于双层圆形台座。身着雕刻精美褶皱的缎面纯白抹胸晚礼服长裙，裙摆顺垂而下，佩戴微缩珍珠耳坠与吊坠项链，盘发整齐，神态娇柔深情。纯净奶油杏色影棚背景，侧逆轮廓光勾勒发丝与天鹅颈线条，微距光影体现高级定制手办质感。",
        "prompt_en": "Macro studio photograph of a 3D physical model, 12.0cm full-body 3D printed painted resin figurine, full-body seated gracefully on a minimalist white geometric cubic block mounted on a circular craft pedestal, a beautiful 26-year-old Chinese bride with refined facial features, warm serene gaze, sculpted ivory-white satin strapless gown cascading in elegant folds, subtle painted resin texture, seamless cream-apricot studio cyclorama, balanced rim lighting and soft keylight, shot on Hasselblad X2D 100C with 120mm macro lens --ar 1:1 --style raw --s 55 --v 8 --no English text, real living human, anime, glossy plastic, wax figure, rough edges, cluttered room, western features",
        "template_en": "Macro studio photograph of a 3D physical model, {scale_desc} 3D printed painted resin figurine, full-body seated gracefully on a minimalist white geometric cubic block mounted on a circular craft pedestal, {ifts}, sculpted {clothing_desc}, subtle painted resin texture, seamless cream-apricot studio cyclorama, balanced rim lighting and soft keylight, shot on Hasselblad X2D 100C with 120mm macro lens --ar 1:1 --style raw --s 55 --v 8 --no English text, real living human, anime, glossy plastic, wax figure, rough edges, cluttered room, western features"
    },
    {
        "id": "BM-04",
        "category": "benchmark",
        "title": "【元气日常·青春女儿工装手办】",
        "subtitle": "致敬爆款《缩小版的闺女也太可爱了吧！》",
        "engine": "Gemini / Imagen",
        "aspect_ratio": "3:4",
        "is_cover": False,
        "tag_class": "gemini",
        "target_audience": "年轻女孩 / 闺蜜留念 / 亲子成长礼",
        "prompt_cn": "现代日常休闲风格年轻女孩全彩 3D 打印全身手办，亭亭玉立于纯白圆形微倒角底座上。女孩留着微卷长黑发，面容清秀甜美，身着粉色细吊带叠穿白色抹胸内搭与水洗深灰直筒牛仔裤，脚踩微缩白色运动板鞋。微距镜头捕捉牛仔裤缝线立体雕刻感与发丝分缕细节，极简暖米灰影棚背景，通透清新的自然漫射光线。",
        "prompt_en": "Vertical 3:4 composition. A high-precision 12.0cm 3D printed painted resin miniature full-body figurine of a lively 22-year-old Chinese young woman standing firmly on a clean circular white pedestal. She has natural long dark wavy hair, sweet gentle smile, wearing a sculpted dusty-pink camisole top and detailed charcoal-gray denim straight trousers with miniature white sneakers. Delicate painted resin finish with realistic fabric folds and matte texture. Seamless neutral studio background with soft wrap-around diffuse lighting. Shot on Canon EOS R5 with 85mm f/2 macro lens, natural lifestyle aesthetic. Avoid: English text, letters, watermark, anime, 3d render CGI, glossy toy plastic, smooth airbrushed skin, western features, deformed legs, extra toes, missing fingers, floating base",
        "template_en": "Vertical 3:4 composition. A high-precision {scale_desc} 3D printed painted resin miniature full-body figurine of {ifts} standing firmly on a clean circular white pedestal, wearing sculpted {clothing_desc}. Delicate painted resin finish with realistic fabric folds and matte texture. Seamless neutral studio background with soft wrap-around diffuse lighting. Shot on Canon EOS R5 with 85mm f/2 macro lens, natural lifestyle aesthetic. Avoid: English text, letters, watermark, anime, 3d render CGI, glossy toy plastic, smooth airbrushed skin, western features, deformed legs, extra toes, missing fingers, floating base"
    },
    {
        "id": "BM-05",
        "category": "benchmark",
        "title": "【儒雅风骨·退休老教师/学者尊师像】",
        "subtitle": "致敬爆款《教师节，把老师做成3D打印手办送给Ta》",
        "engine": "Midjourney V8",
        "aspect_ratio": "1:1",
        "is_cover": False,
        "tag_class": "mj",
        "target_audience": "退休老教师 / 资深学者 / 德高望重长辈",
        "prompt_cn": "68 岁德高望重的中国老教师全彩光敏树脂 3D 打印半身胸像，保持上半身，安装于深色胡桃木微倒角工艺底座。老人面容清癯睿智，戴着微缩复古黑框眼镜，眼含关切与鼓励笑意，鬓角花白梳理整齐，身着雕刻精巧的深灰立领中山装，左胸前别着一枚老式钢笔。影棚中性灰背景，45 度经典伦勃朗柔光，展现岁月积淀的师者风范。",
        "prompt_en": "Macro studio photograph of a 3D physical model, 6.0cm 3D printed painted resin bust, Keep the upper body, a distinguished 68-year-old Chinese male teacher, intelligent scholarly face with warm encouraging smile eyes, fine wrinkles, silver-streaked hair, sculpted vintage dark-rimmed spectacles, sculpted dark charcoal Mao collar tunic suit with a miniature fountain pen clipped to the pocket, mounted on a dark beveled walnut wood base, subtle resin SSS finish, neutral studio gray backdrop, classic Rembrandt soft lighting, shot on Nikon Z9 with 105mm f/2.8 micro lens --ar 1:1 --style raw --s 50 --v 8 --no English text, real living human, plaster pillar, porcelain doll, wax museum, youth, western features, chaotic room",
        "template_en": "Macro studio photograph of a 3D physical model, {scale_desc} 3D printed painted resin bust, Keep the upper body, {ifts}, sculpted {clothing_desc}, mounted on a dark beveled walnut wood base, subtle resin SSS finish, neutral studio gray backdrop, classic Rembrandt soft lighting, shot on Nikon Z9 with 105mm f/2.8 micro lens --ar 1:1 --style raw --s 50 --v 8 --no English text, real living human, plaster pillar, porcelain doll, wax museum, youth, western features, chaotic room"
    },

    # ---------------- 专区 B: 节后工位治愈好物 × 实体开箱对比爆款 (5组) ----------------
    {
        "id": "WS-06",
        "category": "workstation",
        "title": "【工位开箱·掌心手办 vs 手机老照片对望】",
        "subtitle": "★ 首屏 CTR 14%~16% 爆款第一候选",
        "engine": "Gemini / Imagen",
        "aspect_ratio": "3:4",
        "is_cover": True,
        "tag_class": "cover",
        "target_audience": "节后返工打工人 / 思乡共情 / 国庆全家福纪念",
        "prompt_cn": "小红书爆款封面构图。开工第一周的办公工位上，自然窗光侧射。前景中，一只年轻人的手掌在右侧轻托着 6cm 全彩光敏树脂老母亲慈祥笑颜手办（暗红毛衣配灰发髻）；左侧另一只手握着一部智能手机，屏幕上清晰显示着国庆节在老家客厅拍下的原版泛黄母亲生活照。背景为微微虚化的工位机械键盘、显示器边缘与一小盆绿萝。手办的真实树脂微瑕哑光质感与手机照片对望，情感张力极强。顶部 1/3 预留干净留白供大字排版。",
        "prompt_en": "Vertical 3:4 composition. An authentic office desk setting with natural window side-light. In the close foreground, a person's right hand holds a lifelike 6.0cm 3D printed painted resin bust of an elderly Chinese mother with silver hair bun and a warm crinkling smile wearing a maroon sweater; the left hand holds an open smartphone displaying the original vintage family snapshot of the same smiling mother on the screen. Blurred background shows an office computer keyboard, monitor edge, and a small green pothos desk plant. Realistic physical resin textures with matte finish and subtle handcrafted micro-details. Leave clean negative space in the upper third for a title overlay. Shot on Sony A7R V with 35mm f/2.0 lens, raw unedited documentary workplace aesthetic. Avoid: English text, letters, watermark, anime, CGI render, glossy plastic toy, western faces, deformed fingers, floating phone, cluttered trash, funeral altar, black-and-white portrait frame",
        "template_en": "Vertical 3:4 composition. An authentic office desk setting with natural window side-light. In the close foreground, a person's right hand holds {figurine_anchor}; the left hand holds an open smartphone displaying {photo_ref_desc}. Blurred background shows an office computer keyboard, monitor edge, and a small green pothos desk plant. Realistic physical resin textures with matte finish and subtle handcrafted micro-details. Leave clean negative space in the upper third for a title overlay. Shot on Sony A7R V with 35mm f/2.0 lens, raw unedited documentary workplace aesthetic. Avoid: English text, letters, watermark, anime, CGI render, glossy plastic toy, western faces, deformed fingers, floating phone, cluttered trash, funeral altar, black-and-white portrait frame"
    },
    {
        "id": "WS-07",
        "category": "workstation",
        "title": "【工位治愈·键盘边默默陪伴的奶奶手办】",
        "subtitle": "工作日抗疲劳与情感陪伴",
        "engine": "Gemini / Imagen",
        "aspect_ratio": "3:4",
        "is_cover": False,
        "tag_class": "gemini",
        "target_audience": "程序员 / 职场白领 / 办公室桌面治愈",
        "prompt_cn": "打工人办公桌桌面微距视点。一台点亮的笔记本电脑与无线机械键盘旁，摆放着一杯冒着微热气的咖啡，手办端端正正立在键盘右上方。手办为 6cm 全彩树脂雕塑，是一位系着黑红格子围巾、笑意盈盈的花白发外婆，一体化深色微倒角底座稳稳贴合桌面木纹。午后明亮的自然斜阳洒在桌面上，形成柔和的光影，营造出“开工再累，一抬头看见奶奶就在身边”的无限治愈感。",
        "prompt_en": "Vertical 3:4 composition. A healing office desk miniature still life. On a modern light oak office desktop, next to a wireless mechanical keyboard and a clean ceramic coffee mug, stands a 6.0cm 3D printed painted resin bust of a beloved Chinese grandmother with silver-gray hair, kind smiling eyes, wearing a red-and-black plaid knitted scarf, resting solidly on a dark beveled circular base. Warm golden afternoon sunlight slanting across the desk, casting gentle long shadows. Natural shallow depth of field with the computer screen softly blurred in the background. Shot on Fujifilm X-T5 with 56mm f/1.4 lens, authentic cinematic cozy workplace mood. Avoid: English text, letters, brand logos on computer, anime, cartoon, glossy toy finish, CGI render, youth, western features, messy desktop, broken geometry",
        "template_en": "Vertical 3:4 composition. A healing office desk miniature still life. On a modern light oak office desktop, next to a wireless mechanical keyboard and a clean ceramic coffee mug, stands {figurine_anchor}, resting solidly on a dark beveled circular base. Warm golden afternoon sunlight slanting across the desk, casting gentle long shadows. Natural shallow depth of field with the computer screen softly blurred in the background. Shot on Fujifilm X-T5 with 56mm f/1.4 lens, authentic cinematic cozy workplace mood. Avoid: English text, letters, brand logos on computer, anime, cartoon, glossy toy finish, CGI render, youth, western features, messy desktop, broken geometry"
    },
    {
        "id": "WS-08",
        "category": "workstation",
        "title": "【硬核开箱·防震定制黑珍珠棉与打样参数卡】",
        "subtitle": "破除纯 AI 疑虑·实体交付证明",
        "engine": "Gemini / Imagen",
        "aspect_ratio": "3:4",
        "is_cover": False,
        "tag_class": "gemini",
        "target_audience": "质检信任状 / 工艺硬核展示 / 开箱验货",
        "prompt_cn": "工位开箱俯拍 45 度微距特写。桌上放置着刚拆开的原色牛皮纸硬质礼盒，盒内精密开槽的高密度防震黑珍珠棉中，静静嵌卧着一尊刚收到的 12cm 全彩光敏树脂中国老父亲全身手办（身着工整深灰夹克与深色长裤，神情刚毅慈爱）。盒子一侧斜放着一张空白的微缩打样质检卡片与拭镜布，展现无滤镜工业级 3D 打印实体手办交付现场，质感沉稳坚实。",
        "prompt_en": "Vertical 3:4 composition. A top-down 45-degree macro view of a real unboxing moment on a wooden desk. An open rigid kraft-paper packaging box with precision custom-cut shockproof black pearl foam cushioning, inside which rests a freshly delivered 12.0cm 3D printed painted resin full-body figurine of an elderly Chinese father in a dark charcoal jacket. Next to the foam lies a blank miniature craft inspection card and a micro-fiber cleaning cloth. Natural desk daylight revealing the fine matte painted resin finish and solid tactile weight. Shot on Nikon Z8 with 50mm f/2.8 macro lens, documentary unboxing texture. Avoid: English text, readable letters, brand marks, anime, 3d CGI render, glossy cheap plastic, smooth doll skin, deformed hands, broken parts, dirty background",
        "template_en": "Vertical 3:4 composition. A top-down 45-degree macro view of a real unboxing moment on a wooden desk. An open rigid kraft-paper packaging box with precision custom-cut shockproof black pearl foam cushioning, inside which rests {figurine_anchor}. Next to the foam lies a blank miniature craft inspection card and a micro-fiber cleaning cloth. Natural desk daylight revealing the fine matte painted resin finish and solid tactile weight. Shot on Nikon Z8 with 50mm f/2.8 macro lens, documentary unboxing texture. Avoid: English text, readable letters, brand marks, anime, 3d CGI render, glossy cheap plastic, smooth doll skin, deformed hands, broken parts, dirty background"
    },
    {
        "id": "WS-09",
        "category": "workstation",
        "title": "【工位一隅·绿植多肉与老父亲手办的日光微景】",
        "subtitle": "清新治愈与桌面情感庇护所",
        "engine": "Gemini / Imagen",
        "aspect_ratio": "3:4",
        "is_cover": False,
        "tag_class": "gemini",
        "target_audience": "工位绿化角 / 自然清新风 / 阳台窗台摆件",
        "prompt_cn": "办公室窗台办公区域角落。白色陶瓷花盆中生机勃勃的多肉植物与文竹掩映下，立着一尊身着蓝布工作服的老父亲微缩全身 3D 手办。初秋清晨通透的清澈阳光透过百叶窗洒下斑驳光斑，照在手办沧桑而坚毅的面颊与树脂衣褶上。绿色生机与长辈温情手办融为一体，犹如工位上一座微缩的情感庇护所。",
        "prompt_en": "Vertical 3:4 composition. A refreshing office window sill miniature diorama. Beside a white ceramic pot of thriving succulent plants and green bamboo leaves, stands a 12.0cm 3D printed painted resin full-body figurine of an honorable 65-year-old Chinese father wearing a sculpted muted navy-blue work jacket and trousers. Morning sunbeams filtering through office window blinds, casting natural dappled light patterns across the figurine's weathered smiling face and resin folds. Shot on Sony A7 IV with 50mm f/1.8 lens, airy, peaceful, healing office atmosphere. Avoid: English text, letters, anime, cartoon, glossy toy shine, CGI, western face, deformed fingers, floating base, cluttered background",
        "template_en": "Vertical 3:4 composition. A refreshing office window sill miniature diorama. Beside a white ceramic pot of thriving succulent plants and green bamboo leaves, stands {figurine_anchor}. Morning sunbeams filtering through office window blinds, casting natural dappled light patterns across the figurine's weathered smiling face and resin folds. Shot on Sony A7 IV with 50mm f/1.8 lens, airy, peaceful, healing office atmosphere. Avoid: English text, letters, anime, cartoon, glossy toy shine, CGI, western face, deformed fingers, floating base, cluttered background"
    },
    {
        "id": "WS-10",
        "category": "workstation",
        "title": "【加班长夜·屏幕幽光中的温情灯塔】",
        "subtitle": "夜班情绪共鸣与回血力量",
        "engine": "Gemini / Imagen",
        "aspect_ratio": "3:4",
        "is_cover": False,
        "tag_class": "gemini",
        "target_audience": "深夜加班族 / 情感回血 / 亲情陪伴支撑",
        "prompt_cn": "深夜加班工位情感特写。周围办公室环境暗淡安静，电脑显示器散发着幽微柔和的冷色背光，而工位角落的一盏暖色护眼小台灯，则将一束温馨的暖黄光线精准聚拢在桌面的全彩手办上。手办为 6cm 慈祥老父亲半身胸像，目光温柔注视着正在加班奋斗的年轻人。桌上搁着一副摘下的眼镜与水杯，冷暖光影对比强烈，画面极具情感冲击力与陪伴自愈感。",
        "prompt_en": "Vertical 3:4 composition. An evocative late-night overtime office scene. Dim, quiet office surroundings with subtle cool ambient illumination from a computer monitor. A small warm LED desk lamp directs a soft cone of golden light onto a 6.0cm 3D printed painted resin bust of a benevolent Chinese father with silver hair and encouraging warm eyes. Resting next to the figurine are folded glasses and a ceramic mug. Dramatic contrast between the cool monitor glow and the warm golden lamplight highlighting the fine resin textures and loving expression. Shot on Canon EOS R6 with 50mm f/1.4 lens, cinematic, emotional, deep companionship. Avoid: English text, letters, computer code, anime, cartoon, 3d render CGI, plastic doll shine, western features, deformed face, creepy shadows, cemetery mood",
        "template_en": "Vertical 3:4 composition. An evocative late-night overtime office scene. Dim, quiet office surroundings with subtle cool ambient illumination from a computer monitor. A small warm LED desk lamp directs a soft cone of golden light onto {figurine_anchor}. Resting next to the figurine are folded glasses and a ceramic mug. Dramatic contrast between the cool monitor glow and the warm golden lamplight highlighting the fine resin textures and loving expression. Shot on Canon EOS R6 with 50mm f/1.4 lens, cinematic, emotional, deep companionship. Avoid: English text, letters, computer code, anime, cartoon, 3d render CGI, plastic doll shine, western features, deformed face, creepy shadows, cemetery mood"
    }
]


# ==============================================================================
# 核心业务 API 函数 (Python 脚本调用接口)
# ==============================================================================
def get_viral_prompts(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """获取爆款提示词列表，支持按分类 (benchmark / workstation) 过滤"""
    if not category:
        return copy.deepcopy(VIRAL_PROMPT_REGISTRY)
    cat_lower = category.strip().lower()
    return [copy.deepcopy(p) for p in VIRAL_PROMPT_REGISTRY if p["category"].lower() == cat_lower]


def get_viral_prompt_by_id(prompt_id: str) -> Optional[Dict[str, Any]]:
    """通过唯一 ID (如 BM-01, WS-06) 获取对应的提示词结构"""
    clean_id = prompt_id.strip().upper()
    for p in VIRAL_PROMPT_REGISTRY:
        if p["id"].upper() == clean_id:
            return copy.deepcopy(p)
    return None


def render_viral_prompt(
    prompt_id: str,
    char_profile: Optional[Dict[str, Any]] = None,
    override_params: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    依据长辈人设档案 (character_profile) 动态渲染高精爆款提示词
    :param prompt_id: 模板 ID (如 WS-06, BM-01)
    :param char_profile: 包含 ifts, title_cn, posture, cloth, heirloom 等字段的字典
    :param override_params: 额外覆盖参数字典
    :return: 渲染后的提示词对象字典 (含 rendered_prompt_en 与元数据)
    """
    base = get_viral_prompt_by_id(prompt_id)
    if not base:
        raise ValueError(f"未找到指定 ID 的爆款提示词模板: {prompt_id}")

    result = copy.deepcopy(base)
    if not char_profile:
        result["rendered_prompt_en"] = result["prompt_en"]
        result["is_customized"] = False
        return result

    # 提取人物特征
    ifts = char_profile.get("ifts", "").strip()
    title_cn = char_profile.get("title_cn", "长辈").strip()
    posture = char_profile.get("posture", "BM").upper()
    is_bust = posture in ("BW", "BM")
    scale_desc = "6.0cm bust" if is_bust else "12.0cm full-body figurine"
    clothing = char_profile.get("cloth", char_profile.get("clothing", "authentic traditional clothing"))
    
    # 构造锚点
    if ifts:
        figurine_anchor = (
            f"a {scale_desc} 3D printed painted resin {'bust' if is_bust else 'figurine'} of {ifts}"
        )
    else:
        figurine_anchor = f"a {scale_desc} 3D printed painted resin figurine of an elderly Chinese elder"

    photo_ref_desc = f"the original vintage family snapshot of the same smiling {title_cn} on the screen"

    context: Dict[str, Any] = {
        "ifts": ifts or "elderly Chinese person with warm smiling eyes",
        "scale_desc": scale_desc,
        "clothing_desc": clothing,
        "figurine_anchor": figurine_anchor,
        "photo_ref_desc": photo_ref_desc,
    }
    if override_params:
        context.update(override_params)

    # 替换模板占位符
    tpl = result.get("template_en", result["prompt_en"])
    rendered = tpl
    for k, v in context.items():
        rendered = rendered.replace(f"{{{k}}}", str(v))

    result["rendered_prompt_en"] = rendered
    result["is_customized"] = True
    result["injected_character"] = title_cn
    return result


def load_character_from_dir(char_dir: Union[str, Path]) -> Dict[str, Any]:
    """从本地长辈素材目录中解析人物基础档案（兼容 character.json, character_profile.md, prompts.md）"""
    path = Path(char_dir).resolve()
    data: Dict[str, Any] = {"dir": path.name}

    # 优先解析 character.json
    c_json = path / "character.json"
    if c_json.exists():
        try:
            with open(c_json, "r", encoding="utf-8") as f:
                d = json.load(f)
                data.update(d)
                return data
        except Exception:
            pass

    # 解析 prompts.json
    p_json = path / "prompts.json"
    if p_json.exists():
        try:
            with open(p_json, "r", encoding="utf-8") as f:
                d = json.load(f)
                if "ifts" in d:
                    data["ifts"] = d["ifts"]
                if "title_cn" in d:
                    data["title_cn"] = d["title_cn"]
                if "posture" in d:
                    data["posture"] = d["posture"]
                return data
        except Exception:
            pass

    # 正则提取 prompts.md
    p_md = path / "prompts.md"
    if p_md.exists():
        try:
            text = p_md.read_text(encoding="utf-8")
            ifts_m = re.search(r"## 0\.\s*人物唯一性指纹[^\`]*```text\s*([^`]+?)```", text)
            if ifts_m:
                data["ifts"] = ifts_m.group(1).strip()
            title_m = re.search(r"char_\d+_([B|F][W|M])_([^\n]+)", path.name)
            if title_m:
                data["posture"] = title_m.group(1)
                data["title_cn"] = title_m.group(2)
        except Exception:
            pass

    return data


def export_viral_prompts(format_type: str = "json", category: Optional[str] = None) -> str:
    """将提示词矩阵导出为 JSON 或 Markdown 文本格式"""
    prompts = get_viral_prompts(category)
    if format_type.lower() == "json":
        return json.dumps(prompts, ensure_ascii=False, indent=2)
    
    # 格式化为 Markdown
    md_lines = [
        "# 3D 全彩手办爆款生图提示词库 (Viral Prompts Registry)",
        "",
        f"> 导出时间: {Path(__file__).name} · 共 {len(prompts)} 组标准指令",
        ""
    ]
    for p in prompts:
        md_lines.extend([
            f"## [{p['id']}] {p['title']}",
            f"- **分类**：{p['category']} ｜ **引擎**：{p['engine']} ｜ **画幅**：`{p['aspect_ratio']}`",
            f"- **定位**：{p['subtitle']}",
            "#### 中文释义",
            p["prompt_cn"],
            "#### 英文生图指令",
            "```text",
            p["prompt_en"],
            "```",
            ""
        ])
    return "\n".join(md_lines)


# ==============================================================================
# CLI 命令行入口
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(description="3D 全彩手办爆款提示词引擎 v5.1")
    parser.add_argument("--list", action="store_true", help="打印当前已注册的 10 组爆款提示词清单")
    parser.add_argument("--category", choices=["benchmark", "workstation"], help="按分类过滤 (对标或工位)")
    parser.add_argument("--id", help="查看指定编号的提示词详细信息 (如 BM-01, WS-06)")
    parser.add_argument("--char-dir", help="指定人物素材目录，动态提取 IFTS 并注模渲染")
    parser.add_argument("--render", help="指定要渲染的提示词 ID (需配合 --char-dir 使用)")
    parser.add_argument("--export-json", nargs="?", const="-", help="导出为 JSON 格式（可指定输出文件，缺省输出到终端）")
    parser.add_argument("--export-md", nargs="?", const="-", help="导出为 Markdown 格式（可指定输出文件，缺省输出到终端）")

    args = parser.parse_args()

    if args.list:
        prompts = get_viral_prompts(args.category)
        print(f"\n🔥 已注册爆款提示词矩阵 (共 {len(prompts)} 组):\n")
        print(f"{'ID':<8} {'引擎/画幅':<20} {'标题':<24} {'定位/爆款来源'}")
        print("-" * 85)
        for p in prompts:
            engine_str = f"{p['engine']} ({p['aspect_ratio']})"
            print(f"{p['id']:<8} {engine_str:<20} {p['title']:<24} {p['subtitle']}")
        print("")
        return

    if args.id and not args.char_dir:
        p = get_viral_prompt_by_id(args.id)
        if not p:
            print(f"❌ 错误: 未找到 ID 为 {args.id} 的提示词", file=sys.stderr)
            sys.exit(1)
        print(f"\n{'='*70}")
        print(f"【{p['id']}】{p['title']} ({p['engine']} · {p['aspect_ratio']})")
        print(f"定位：{p['subtitle']}")
        print(f"适用群体：{p.get('target_audience', '通用')}")
        print(f"{'-'*70}")
        print(f"中文释义：\n{p['prompt_cn']}\n")
        print(f"英文指令：\n{p['prompt_en']}")
        print(f"{'='*70}\n")
        return

    if args.char_dir:
        char_data = load_character_from_dir(args.char_dir)
        render_id = args.render or args.id or "WS-06"
        rendered = render_viral_prompt(render_id, char_data)
        print(f"\n🎨 已为长辈 [{char_data.get('title_cn', char_data.get('dir'))}] 成功注模爆款场景 【{rendered['id']}】")
        print(f"引擎与画幅：{rendered['engine']} · {rendered['aspect_ratio']}")
        print(f"英文指令：\n\n{rendered['rendered_prompt_en']}\n")
        return

    if args.export_json:
        out = export_viral_prompts("json", args.category)
        if args.export_json == "-":
            print(out)
        else:
            Path(args.export_json).write_text(out, encoding="utf-8")
            print(f"✅ 成功导出 JSON 提示词至: {args.export_json}")
        return

    if args.export_md:
        out = export_viral_prompts("md", args.category)
        if args.export_md == "-":
            print(out)
        else:
            Path(args.export_md).write_text(out, encoding="utf-8")
            print(f"✅ 成功导出 Markdown 提示词至: {args.export_md}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
