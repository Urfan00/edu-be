from django.contrib import admin
from .models import Purpose, SourceOfInformation, University, Filial, Region, Program, Register
from import_export.admin import ImportExportModelAdmin


@admin.register(Purpose)
class PurposeAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(SourceOfInformation)
class SourceOfInformationAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(University)
class UniversityAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Filial)
class FilialAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Region)
class RegionAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Program)
class ProgramAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Register)
class RegisterAdmin(ImportExportModelAdmin):
    list_display = ('id', 'first_name' , 'last_name' , 'father_name' , 'email' , 'passport_id' , 'phone_number_1' , 'phone_number_2' , 'gender' , 'lesson_type' , 'status' , 'purpose' , 'source_of_information' , 'university' , 'filial' , 'region' , 'program', 'created_at', 'updated_at')
    search_fields = ('first_name', 'last_name', 'email', 'passport_id')
    list_filter = ('gender' , 'lesson_type' , 'status' , 'purpose' , 'source_of_information' , 'university' , 'filial' , 'region' , 'program', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
