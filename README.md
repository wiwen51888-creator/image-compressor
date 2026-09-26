# image-compressor

图片批量压缩工具。在尽量保持画质的前提下减小图片体积，支持 JPG / PNG / WebP。

## 安装

```bash
pip install -r requirements.txt
```

## 用法

```bash
# 压缩整个目录，输出到 ./out
python compress.py ./photos --out ./out

# 指定质量（1-100，默认 82）
python compress.py ./photos --quality 70

# 限制最大边长（超过则等比缩放）
python compress.py ./photos --max-size 1920

# 转换格式为 webp
python compress.py ./photos --format webp
```

## 参数

- `--out`：输出目录（默认在源目录旁建 out/）
- `--quality`：压缩质量 1-100（默认 82）
- `--max-size`：最大边长，超过则等比缩放
- `--format`：输出格式 jpg / png / webp（默认保持原格式）
- `--recursive`：递归子目录

## 效果

输出时会打印每张图片的原始大小、压缩后大小和压缩率。