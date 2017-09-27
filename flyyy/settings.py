# -*- coding: utf-8 -*-

# Scrapy settings for flyyy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import random
uuids = ['126ff2ad3b1443b39b5a12e7645f2845', 'aa6aa3f11abf428185a88060a6f8ad58', 'e9f304ed9c864d389bfb2a3d08bb7e39', '60e773088c7845b0943998b2dd22c15d', 'df72271ebb2e4dc09e5966e2ae41ad9d', '11c7fca0114a4cc38899a9f056ec6897', '21dcf7be99634a35911cf581ce2cb54f', 'a2e99e4b6c7c4bffaac28f142e471079', 'ad12af6d7f7a41979293dee950e39987', 'de895412e00d46aea96c67443b642013', '54fae3ea190f4a6b801e7c4151899fe1', 'bf515ede4e774f70b71063a921077d4a', '7e4af6599f674a7b8e0d94a1daeddf5a', 'f8787c5085994775a31c0096584567a5', '9f9267b580dd4e5096451fb42c3695a5', 'a8a134a10fc84f6cbf8e4c03557394ef', 'c27ffc3c506a4ba3b2affe0f136dab9a', 'dee8d70b9487409b866e3095b497e78f', '10b235efb6f6456f80bf5c0b3c382e1c', 'd2a974877b534cd49f6dbd7bf00c9e3f', '5a9ab72f58024030930d36e87bd459e1', '9f0ccedb02a746a2b4981db5cc279d23', 'bed3f0fe25c040c480fcef94f3e404d0', '65806634a4cb4ec4bdcdd54e5950d24c', '89cbb4b99045434286faf13373c6bf2d', '19076cf32936441a8d241ca72bb15ac9', '853b0e579c5f4bbf828e345e46547343', 'cc85e3c72b524a799049a457e46cf2be', '326c3bbec98d43ba9a0a431a9e015256', 'd05ced4eb9264f868937fcb59c0281cf', '4c57331fe41c4fe884d64758953d3c66', '3672d7e6ae5a4e69bfd05f27604133a4', '32f22267ebdb466d94879e8efa5309cb', 'bcd820291338491eae5eadb244a86353', '56a78222b44b4c3e82f87ecfc2e89ac0', 'a4c4150a8c1d4ee5bd2e5cccf4700683', '531d946f8f82410396439deb14d170e1', '6ae1f2ac0e0848879f85d332c0d6c605', '4e98fcdbb47d4576b786aadbdbcbe5b0', '9cf0e24bc46944938736064dd6042fc5', 'd1f1818c78a3477bad7f4bad116f57ac', '14bd9b4f593c4c91a2da143e7445128a', '72baa82d1c77484395cec9ab8ad0b9a3', '2da3555125bf45019746988838e0823f', '878882893a504238ba96a75720efde9e', 'd8952667ed5343229d89832d1554d6d5', '2b692c882b574c23b5b0b82eb7c634de', 'd379b0b14a5349c79dc50950894d55d4', 'a17545af95574eacae60d6e554207cad', '60caa59014654f7fbbed1a982403c1d4', '96032f2cfe674119849ae9f8be538ddf', '9cc02ddd35234beaa6e122f9eb5dfe48', 'ffafcd2daa5c4e53856371639610ea5f', 'd536afd7e0e34c6bbe4f2d95f60218ac', '8dfb6561013c4b0d89dc0c00276b3276', '5d931d01c70844b2bd8474b452a5d678', '5de099308c4b421f87f13a39e61e32bb', '42a5e2ff5c8c49bf9cc2de92632f6737', 'b12a8957f36846c896f11af1eb238193', '885f7103df954ef282a9459f35854d5e', '89bac3b026964f8987af42a7f60d1f63', '6440a09f09ec4e129ad6073d99359b1c', '6ec3de472db04ae1b9f7bd8c03c5988c', '0ff12c963e4b4c0ea577cde007eaba90', '92903f733dd84d489cfe0e9ef6fe5704', 'eb830f839be54338a9e89515f9c51a8c', '7bb8b31b6cb04cacb651f8a726d051c4', 'd12c2cf7a28f43cf9e45a93f499d979e', '8611d971bd0d40b0b859ab470d2dd859', '35f5a9fa904c48d5aa2c4de1e5ba649c', '58637f36054d4981b95bd272801eeb9b', 'd51ad22ab1d5463db9cf689362222117', '44d14879e40948fb8a38e10d29c93998', '3310616d54894930a13e9f6dded2274e', '87fef1943c3b46b9a76b767acd1998bc', 'fca95689d74a4834a758746277a2d644', 'ea8a4719705b454b886bae1db4c36b97', '13458a28b1eb43f8b41ae0c504df5241', 'f5c7e63224a04709899f373455cbc173', '8f7ebad88641452ca1c7aeed83d341c1', 'd43ecbcbff904c52af092f605b3bce72', 'aa50140d98084a098d3a17e16aecc43b', 'f24c096c864e43b8a49d2fc293d6ae25', '1cfaf5b53da94b47afbeefa8c3de7aa5', '15f4a8339160487db43b60f5216080b0', '1e89d7caa090447bbbce431ed20f0510', 'a883af14e7894eaca4cfca47f97ba8e3', '2b2b6ca3db7c49e197d30b9ca41d5573', 'a783978764d24efca5d109c611a6c909', '16fac305832245028dfc198ab04d9d5d', 'c83dc99a6b0c4ec180e5ca0450bc69ba', 'f56b453a15d44b5d9a4c8926896d1975', '850cff90521d440392d3579177e7e0c8', '9215a5a8cc7940fd82eecf2554c96243', '0aed0eb5b0cc401fa90c52646de28164', '8c9f574bebc24c65a4a5e08ad2cacbac', '8a2e6cf474c94ccebab60920aa003c98', 'f444d794c1554d33a890597a21dbaf3f', 'bf104e6e14674575a6f7055d5b5428fb', 'a83b06acea974686817d23769ea28e5e']

# Default Settings
BOT_NAME = 'flyyy'
SPIDER_MODULES = ['flyyy.spiders']
NEWSPIDER_MODULE = 'flyyy.spiders'

# Custom Settings
#DOWNLOAD_HANDLERS = {'s3': None,}
#ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 300}
#IMAGES_STORE = './images/'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'flyyy (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
    'User-agent': uuids[random.randint(0,99)],
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'flyyy.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'flyyy.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'flyyy.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
