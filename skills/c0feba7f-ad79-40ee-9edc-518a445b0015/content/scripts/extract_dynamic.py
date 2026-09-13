"""
clerk 技能辅助脚本：读取动态分析报告并提取关键数据
用法: python3 extract_dynamic.py <动态报告路径>
输出: JSON 格式的提取结果
"""
import sys
import json
import re
from docx import Document


def find_table_by_header(doc, header_cells):
    """通过表头内容定位表格"""
    for i, table in enumerate(doc.tables):
        if len(table.rows) > 0:
            first_row = [cell.text.strip() for cell in table.rows[0].cells]
            if all(h in first_row for h in header_cells):
                return i, table
    return None, None


def parse_frequency_cell(cell_text):
    """
    解析调用频次列的文本，提取SDK和调用次数
    格式: SDK包名(SDK中文名, 调用N次)\nSDK包名2(...)
    返回: [(sdk_full_name, count), ...]
    """
    results = []
    total = 0
    lines = cell_text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        match = re.search(r'调用(\d+)次', line)
        if match:
            count = int(match.group(1))
            total += count
            sdk_name = line.split('(')[0].strip() if '(' in line else line
            paren_match = re.match(r'^([^(]+)\(([^,)]+)', line)
            if paren_match:
                sdk_id = paren_match.group(1).strip()
                sdk_cn = paren_match.group(2).strip()
                results.append({
                    'sdk_id': sdk_id,
                    'sdk_name': sdk_cn,
                    'count': count,
                    'raw': line
                })
            else:
                results.append({
                    'sdk_id': sdk_name,
                    'sdk_name': '',
                    'count': count,
                    'raw': line
                })
    return results, total


def extract_api_table(table):
    """提取API调用频次表"""
    apis = []
    for i, row in enumerate(table.rows):
        if i == 0:
            continue
        cells = [cell.text.strip() for cell in row.cells]
        if len(cells) >= 2:
            api_name = cells[0]
            freq_text = cells[1]
            sdk_details, total_count = parse_frequency_cell(freq_text)
            apis.append({
                'api_name': api_name,
                'total_count': total_count,
                'sdk_details': sdk_details,
                'raw_freq': freq_text
            })
    return apis


def extract_sdk_table(table):
    """提取SDK调用表"""
    sdks = []
    for i, row in enumerate(table.rows):
        if i == 0:
            continue
        cells = [cell.text.strip() for cell in row.cells]
        if len(cells) >= 2:
            sdk_full = cells[0]
            apis_text = cells[1]
            sdk_match = re.match(r'^([^(]+)\(([^)]+)\)', sdk_full)
            if sdk_match:
                sdk_id = sdk_match.group(1).strip()
                sdk_cn = sdk_match.group(2).strip()
            else:
                sdk_id = sdk_full
                sdk_cn = ''
            api_list = [a.strip() for a in apis_text.split('\n') if a.strip()]
            sdks.append({
                'sdk_id': sdk_id,
                'sdk_name': sdk_cn,
                'sdk_full': sdk_full,
                'apis': api_list
            })
    return sdks


def main():
    if len(sys.argv) < 2:
        print("用法: python3 extract_dynamic.py <动态报告路径>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    doc = Document(path)

    # 提取样本信息
    sample_info = {}
    if len(doc.tables) > 0:
        for row in doc.tables[0].rows:
            cells = [cell.text.strip() for cell in row.cells]
            if len(cells) >= 2:
                sample_info[cells[0]] = cells[1]

    # 定位API调用频次表（同意前/同意后）
    _, api_before_table = find_table_by_header(doc, ['API名称', '调用频次(同意前)'])
    _, api_after_table = find_table_by_header(doc, ['API名称', '调用频次(同意后)'])
    _, sdk_before_table = find_table_by_header(doc, ['SDK名称', 'API名称(同意前)'])
    _, sdk_after_table = find_table_by_header(doc, ['SDK名称', 'API名称(同意后)'])

    result = {
        'sample_info': sample_info,
        'api_before': extract_api_table(api_before_table) if api_before_table else [],
        'api_after': extract_api_table(api_after_table) if api_after_table else [],
        'sdk_before': extract_sdk_table(sdk_before_table) if sdk_before_table else [],
        'sdk_after': extract_sdk_table(sdk_after_table) if sdk_after_table else [],
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
