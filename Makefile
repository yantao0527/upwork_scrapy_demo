
scrapy-shell:
	scrapy shell 'https://www.cnn.com/'

crawl:
	scrapy crawl cnn -o cnn.jsonl

clean:
	rm -f cnn.jsonl