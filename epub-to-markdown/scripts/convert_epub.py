#!/usr/bin/env python3
"""
EPUB to Markdown Converter

纯 Python 实现，使用 zipfile 直接提取 EPUB 内容。
EPUB 本质是 ZIP 格式，包含 HTML/XHTML 文件和资源。
"""
import argparse
import json
import os
import re
import sys
import zipfile
from pathlib import Path
from html.parser import HTMLParser
from html.entities import name2codepoint
from xml.etree import ElementTree as ET


class MarkdownExtractor(HTMLParser):
    """HTML to Markdown 转换器"""

    def __init__(self):
        super().__init__()
        self.markdown = []
        self.in_style = False
        self.in_script = False
        self.list_depth = 0
        self.list_type = []  # 'ul' or 'ol'
        self.current_list_item = []

    def handle_starttag(self, tag, attrs):
        self.in_style = tag in ['style', 'script']
        if self.in_style:
            return

        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = tag[1]
            self.markdown.append(f"\n\n{'#' * int(level)} ")

        elif tag == 'p':
            if self.markdown and not self.markdown[-1].endswith('\n\n'):
                self.markdown.append('\n\n')

        elif tag == 'br':
            self.markdown.append('  \n')

        elif tag in ['b', 'strong']:
            self.markdown.append('**')

        elif tag in ['i', 'em']:
            self.markdown.append('*')

        elif tag == 'a':
            href = dict(attrs).get('href', '')
            self.markdown.append('[')
            self.current_href = href

        elif tag in ['ul', 'ol']:
            self.list_depth += 1
            self.list_type.append('ul' if tag == 'ul' else 'ol')
            self.markdown.append('\n')

        elif tag == 'li':
            indent = '  ' * (self.list_depth - 1)
            if self.list_type and self.list_type[-1] == 'ol':
                self.markdown.append(f'{ind}1. ')
            else:
                self.markdown.append(f'{ind}- ')

        elif tag == 'img':
            src = dict(attrs).get('src', '')
            alt = dict(attrs).get('alt', '')
            self.markdown.append(f'![{alt}]({src})')

        elif tag == 'blockquote':
            self.markdown.append('> ')

        elif tag == 'code':
            self.markdown.append('`')

        elif tag == 'pre':
            self.markdown.append('\n```\n')

        elif tag == 'hr':
            self.markdown.append('\n\n---\n\n')

    def handle_endtag(self, tag):
        self.in_style = False

        if tag in ['b', 'strong']:
            self.markdown.append('**')

        elif tag in ['i', 'em']:
            self.markdown.append('*')

        elif tag == 'a':
            href = getattr(self, 'current_href', '')
            self.markdown.append(f']({href})')

        elif tag in ['ul', 'ol']:
            self.list_depth -= 1
            if self.list_type:
                self.list_type.pop()
            self.markdown.append('\n')

        elif tag == 'code':
            self.markdown.append('`')

        elif tag == 'pre':
            self.markdown.append('\n```\n\n')

    def handle_data(self, data):
        if self.in_style or self.in_script:
            return
        self.markdown.append(data)

    def handle_entityref(self, name):
        if name in name2codepoint:
            self.markdown.append(chr(name2codepoint[name]))

    def handle_charref(self, name):
        try:
            self.markdown.append(chr(int(name[1:] if name.startswith('x') else name)))
        except ValueError:
            pass

    def get_markdown(self):
        return ''.join(self.markdown).strip()


def parse_epub_metadata(epub_path):
    """解析 EPUB 元数据"""
    with zipfile.ZipFile(epub_path, 'r') as zf:
        # 查找 .opf 文件
        opf_files = [f for f in zf.namelist() if f.endswith('.opf')]
        if not opf_files:
            return {}

        with zf.open(opf_files[0]) as f:
            tree = ET.parse(f)
            root = tree.getroot()

            # 命名空间
            ns = {'dc': 'http://purl.org/dc/elements/1.1/',
                  'opf': 'http://www.idpf.org/2007/opf'}

            metadata = {}
            title_elem = root.find('dc:title', ns)
            if title_elem is not None:
                metadata['title'] = title_elem.text

            creator_elem = root.find('dc:creator', ns)
            if creator_elem is not None:
                metadata['author'] = creator_elem.text

            language_elem = root.find('dc:language', ns)
            if language_elem is not None:
                metadata['language'] = language_elem.text

            publisher_elem = root.find('dc:publisher', ns)
            if publisher_elem is not None:
                metadata['publisher'] = publisher_elem.text

            identifier_elem = root.find('dc:identifier', ns)
            if identifier_elem is not None:
                metadata['isbn'] = identifier_elem.text

            return metadata


def get_content_files(epub_path):
    """获取 EPUB 中的内容文件列表（按阅读顺序）"""
    with zipfile.ZipFile(epub_path, 'r') as zf:
        # 查找 .opf 文件
        opf_files = [f for f in zf.namelist() if f.endswith('.opf')]
        if not opf_files:
            return []

        with zf.open(opf_files[0]) as f:
            tree = ET.parse(f)
            root = tree.getroot()

            # 查找 manifest
            ns = {'opf': 'http://www.idpf.org/2007/opf'}
            manifest = root.find('opf:manifest', ns)

            if manifest is None:
                return []

            # 获取所有 HTML/XHTML 文件
            items = manifest.findall('opf:item', ns)
            content_files = []

            for item in items:
                media_type = item.get('media-type', '')
                href = item.get('href', '')

                if 'html' in media_type or href.endswith(('.html', '.xhtml')):
                    # 获取完整路径
                    opf_dir = os.path.dirname(opf_files[0])
                    full_path = os.path.normpath(os.path.join(opf_dir, href))
                    content_files.append(full_path)

            return content_files


def extract_images(epub_path, output_dir):
    """提取 EPUB 中的图片"""
    output_dir = Path(output_dir)
    images_dir = output_dir / 'images'
    images_dir.mkdir(parents=True, exist_ok=True)

    image_mapping = {}

    with zipfile.ZipFile(epub_path, 'r') as zf:
        for name in zf.namelist():
            if name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                # 保留原始文件名
                filename = os.path.basename(name)
                output_path = images_dir / filename

                with zf.open(name) as source, open(output_path, 'wb') as target:
                    target.write(source.read())

                # 记录原始路径到本地路径的映射
                image_mapping[name] = f'images/{filename}'

    return image_mapping


def convert_epub_to_markdown(epub_path, output_dir, extract_images_flag=False,
                             split_chapters=False):
    """将 EPUB 转换为 Markdown"""
    epub_path = Path(epub_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"📖 正在处理: {epub_path.name}")

    # 解析元数据
    print("   解析元数据...")
    metadata = parse_epub_metadata(epub_path)
    metadata['source_file'] = epub_path.name

    # 提取图片
    image_mapping = {}
    if extract_images_flag:
        print("   提取图片...")
        image_mapping = extract_images(epub_path, output_dir)
        print(f"   已提取 {len(image_mapping)} 张图片")

    # 获取内容文件
    content_files = get_content_files(epub_path)
    print(f"   找到 {len(content_files)} 个内容文件")

    # 转换内容
    all_content = []
    chapters = []

    with zipfile.ZipFile(epub_path, 'r') as zf:
        for i, content_file in enumerate(content_files, 1):
            if content_file not in zf.namelist():
                continue

            print(f"   转换文件 {i}/{len(content_files)}: {os.path.basename(content_file)}")

            with zf.open(content_file) as f:
                html_content = f.read().decode('utf-8', errors='ignore')

            # 转换为 Markdown
            extractor = MarkdownExtractor()
            extractor.feed(html_content)
            markdown_content = extractor.get_markdown()

            # 更新图片路径
            for orig_path, new_path in image_mapping.items():
                markdown_content = markdown_content.replace(orig_path, new_path)

            if split_chapters:
                # 检测章节标题
                title_match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1).strip()
                else:
                    title = f"Chapter_{i:02d}"

                # 清理文件名
                safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
                chapter_file = output_dir / 'chapters' / f"chapter_{i:02d}_{safe_title}.md"

                (output_dir / 'chapters').mkdir(exist_ok=True)

                with open(chapter_file, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)

                chapters.append({
                    'id': f'ch{i}',
                    'title': title,
                    'file': f"chapters/{chapter_file.name}"
                })

            all_content.append(markdown_content)

    # 生成完整 Markdown
    full_markdown = f"# {metadata.get('title', '未知标题')}\n\n"
    full_markdown += f"**作者**: {metadata.get('author', '未知')}\n\n"
    full_markdown += "---\n\n"
    full_markdown += '\n\n'.join(all_content)

    if split_chapters:
        full_file = output_dir / 'full_book.md'
        metadata['chapters'] = chapters
    else:
        # 使用书名作为文件名
        safe_title = re.sub(r'[<>:"/\\|?*]', '_', metadata.get('title', 'output'))
        full_file = output_dir / f"{safe_title}.md"

    with open(full_file, 'w', encoding='utf-8') as f:
        f.write(full_markdown)

    # 保存元数据
    metadata_file = output_dir / 'book_metadata.json'
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    # 统计信息
    word_count = len(full_markdown.split())

    print(f"\n✅ 转换完成!")
    print(f"📄 输出文件: {full_file.name}")
    print(f"📊 字数: 约 {word_count:,} 字")
    if extract_images_flag:
        print(f"🖼️ 图片: 已提取 {len(image_mapping)} 张")
    if split_chapters:
        print(f"📖 章节: 已拆分 {len(chapters)} 章")
    print(f"📁 保存位置: {output_dir}")

    return {
        'success': True,
        'output_file': str(full_file),
        'metadata_file': str(metadata_file),
        'word_count': word_count,
        'image_count': len(image_mapping),
        'chapter_count': len(chapters) if split_chapters else 0
    }


def batch_convert(input_dir, output_dir, **kwargs):
    """批量转换 EPUB 文件"""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    epub_files = list(input_dir.glob('*.epub'))

    if not epub_files:
        print(f"❌ 在 {input_dir} 中未找到 EPUB 文件")
        return

    print(f"📚 找到 {len(epub_files)} 个 EPUB 文件\n")

    results = []
    for i, epub_file in enumerate(epub_files, 1):
        print(f"\n[{i}/{len(epub_files)}] ", end='')
        book_output = output_dir / epub_file.stem

        try:
            result = convert_epub_to_markdown(epub_file, book_output, **kwargs)
            results.append(result)
        except Exception as e:
            print(f"❌ 转换失败: {e}")
            results.append({'success': False, 'error': str(e)})

    # 汇总
    successful = sum(1 for r in results if r.get('success'))
    print(f"\n\n{'='*50}")
    print(f"✅ 批量转换完成: {successful}/{len(epub_files)} 成功")


def main():
    parser = argparse.ArgumentParser(
        description='将 EPUB 电子书转换为 Markdown 格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 转换单个文件
  python convert_epub.py book.epub -o output

  # 批量转换
  python convert_epub.py --batch ~/Downloads/epubs -o output

  # 提取图片
  python convert_epub.py book.epub -o output --extract-images

  # 按章节拆分
  python convert_epub.py book.epub -o output --split-chapters
        """
    )

    parser.add_argument('input', nargs='?', help='EPUB 文件或目录（批量模式）')
    parser.add_argument('-o', '--output', default='output', help='输出目录')
    parser.add_argument('--batch', action='store_true', help='批量转换模式')
    parser.add_argument('--extract-images', action='store_true',
                        help='提取图片到 images/ 目录')
    parser.add_argument('--split-chapters', action='store_true',
                        help='按章节拆分为多个文件')

    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        return

    kwargs = {
        'extract_images_flag': args.extract_images,
        'split_chapters': args.split_chapters
    }

    if args.batch:
        batch_convert(args.input, args.output, **kwargs)
    else:
        convert_epub_to_markdown(args.input, args.output, **kwargs)


if __name__ == '__main__':
    main()
