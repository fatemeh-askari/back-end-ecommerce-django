# Generated by Django 4.2.4 on 2023-08-25 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account_module', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='نام محصول')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/products', verbose_name='تصویر محصول')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='images/products', verbose_name='تصویر محصول2')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='images/products', verbose_name='تصویر محصول3')),
                ('image4', models.ImageField(blank=True, null=True, upload_to='images/products', verbose_name='تصویر محصول4')),
                ('image5', models.ImageField(blank=True, null=True, upload_to='images/products', verbose_name='تصویر محصول5')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='قیمت')),
                ('new_price', models.IntegerField(blank=True, null=True, verbose_name='قیمت بعد از اعمال تخفیف')),
                ('discount', models.IntegerField(blank=True, null=True, verbose_name='تخفیف')),
                ('is_free', models.BooleanField(default=False, verbose_name='قالب رایگان')),
                ('short_description', models.CharField(db_index=True, max_length=360, null=True, verbose_name='توضیحات کوتاه')),
                ('short_description2', models.CharField(db_index=True, max_length=360, null=True, verbose_name='توضیحات کوتاه2')),
                ('short_description3', models.CharField(db_index=True, max_length=360, null=True, verbose_name='توضیحات کوتاه3')),
                ('short_description4', models.CharField(db_index=True, max_length=360, null=True, verbose_name='توضیحات کوتاه4')),
                ('short_description5', models.CharField(db_index=True, max_length=360, null=True, verbose_name='توضیحات کوتاه5')),
                ('description', models.TextField(db_index=True, verbose_name='توضیحات اصلی')),
                ('slug', models.SlugField(blank=True, default='', max_length=200, unique=True, verbose_name='عنوان در url')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال / غیرفعال')),
                ('is_delete', models.BooleanField(verbose_name='حذف شده / نشده')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد')),
                ('template_url', models.URLField(blank=True, null=True, verbose_name='آدرس قالب')),
                ('is_special_products1', models.BooleanField(blank=True, default=False, null=True, verbose_name='قالب ویژه (پارت 1 صفحه خانه)')),
                ('is_special_products2', models.BooleanField(blank=True, default=False, null=True, verbose_name='قالب ویژه (پارت 2 صفحه خانه)')),
                ('is_in_list_special_products', models.BooleanField(blank=True, default=False, null=True, verbose_name='قرارگیری در لیست محصولات ویژه')),
                ('version', models.CharField(blank=True, max_length=100, null=True, verbose_name='نمایش ورژن قالب در وب سایت')),
                ('publish_date', models.CharField(blank=True, max_length=180, null=True, verbose_name='نمایش تاریخ ایجاد در وب سایت')),
                ('update_date', models.CharField(blank=True, max_length=180, null=True, verbose_name='نمایش تاریخ آپدیت قالب در وب سایت')),
                ('average_rating', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('total_ratings', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=300, verbose_name='نام موضوع')),
                ('url_title', models.CharField(db_index=True, max_length=300, verbose_name='عنوان در url')),
                ('icon_brand', models.CharField(blank=True, db_index=True, max_length=35, null=True, verbose_name='آیکون')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/products', verbose_name='تصویر موضوع')),
                ('is_active', models.BooleanField(verbose_name='فعال / غیرفعال')),
                ('is_in_header', models.BooleanField(blank=True, null=True, verbose_name='قرارگیری در هدر')),
            ],
            options={
                'verbose_name': 'طبقه بندی موضوعی',
                'verbose_name_plural': 'موضوعات',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=300, verbose_name='عنوان')),
                ('url_title', models.CharField(db_index=True, max_length=300, verbose_name='عنوان در url')),
                ('is_active', models.BooleanField(verbose_name='فعال / غیرفعال')),
                ('is_delete', models.BooleanField(verbose_name='حذف شده / نشده')),
                ('icon', models.CharField(blank=True, db_index=True, max_length=35, null=True, verbose_name='آیکون')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/products', verbose_name='تصویر دسته بندی')),
                ('is_in_listCat_homepage', models.BooleanField(blank=True, null=True, verbose_name='قرارگیری در صفحه اصلی قسمت لیست محصولات')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='images/products', verbose_name='تصویر دسته بندی در لیست دسته بندی ها')),
                ('is_in_homepage1', models.BooleanField(blank=True, null=True, verbose_name='قرارگیری در صفحه اصلی 1')),
                ('is_in_homepage2', models.BooleanField(blank=True, null=True, verbose_name='قرارگیری در صفحه اصلی 2')),
                ('is_in_homepage3', models.BooleanField(blank=True, null=True, verbose_name='قرارگیری در صفحه اصلی 3')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='ProductColorCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=300, verbose_name='عنوان')),
                ('url_title', models.CharField(db_index=True, max_length=300, verbose_name='عنوان در url')),
                ('hex_color', models.CharField(blank=True, db_index=True, max_length=15, null=True, verbose_name='رنگ hex')),
                ('is_active', models.BooleanField(verbose_name='فعال / غیرفعال')),
                ('is_delete', models.BooleanField(verbose_name='حذف شده / نشده')),
            ],
            options={
                'verbose_name': 'رنگ محصول',
                'verbose_name_plural': 'رنگ های محصول',
            },
        ),
        migrations.CreateModel(
            name='Proforma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False, verbose_name='پرداخت شده')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('products', models.ManyToManyField(to='product_module.product', verbose_name='محصول\u200cها')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account_module.user', verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پیش فاکتور',
                'verbose_name_plural': 'پیش فاکتورها',
            },
        ),
        migrations.CreateModel(
            name='ProductVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=40, verbose_name='آی پی کاربر')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_module.product', verbose_name='محصول')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account_module.user', verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'بازدید محصول',
                'verbose_name_plural': 'بازدیدهای محصول',
            },
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(db_index=True, max_length=300, verbose_name='عنوان')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_tags', to='product_module.product')),
            ],
            options={
                'verbose_name': 'تگ محصول',
                'verbose_name_plural': 'تگ های محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductSupport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='عنوان')),
                ('email', models.EmailField(max_length=300, verbose_name='ایمیل')),
                ('full_name', models.CharField(max_length=300, verbose_name='نام و نام خانوادگی')),
                ('message', models.TextField(verbose_name='متن درخواست پشتیبانی')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('response', models.TextField(blank=True, null=True, verbose_name='متن پاسخ درخواست پشتیبانی')),
                ('is_read_by_admin', models.BooleanField(default=False, verbose_name='خوانده شده توسط ادمین')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account_module.user', verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پشتیبانی محصول',
                'verbose_name_plural': 'لیست درخواست های پشتیبانی محصول',
            },
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField()),
                ('review', models.TextField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_module.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account_module.user')),
            ],
        ),
        migrations.CreateModel(
            name='ProductComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام کامنت\u200cگذار')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل کامنت\u200cگذار')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('text', models.TextField(verbose_name='متن کامنت')),
                ('admin_answer', models.TextField(blank=True, null=True, verbose_name='پاسخ ادمین')),
                ('admin_answer_create_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ثبت پاسخ ادمین')),
                ('is_show', models.BooleanField(default=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product_module.productcomment', verbose_name='کامنت والد')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_module.product', verbose_name='محصول')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account_module.user', verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'کامنت های محصول',
                'verbose_name_plural': 'کامنت ها',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product_module.productbrand', verbose_name='برند'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='product_categories', to='product_module.productcategory', verbose_name='دسته بندی ها'),
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.ManyToManyField(blank=True, null=True, related_name='product_color_categories', to='product_module.productcolorcategory', verbose_name='رنگ ها'),
        ),
    ]