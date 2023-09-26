from django.db import models
from django.urls import reverse
from account_module.models import User


# Create your models here.

class ArticleCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان دسته بندی')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر دسته بندی')


    def __str__(self):
        return f'( {self.title} - {self.url_title} )'

    class Meta:
        verbose_name = 'دسته بندی مقالات'
        verbose_name_plural = 'دسته بندی های مقالات'


class Article(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان مقاله')
    category = models.ManyToManyField(ArticleCategory, related_name='article_categories', verbose_name='دسته بندی ها')
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='نویسنده مقاله')
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول')
    short_description = models.CharField(max_length=360, db_index=True, null=True, verbose_name='توضیحات کوتاه')
    description = models. TextField(verbose_name='متن اصلی مقاله', db_index=True)
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=200, unique=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد', null=True, blank=True)
    is_in_homepage = models.BooleanField(default=False, verbose_name='قالب ویژه (پارت 1 صفحه خانه)', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('article-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'


class ArticleTag(models.Model):
    caption = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    product = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_tags')

    class Meta:
        verbose_name = 'تگ مقاله'
        verbose_name_plural = 'تگ های مقالات'

    def __str__(self):
        return self.caption


class ArticleComment(models.Model):
    product = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='مقاله')
    parent = models.ForeignKey('ArticleComment', null=True, blank=True, on_delete=models.CASCADE, verbose_name='کامنت والد' )
    ip = models.CharField(max_length=40, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='کاربر')
    email = models.EmailField(null=True, blank=True, verbose_name='ایمیل')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    text = models.TextField(verbose_name='متن کامنت')
    admin_answer = models.TextField(null=True, blank=True, verbose_name='پاسخ ادمین')
    is_show = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'کامنت های مقاله'
        verbose_name_plural = 'کامنت های مقالات'