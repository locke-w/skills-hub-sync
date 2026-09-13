"""
clerk 技能辅助脚本：填写工信部报告
用法: python3 fill_report.py <工信部报告路径> <动态数据JSON路径> <输出路径> [--highlight-json <高亮项JSON>]

动态数据JSON: extract_dynamic.py 的输出
高亮项JSON: 需要黄色高亮的API名称列表 (可选)
"""
import sys
import json
import re
import argparse
from docx import Document
from docx.oxml.ns import qn


def find_report_table(doc, keyword):
    """通过关键词定位工信部报告中的表格"""
    for i, table in enumerate(doc.tables):
        if len(table.rows) >= 2:
            row0_text = ' '.join(cell.text.strip() for cell in table.rows[0].cells)
            if keyword in row0_text:
                return i, table
    return None, None


def clear_cell(cell):
    """清空单元格内容"""
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.text = ''
    if cell.paragraphs:
        cell.paragraphs[0].text = ''


def write_cell_with_highlight(cell, lines, highlight_lines=None):
    """
    向单元格写入多行文本，支持黄色高亮
    lines: [(text, should_highlight), ...]
    """
    clear_cell(cell)
    p = cell.paragraphs[0] if cell.paragraphs else cell.add_paragraph()

    for i, (text, highlight) in enumerate(lines):
        if i > 0:
            run = p.add_run('\n')
        run = p.add_run(text)
        if highlight:
            rPr = run._element.get_or_add_rPr()
            highlight_elem = rPr.makeelement(qn('w:highlight'), {qn('w:val'): 'yellow'})
            rPr.append(highlight_elem)


def format_api_for_211(api_data):
    """格式化API数据用于2.1.1序号2"""
    lines = []
    for api in api_data:
        api_name = api['api_name']
        details = []
        for sdk in api['sdk_details']:
            if sdk['sdk_name']:
                details.append(f"{sdk['sdk_id']}({sdk['sdk_name']}, 调用{sdk['count']}次)")
            else:
                details.append(f"{sdk['sdk_id']}(调用{sdk['count']}次)")
        line = f"{api_name}：{'、'.join(details)}"
        lines.append((line, False))
    return lines


def format_sdk_for_211(sdk_data, missing_sdks=None):
    """格式化SDK数据用于2.1.1序号3，标注隐私政策未声明的SDK"""
    lines = []
    if missing_sdks is None:
        missing_sdks = set()

    for sdk in sdk_data:
        is_missing = sdk['sdk_id'] in missing_sdks or sdk['sdk_full'] in missing_sdks
        prefix = "【未声明】" if is_missing else ""
        api_list = '、'.join(sdk['apis'])
        line = f"{prefix}{sdk['sdk_full']}：{api_list}"
        lines.append((line, is_missing))
    return lines


def format_api_for_212(api_data):
    """
    格式化API数据用于2.1.2序号2
    - 删除总频次<=2的
    - 高亮总频次>10的
    """
    lines = []
    for api in api_data:
        total = api['total_count']
        if total <= 2:
            continue
        highlight = total > 10

        details = []
        for sdk in api['sdk_details']:
            if sdk['sdk_name']:
                details.append(f"{sdk['sdk_id']}({sdk['sdk_name']}, 调用{sdk['count']}次)")
            else:
                details.append(f"{sdk['sdk_id']}(调用{sdk['count']}次)")

        line = f"{api['api_name']}(共{total}次)：{'、'.join(details)}"
        lines.append((line, highlight))
    return lines


def main():
    parser = argparse.ArgumentParser(description='填写工信部报告')
    parser.add_argument('report_path', help='工信部报告路径')
    parser.add_argument('data_path', help='动态数据JSON路径')
    parser.add_argument('output_path', help='输出文件路径')
    parser.add_argument('--missing-sdks', help='隐私政策未声明的SDK列表JSON文件', default=None)
    args = parser.parse_args()

    with open(args.data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    missing_sdks = set()
    if args.missing_sdks:
        with open(args.missing_sdks, 'r', encoding='utf-8') as f:
            missing_sdks = set(json.load(f))

    doc = Document(args.report_path)

    # 定位 2.1.1 违规收集个人信息表格
    idx_211, table_211 = find_report_table(doc, '违规收集个人信息')
    if table_211 is None:
        print("警告：未找到违规收集个人信息表格", file=sys.stderr)
    else:
        # 序号2（通常是行4）: API信息
        # 寻找序号2所在的行
        for i, row in enumerate(table_211.rows):
            cells = [cell.text.strip() for cell in row.cells]
            if len(cells) > 0 and cells[0] == '2':
                api_lines = format_api_for_211(data['api_after'])
                write_cell_with_highlight(row.cells[2], api_lines)
                print(f"已填写 2.1.1 序号2（行{i}）：{len(api_lines)} 条API记录")
                break

        # 序号3（通常是行5）: SDK信息
        for i, row in enumerate(table_211.rows):
            cells = [cell.text.strip() for cell in row.cells]
            if len(cells) > 0 and cells[0] == '3':
                sdk_lines = format_sdk_for_211(data['sdk_after'], missing_sdks)
                write_cell_with_highlight(row.cells[2], sdk_lines)
                print(f"已填写 2.1.1 序号3（行{i}）：{len(sdk_lines)} 条SDK记录")
                break

    # 定位 2.1.2 超范围收集个人信息表格
    idx_212, table_212 = find_report_table(doc, '超范围收集个人信息')
    if table_212 is None:
        print("警告：未找到超范围收集个人信息表格", file=sys.stderr)
    else:
        # 序号2: 超频次API信息
        for i, row in enumerate(table_212.rows):
            cells = [cell.text.strip() for cell in row.cells]
            if len(cells) > 0 and cells[0] == '2':
                freq_lines = format_api_for_212(data['api_after'])
                write_cell_with_highlight(row.cells[2], freq_lines)
                print(f"已填写 2.1.2 序号2（行{i}）：{len(freq_lines)} 条超频次API记录")
                break

    doc.save(args.output_path)
    print(f"\n报告已保存至: {args.output_path}")


if __name__ == '__main__':
    main()
