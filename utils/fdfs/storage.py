from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import  settings

class FDFSStorage(Storage):
    '''自定义文件存储类（fastdfs）'''
    def __init__(self,client_conf=None, base_url=None):
        '''你传了参数就使用你自己的，没有传就用我默认的，增加上传文件的灵活性'''
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL
        self.base_url = base_url

    def _open(self,name,mode='rb'):
        '''打开文件，但是我们项目不用这个方法'''
        pass

    def _save(self,name,content):
        '''上传文件，这才是关键'''
        # name是你上传文件名
        # content就是包含你上传内容的file对象

        # 创建一个Fdfs_client对象
        client = Fdfs_client(self.client_conf)
        # 上传文件到fastdfs系统中
        res = client.upload_by_buffer(content.read())

        # dict
        # {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id,
        #     'Status': 'Upload successed.',
        #     'Local file name': local_file_name,
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # }

        # if res.get('Status') != 'Upload successed':
        #     # 上传失败
        #     raise Exception('上传文件到 fastdfs 失败')

        # 获取返回的文ID
        filename = res.get('Remote file_id')
        return filename

    # exists函数也是必须实现的，django会在调用save之前判断文件名是否可用
    def exists(self,name):
        '''django判断文件名是否可用'''
        return False

    def url(self,name):
        '''根据id返回name，要不然你加进去的文件点进去现实的是id号'''
        return self.base_url + name
