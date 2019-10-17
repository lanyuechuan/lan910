from django.shortcuts import render
<<<<<<< HEAD

# Create your views here.
=======
from django.views.generic import View

from django.http import JsonResponse
from goods.models import GoodsSKU
from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin
# Create your views here.

# 该类视图完成添加商品到购物车
# １）确定前端请求方式，你get,post或者说参数名都不知道，你后端咋接收？哦,你前段是采用ajax　post方式，并且参数叫sku_id,那我就用post sku_id接收
# 如果涉及到数据的修改（增删改），采用post
# 如果只涉及到数据的获取，则使用get
# ２）传递参数：商品id(sku_id) 商品数量(count)

# /cart/add
class CartAddView(View):
    """购物车记录添加"""
    def post(self, request):
        """购物车记录添加"""
        user = request.user
        # ajax发起的请求都在后台,在浏览器是看不到效果的，这就是为什么我们不直接继承mixin抱起来判断用户是否登录,就算你继承了,没登录确实会跳转到登录界面，但是这个跳转只会在后台进行,浏览器中看不到效果
        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({'res':0, 'errmsg':'请先登录'})

        # 1\接收数据
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        # 2\数据校验
        if not all([sku_id, count]):
            return JsonResponse({'res':1, 'errmsg': '数据不完整'})

        # 检验添加的商品数量
        try:
            count = int(count)
        except Exception as e:
            # 数目出错
            return JsonResponse({'res': 2, 'errmsg': '商品数目出错'})

        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在
            return JsonResponse({'res':3, 'errmsg': '商品不存在'})

        # 3\业务处理 添加购物车记录
        conn = get_redis_connection('default') # 先使用默认setting链接redis数据库
        cart_key = 'cart_%d' % user.id
        # 先尝试获取sku_id的值 -> hget cart_key 属性
        # 如果sku_id在hash中不存在，hget返回None
        cart_count = conn.hget(cart_key, sku_id)
        if cart_count:
            # 累加购物车中商品的数目
            count += int(cart_count)

        # 校验商品的库存
        if count > sku.stock:
            return JsonResponse({'res':4, 'errmsg':'商品库存不足'})
        # 设置hash中sku_id对应的值
        # hset -> 如果sku_id已经存在，更新数据，如果sku_id不存在，添加数据
        conn.hset(cart_key, sku_id, count)

        # 计算用户购物车中商品的条目数
        # total_count = conn.hlen(cart_key)
        total_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count += int(val)

        # 返回应答
        return JsonResponse({'res':5, 'total_count': total_count, 'message':'添加成功'})


# /cart/
class CartInfoView(LoginRequiredMixin, View):
    """购物车页面显示"""
    def get(self, request):
        """显示"""
        user = request.user
        # 获取用户购物车中商品的信息
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        # {'商品id':商品数量}
        cart_dict = conn.hgetall(cart_key)

        skus = []
        # 用来保存用户购物从中商品的总数和总价
        total_count = 0
        total_price = 0
        # 遍历获取商品的信息
        for sku_id, count in cart_dict.items():
            # 根据商品的id获取商品的信息
            sku = GoodsSKU.objects.get(id=sku_id)
            # 计算商品的小计
            amount = sku.price * int(count)
            # 动态给sku对象增加一个属性amount，保存商品的小计
            sku.amount = amount
            # 动态给sku对象增加一个属性count，保存购物车中对应商品的数量,就像goods视图一样
            sku.count = count
            # 添加
            skus.append(sku)

            # 累加计算商品的总数和总价，不是条目数
            total_count += int(count)
            total_price += amount

        # 组织上下文
        context = {'total_count': total_count,
                   'total_price': total_price,
                   'skus': skus}

        return render(request, 'cart.html', context)


# 更新购物车记录
# 采用ajax post
# 前端需要传递的参数：商品id(sku_id) 更新的商品数量(count)
# /cart/update
class CartUpdateView(View):
    """购物从记录更新"""
    def post(self, request):
        """更新"""
        user = request.user
        # 前端用ajax请求，后端判断是否登录不能用loginrequire,ajax请求在后端，记住咯
        if not user.is_authenticated():
            # 用户为登录
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})

        # １\接收数据
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        # 2\数据校验
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        # 检验添加的商品数量
        try:
            count = int(count)
        except Exception as e:
            # 数目出错
            return JsonResponse({'res': 2, 'errmsg': '商品数目出错'})

        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在
            return JsonResponse({'res': 3, 'errmsg': '商品不存在'})

        # 3\业务处理：更新购物车记录
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id

        # 校验商品的库存
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})

        # 更新
        conn.hset(cart_key, sku_id, count)

        # 4\返回应答
        return JsonResponse({'res': 5, 'message': '更新成功'})


# 删除购物车记录
# 采用ajax post
# 前端需要传递的参数:商品的id(sku_id)
# /cart/delete
class CartDeleteView(View):
    """购物车记录删除"""
    def post(self, request):
        """删除"""
        user = request.user
        if not user.is_authenticated():
            # 用户为登录
            return JsonResponse({'res': 0, 'errmsg': '请先登录'})

        # 接收数据
        sku_id = request.POST.get('sku_id')

        # 数据的校验
        if not sku_id:
            return JsonResponse({'res': 1, 'errmsg': '无效的商品id'})

        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在
            return JsonResponse({'res': 2, 'errmsg': '商品不存在'})

        # 业务处理：删除购物车记录
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id

        # 删除 hdel
        conn.hdel(cart_key, sku_id)

        # 计算用户购物车中商品的条目数
        # total_count = conn.hlen(cart_key)
        total_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count += int(val)

        # 返回应答
        return JsonResponse({'res': 3, 'total_count': total_count, 'message': '删除成功'})
>>>>>>> second_dailyfresh
