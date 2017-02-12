# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import time

from weibo_message import WeiboMessage
from config import add_watermark, watermark_url, watermark_nike
from config import max_images
from logger import logger

if max_images < 0 or max_images > 9:
    max_images = 9

class WeiboSender(object):
    def __init__(self, session, uid):
        super(WeiboSender, self).__init__()
        self.session = session
        self.uid = str(uid)
        self.Referer = u"http://www.weibo.com/u/%s/home?wvr=5" % str(self.uid)
        
    def send_weibo(self, weibo):
        if not isinstance(weibo, WeiboMessage):
            raise ValueError(u'weibo must WeiboMessage class type' )
            logger.debug( u'weibo must WeiboMessage class type' )
        if weibo.is_empty:
            return

        pids = ''
        if weibo.has_image:
            pids = self.upload_images(images)
        data = weibo.get_send_data(pids)
        self.session.headers[u"Referer"] = self.Referer

        try:
            resp = self.session.post(
                u"http://www.weibo.com/aj/mblog/add?ajwvr=6&__rnd=%d" % int( time.time() * 1000),
                data=data
            )
            logger.info(u'微博[%s]发送成功' % str(weibo))
        except Exception as e:
            logger.debug(e)
            logger.info( u'微博[%s]发送失败' % str(weibo) )
        
        
    def upload_images(self, images):
        pids = ""
        if len(images) > max_images:
            images = images[0: max_images]
        for image in images:
            pid = self.upload_image_stream(image)
            if pid:
                pids += " " + pid
            time.sleep(10)
        return pids.strip()


    def upload_image_stream(self, image_url):
        if add_watermark:
            url = u"http://picupload.service.weibo.com/interface/pic_upload.php?app=miniblog&data=1&url=" \
                + watermark_url + u"&markpos=1&logo=1&nick="\
                + watermark_nike + \
                u"&marks=1&mime=image/jpeg&ct=0.5079312645830214"

        else:
            url = u"http://picupload.service.weibo.com/interface/pic_upload.php?rotate=0&app=miniblog&s=json&mime=image/jpeg&data=1&wm="

        #self.http.headers["Content-Type"] = "application/octet-stream"
        image_name = image_url
        try:
            f = self.session.get( image_name, timeout=30 )
            img = f.content
            resp = self.session.post( url, data=img )
            upload_json = re.search( '{.*}}', resp.text ).group(0)
            result = json.loads( upload_json )
            code = result[u"code"]
            if code == u"A00006":
                pid = result[u"data"][u"pics"][u"pic_1"][u"pid"]
                return pid
        except Exception as e:
            logger.info(u"图片上传失败：%s" % image_name)
        return None
