from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from account_module.models import User


class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')
    icon = models.CharField(max_length=35, db_index=True, verbose_name='آیکون', null=True, blank=True)
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر دسته بندی')
    is_in_listCat_homepage = models.BooleanField(verbose_name='قرارگیری در صفحه اصلی قسمت لیست محصولات', null=True,
                                                 blank=True)
    image2 = models.ImageField(upload_to='images/products', null=True, blank=True,
                               verbose_name='تصویر دسته بندی در لیست دسته بندی ها')
    is_in_homepage1 = models.BooleanField(verbose_name='قرارگیری در صفحه اصلی 1', null=True, blank=True)
    is_in_homepage2 = models.BooleanField(verbose_name='قرارگیری در صفحه اصلی 2', null=True, blank=True)
    is_in_homepage3 = models.BooleanField(verbose_name='قرارگیری در صفحه اصلی 3', null=True, blank=True)

    def __str__(self):
        return f'( {self.title} - {self.url_title} )'

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ProductBrand(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام موضوع', db_index=True)
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    icon_brand = models.CharField(max_length=35, db_index=True, verbose_name='آیکون', null=True, blank=True)
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر موضوع')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_in_header = models.BooleanField(verbose_name='قرارگیری در هدر', null=True, blank=True)

    class Meta:
        verbose_name = 'طبقه بندی موضوعی'
        verbose_name_plural = 'موضوعات'

    def __str__(self):
        return self.title


class ProductColorCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    hex_color = models.CharField(max_length=15, db_index=True, verbose_name='رنگ hex', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    def __str__(self):
        return f'( {self.title} - {self.url_title} )'

    class Meta:
        verbose_name = 'رنگ محصول'
        verbose_name_plural = 'رنگ های محصول'


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام محصول')
    category = models.ManyToManyField(ProductCategory, related_name='product_categories', verbose_name='دسته بندی ها')
    color = models.ManyToManyField(ProductColorCategory, related_name='product_color_categories', verbose_name='رنگ ها',
                                   blank=True)
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول')
    image2 = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول2')
    image3 = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول3')
    image4 = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول4')
    image5 = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول5')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='برند', null=True, blank=True)
    price = models.IntegerField(null=True, blank=True, verbose_name='قیمت')
    new_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت بعد از اعمال تخفیف')
    discount = models.IntegerField(null=True, blank=True, verbose_name='تخفیف')
    is_free = models.BooleanField(default=False, verbose_name='قالب رایگان')
    short_description = models.CharField(max_length=360, db_index=True, null=True, verbose_name='توضیحات کوتاه')
    short_description2 = models.CharField(max_length=360, db_index=True, null=True, verbose_name='توضیحات کوتاه2')
    short_description3 = models.CharField(max_length=360, db_index=True, null=True, verbose_name='توضیحات کوتاه3')
    short_description4 = models.CharField(max_length=360, db_index=True, null=True, verbose_name='توضیحات کوتاه4')
    short_description5 = models.CharField(max_length=360, db_index=True, null=True, verbose_name='توضیحات کوتاه5')
    description = models.TextField(verbose_name='توضیحات اصلی', db_index=True)
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=200, unique=True,
                            verbose_name='عنوان در url')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد', null=True, blank=True)
    template_url = models.URLField(verbose_name='آدرس قالب', null=True, blank=True)
    is_special_products1 = models.BooleanField(default=False, verbose_name='قالب ویژه (پارت 1 صفحه خانه)', null=True,
                                               blank=True)
    is_special_products2 = models.BooleanField(default=False, verbose_name='قالب ویژه (پارت 2 صفحه خانه)', null=True,
                                               blank=True)
    is_in_list_special_products = models.BooleanField(default=False, verbose_name='قرارگیری در لیست محصولات ویژه',
                                                      null=True, blank=True)
    version = models.CharField(max_length=100, blank=True, null=True, verbose_name='نمایش ورژن قالب در وب سایت')
    publish_date = models.CharField(max_length=180, blank=True, null=True, verbose_name='نمایش تاریخ ایجاد در وب سایت')
    update_date = models.CharField(max_length=180, blank=True, null=True,
                                   verbose_name='نمایش تاریخ آپدیت قالب در وب سایت')
    average_rating = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    number_rating = models.IntegerField(default=1, verbose_name='تعداد امتیازدهندگان')
    total_ratings = models.PositiveIntegerField(default=0)

    # Methods for updating rating
    def update_rating(self):
        reviews = ProductReview.objects.filter(product=self)
        if reviews.exists():
            total_ratings = reviews.count()
            total_score = sum([review.rating for review in reviews])
            self.average_rating = total_score / total_ratings
            self.total_ratings = total_ratings
            self.save()

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.price})"

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # You can add validation for the rating value if needed
    review = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_rating()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.product.update_rating()


class ProductTag(models.Model):
    caption = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')

    class Meta:
        verbose_name = 'تگ محصول'
        verbose_name_plural = 'تگ های محصولات'

    def __str__(self):
        return self.caption


class ProductVisit(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=40, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='کاربر')

    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدیدهای محصول'


class Proforma(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    products = models.ManyToManyField('Product', verbose_name='محصول‌ها')
    is_paid = models.BooleanField(verbose_name='پرداخت شده', default=False)
    create_date = models.DateField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return f"Proforma {self.pk} - User: {self.user.username}"

    @property
    def total_price(self):
        return sum(product.price for product in self.products.all())

    @property
    def total_products(self):
        return self.products.count()

    class Meta:
        verbose_name = 'پیش فاکتور'
        verbose_name_plural = 'پیش فاکتورها'


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    parent = models.ForeignKey('ProductComment', null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name='کامنت والد')
    ip = models.CharField(max_length=40, null=True, blank=True, verbose_name='آی پی کاربر')
    name = models.CharField(max_length=100, verbose_name='نام کامنت‌گذار')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='کاربر')
    email = models.EmailField(null=True, blank=True, verbose_name='ایمیل کامنت‌گذار')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    text = models.TextField(verbose_name='متن کامنت')
    admin_answer = models.TextField(null=True, blank=True, verbose_name='پاسخ ادمین')
    admin_answer_create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True,
                                                    verbose_name='تاریخ ثبت پاسخ ادمین')
    is_show = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'کامنت های محصول'
        verbose_name_plural = 'کامنت ها'


class ProductSupport(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان')
    email = models.EmailField(max_length=300, verbose_name='ایمیل')
    full_name = models.CharField(max_length=300, verbose_name='نام و نام خانوادگی')
    message = models.TextField(verbose_name='متن درخواست پشتیبانی')
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    response = models.TextField(verbose_name='متن پاسخ درخواست پشتیبانی', null=True, blank=True)
    is_read_by_admin = models.BooleanField(verbose_name='خوانده شده توسط ادمین', default=False)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='کاربر')

    class Meta:
        verbose_name = 'پشتیبانی محصول'
        verbose_name_plural = 'لیست درخواست های پشتیبانی محصول'

    def __str__(self):
        return self.title
