# 定义索引类
from haystack import indexes
# 导入你的模型类
from goods.models import GoodsSKU


# 指定我要对我的GoodsSKU这个类的数据建立索引
# 索引类名格式通常是模型类名＋Index
class GoodsSKUIndex(indexes.SearchIndex,indexes.Indexable):
    # text是索引字段,因为有document=True标志，use_template=True指定根据表中的那些字段建立索引文件，把说明放在一个文件中
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        return GoodsSKU
    # 建立数据的索引，你返回的是所有，所以我就对所有数据(这里代表商品)建立索引
    def index_queryset(self,using=None):
        return self.get_model().objects.all()