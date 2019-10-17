# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20191017_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='comment',
            field=models.CharField(verbose_name='评论', max_length=256, default=''),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='order_id',
            field=models.CharField(verbose_name='订单id', primary_key=True, max_length=128, serialize=False),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='total_price',
            field=models.DecimalField(verbose_name='商品总价', max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='trade_no',
            field=models.CharField(verbose_name='支付编号', max_length=128, default=''),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='transit_price',
            field=models.DecimalField(verbose_name='订单运费', max_digits=10, decimal_places=2),
        ),
    ]
