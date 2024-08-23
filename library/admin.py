from django.contrib import admin
from .models import *


class BookInline(admin.TabularInline):
    model = Book
    extra = 1


class AuthorDetailInline(admin.StackedInline):
    model = AuthorDetail
    extra = 0


def mark_authors_deleted(modeladmin, request, queryset):
    queryset.update(deleted=True)


mark_authors_deleted.short_description = "Mark selected authors as deleted"


def unmark_authors_deleted(modeladmin, request, queryset):
    queryset.update(deleted=False)


unmark_authors_deleted.short_description = "Unmark selected authors as deleted"


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birth_date', 'rating', 'deleted')
    search_fields = ('first_name', 'last_name')
    ordering = ('last_name', 'first_name')
    inlines = [AuthorDetailInline, BookInline]
    actions = [mark_authors_deleted, unmark_authors_deleted]


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publishing_date', 'genre')
    search_fields = ('title', 'author__first_name', 'author__last_name', 'genre')
    list_filter = ('genre', 'publishing_date')
    ordering = ('-publishing_date',)
    list_per_page = 10


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class EventInline(admin.TabularInline):
    model = Event
    extra = 1


class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'site')
    search_fields = ('name', 'location')
    list_filter = ('location',)
    ordering = ('name',)
    inlines = [EventInline]


class PostInline(admin.TabularInline):
    model = Post
    extra = 1


class BorrowInline(admin.TabularInline):
    model = Borrow
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


def activate_members(modeladmin, request, queryset):
    queryset.update(active=True)
activate_members.short_description = "Activate selected members"


def deactivate_members(modeladmin, request, queryset):
    queryset.update(active=False)
deactivate_members.short_description = "Deactivate selected members"

def assign_role_to_reader(modeladmin, request, queryset):
    queryset.update(role='Reader')
assign_role_to_reader.short_description = "Assign role Reader to selected members"

def assign_role_to_staff(modeladmin, request, queryset):
    queryset.update(role='Staff')
assign_role_to_staff.short_description = "Assign role Staff to selected members"


class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'role', 'active')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('role', 'active')
    ordering = ('last_name', 'first_name')
    inlines = [PostInline, BorrowInline, ReviewInline]
    actions = [activate_members, deactivate_members, assign_role_to_reader, assign_role_to_staff]


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'library')
    search_fields = ('title', 'author__first_name', 'author__last_name')
    list_filter = ('library', 'created_at')
    ordering = ('-created_at',)


def mark_borrows_returned(modeladmin, request, queryset):
    queryset.update(returned=True)
mark_borrows_returned.short_description = "Mark selected borrows as returned"


class BorrowAdmin(admin.ModelAdmin):
    list_display = ('member', 'book', 'library', 'borrow_date', 'return_date', 'returned')
    search_fields = ('member__first_name', 'member__last_name', 'book__title', 'library__name')
    list_filter = ('returned', 'borrow_date', 'return_date')
    ordering = ('-borrow_date',)
    actions = [mark_borrows_returned]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'reviewer', 'rating')
    search_fields = ('book__title', 'reviewer__first_name', 'reviewer__last_name')
    list_filter = ('rating',)
    ordering = ('-rating',)


class AuthorDetailAdmin(admin.ModelAdmin):
    list_display = ('author', 'gender', 'birth_city')
    search_fields = ('author__first_name', 'author__last_name', 'birth_city')
    ordering = ('author__last_name',)


class EventParticipantInline(admin.TabularInline):
    model = EventParticipant
    extra = 1


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'library')
    search_fields = ('title', 'library__name')
    list_filter = ('date', 'library')
    ordering = ('-date',)
    inlines = [EventParticipantInline]


class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ('event', 'member', 'registration_date')
    search_fields = ('event__title', 'member__first_name', 'member__last_name')
    list_filter = ('registration_date',)
    ordering = ('-registration_date',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Borrow, BorrowAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(AuthorDetail, AuthorDetailAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventParticipant, EventParticipantAdmin)