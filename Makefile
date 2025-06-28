raw/ifeng.com/page.yml:
	python scripts/config/old_config.py raw/ifeng.com/results.json raw/ifeng.com/page.yml
	python scripts/config/new_config.py raw/ifeng.com/results1.json raw/ifeng.com/page.yml
	python scripts/config/new_config.py raw/ifeng.com/results2.json raw/ifeng.com/page.yml
	python scripts/config/add_meta.py raw/ifeng.com/page.yml

raw/sina.cn/page.yml:
	python scripts/config/old_config.py raw/sina.cn/results.json raw/sina.cn/page.yml
	python scripts/config/new_config.py raw/sina.cn/results1.json raw/sina.cn/page.yml
	python scripts/config/new_config.py raw/sina.cn/results2.json raw/sina.cn/page.yml
	python scripts/config/add_meta.py raw/sina.cn/page.yml

raw/thepaper.cn/page.yml:
	python scripts/config/new_config.py raw/thepaper.cn/results.json raw/thepaper.cn/page.yml
	python scripts/config/new_config.py raw/thepaper.cn/results1.json raw/thepaper.cn/page.yml
	python scripts/config/add_meta.py raw/thepaper.cn/page.yml

raw/sohu.com/page.yml:
	python scripts/config/new_config.py raw/sohu.com/results.json raw/sohu.com/page.yml
	python scripts/config/new_config.py raw/sohu.com/results1.json raw/sohu.com/page.yml
	python scripts/config/new_config.py raw/sohu.com/results2.json raw/sohu.com/page.yml
	python scripts/config/add_meta.py raw/sohu.com/page.yml

raw/chinanews.com/page.yml:
	python scripts/config/new_config.py raw/chinanews.com/results.json raw/chinanews.com/page.yml
	python scripts/config/add_meta.py raw/chinanews.com/page.yml

raw/163.com/page.yml:
	python scripts/config/new_config.py raw/163.com/results.json raw/163.com/page.yml
	python scripts/config/new_config.py raw/163.com/results1.json raw/163.com/page.yml
	python scripts/config/add_meta.py raw/163.com/page.yml

raw/news.qq.com/page.yml:
	python scripts/config/new_config.py raw/news.qq.com/results.json raw/news.qq.com/page.yml
	python scripts/config/add_meta.py raw/news.qq.com/page.yml

raw/unclassify_news/page.yml:
	python scripts/config/old_config.py raw/unclassify_news/results.json raw/unclassify_news/page.yml
	python scripts/config/new_config.py raw/unclassify_news/results1.json raw/unclassify_news/page.yml
	python scripts/config/add_meta.py raw/unclassify_news/page.yml

.PHONY: ifeng.com
ifeng.com: raw/ifeng.com/page.yml
	python scripts/batch.py  raw/ifeng.com/ cleaned/ifeng.com/ ./scripts/cleaner/clean_cheerio.js HTML_CLEANER_CONFIG=./scripts/cleaner/configs/ifeng.com.json 
	python scripts/batch.py  cleaned/ifeng.com/ markdown/ifeng.com/ scripts/markdown/html2md.js

	python scripts/ai/process_dir.py markdown/ifeng.com/ ready/ifeng.com/ scripts/ai/prompt/clean.template  --skip-size-check

.PHONY: sina.cn
sina.cn: raw/sina.cn/page.yml

	python scripts/batch.py  raw/sina.cn/ cleaned/sina.cn/ ./scripts/cleaner/clean_cheerio.js HTML_CLEANER_CONFIG=./scripts/cleaner/configs/sina.cn.json 
	python scripts/batch.py  cleaned/sina.cn/ markdown/sina.cn/ scripts/markdown/html2md.js

	python scripts/ai/process_dir.py markdown/sina.cn/ ready/sina.cn/ scripts/ai/prompt/clean.template  --skip-size-check

.PHONY: thepaper.cn
thepaper.cn: raw/thepaper.cn/page.yml

	python scripts/batch.py  raw/thepaper.cn/ cleaned/thepaper.cn/ ./scripts/cleaner/clean_cheerio.js HTML_CLEANER_CONFIG=./scripts/cleaner/configs/thepaper.cn.json 
	python scripts/batch.py  cleaned/thepaper.cn/ markdown/thepaper.cn/ scripts/markdown/html2md.js

	python scripts/ai/process_dir.py markdown/thepaper.cn/ ready/thepaper.cn/ scripts/ai/prompt/clean.template

.PHONY: sohu.com
sohu.com: raw/sohu.com/page.yml

	python scripts/batch.py  raw/sohu.com/ cleaned/sohu.com/ ./scripts/cleaner/clean_cheerio.js HTML_CLEANER_CONFIG=./scripts/cleaner/configs/sohu.com.json 
	python scripts/batch.py  cleaned/sohu.com/ markdown/sohu.com/ scripts/markdown/html2md.js

	python scripts/ai/process_dir.py markdown/sohu.com/ ready/sohu.com/ scripts/ai/prompt/clean.template  --skip-size-check

.PHONY: chinanews.com
chinanews.com: raw/chinanews.com/page.yml

	python scripts/batch.py  raw/chinanews.com/ cleaned/chinanews.com/ ./scripts/cleaner/clean_cheerio.js HTML_CLEANER_CONFIG=./scripts/cleaner/configs/chinanews.com.json 
	python scripts/batch.py  cleaned/chinanews.com/ markdown/chinanews.com/ scripts/markdown/html2md.js

	python scripts/ai/process_dir.py markdown/chinanews.com/ ready/chinanews.com/ scripts/ai/prompt/clean.template

.PHONY: 163.com
163.com: raw/163.com/page.yml
	python scripts/batch.py  raw/163.com/ cleaned/163.com/ ./scripts/cleaner/clean_cheerio.js HTML_CLEANER_CONFIG=./scripts/cleaner/configs/163.com.json 
	python scripts/batch.py  cleaned/163.com/ markdown/163.com/ scripts/markdown/html2md.js

	python scripts/ai/process_dir.py markdown/163.com/ ready/163.com/ scripts/ai/prompt/clean.template  --skip-size-check

.PHONY: news.qq.com
news.qq.com: raw/news.qq.com/page.yml

	python scripts/batch.py  raw/news.qq.com/ cleaned/news.qq.com/ ./scripts/cleaner/clean_cheerio.js HTML_CLEANER_CONFIG=./scripts/cleaner/configs/news.qq.com.json 
	python scripts/batch.py  cleaned/news.qq.com/ markdown/news.qq.com/ scripts/markdown/html2md.js

	python scripts/ai/process_dir.py markdown/news.qq.com/ ready/news.qq.com/ scripts/ai/prompt/clean.template

.PHONY: unclassify_news
unclassify_news: raw/unclassify_news/page.yml
	python scripts/batch.py  raw/unclassify_news/ cleaned/unclassify_news/ ./scripts/cleaner/clean_cheerio.js HTML_CLEANER_CONFIG=./scripts/cleaner/configs/unclassify_news.json 
	python scripts/batch.py  cleaned/unclassify_news/ markdown/unclassify_news/ scripts/markdown/html2md.js

	python scripts/ai/process_dir.py markdown/unclassify_news/ ready/unclassify_news/ scripts/ai/prompt/clean.template --skip-size-check

build_page: raw/ifeng.com/page.yml raw/sina.cn/page.yml raw/thepaper.cn/page.yml raw/sohu.com/page.yml raw/chinanews.com/page.yml raw/163.com/page.yml raw/news.qq.com/page.yml raw/unclassify_news/page.yml

.PHONY: clean_page
clean_page:
	rm -rf raw/*/page.yml
