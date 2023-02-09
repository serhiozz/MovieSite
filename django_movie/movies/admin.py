from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews

from ckeditor_uploader.widgets import CKEditorUploadingWidget

class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)

# class ReviewInLine(admin.StackedInline):
#     model = Reviews
#     extra = 1 # Количество пустых полей снизу (для добавления нового комента в данном случае)

class ReviewInLine(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')

class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1

    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="85"')

    get_image.short_description = 'Изображение'

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    inlines = [MovieShotsInline, ReviewInLine]
    save_on_top = True # Кнопки сохранения сверху
    save_as = True # Добавление новой записи на основе текущей
    list_editable = ('draft',) # Чтобы установить как черновик прямо из списка фильмов
    actions = ['publish', 'unpublish']

    form = MovieAdminForm

    readonly_fields = ('get_image', )

    # Группируем поля
    fieldsets = (
        (None,{
            "fields": (('title', 'tagline'),)
        }),
        (None, {
            "fields": ('category',)
        }),
        (None, {
            "fields": ('description', ('poster', 'get_image'))
        }),
        (None, {
            "fields": ('year', 'world_premiere')
        }),
        ("Actors", {
            "classes": ("collapse",), # Показываем группу свернутой
            "fields": (('actors', 'directors', 'genres'),)
        }),
        (None, {
            "fields": (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        ("Options", {
            "fields": (('url', 'draft'),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.poster.url}" width="85"')

    def unpublish(self, request, queryset):
        '''Снять с публикаци'''
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f'{row_update} записей обновлено'

        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        '''Снять с публикаци'''
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f'{row_update} записей обновлено'

        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change',)

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = 'Постер'


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)

    # вывод изображения актера в админке
    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50"')

    get_image.short_description = 'Изображение'

@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image',)

    # вывод изображения в админке
    def get_image(self, obj):
        return mark_safe(f'<a href="{obj.image.url}" target="_blank"><img src="{obj.image.url}" width="85"</a>')

    get_image.short_description = 'Изображение'


# Register your models here.
#admin.site.register(Category, CategoryAdmin) или регистрируем как выше с помощью декоратора
admin.site.register(Genre)
admin.site.register(Rating)
admin.site.register(RatingStar)


admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'