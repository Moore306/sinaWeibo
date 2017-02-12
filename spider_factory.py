from cnbeta import CnbetaParser
from cnblog import CnblogParser
from miaopai import MiaopaParser
from myBlog import MyBlogParser
from techweb import TechwebParser
from tuicool import TuicoolParser

spiders = [ 
          MyBlogParser(),
          CnbetaParser(),
          CnblogParser(),
          MiaopaParser(),
          MyBlogParser(),
          TechwebParser(),
          TuicoolParser() 
        ]

currentIndex = 0
count = len(spiders)

def nextSpider():
      global currentIndex
      spider = spiders[currentIndex]
      currentIndex = (currentIndex + 1) % count
      return spider
