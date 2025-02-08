# webpage_archive

This directory contains the archived webpages.

- news_ifeng: the webpages of ifeng news. pattern '.*news.ifeng.*'
- news_sina: the webpages of sina news. pattern '.*news.sina.*'
- unclassify_news: the webpages of unclassify news. pattern '.*news.*'

## process and clean files

```sh
python scripts/workflow.py /home/yunwei37/trans-digital-cn/.github/downloader/webpage_archive/new_all_results/20250123_res

cd cd /home/yunwei37/trans-digital-cn/
python .github/downloader/file_processor.py /home/yunwei37/trans-digital-cn/.github/downloader/webpage_archive/new_all_results/20250123_res /home/yunwei37/trans-digital-cn/.github/downloader/content_archive/workspace

cd /home/yunwei37/trans-digital-cn/.github/downloader/content_archive/
python /home/yunwei37/trans-digital-cn/.github/downloader/content_archive/.github/scripts/workspace/organize_files.py
```
