from django.contrib import admin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
import json
import plotly.express as px
import pandas as pd
from .models import SalesData

@admin.register(SalesData)
class SalesDataAdmin(admin.ModelAdmin):
    list_display = ('product', 'region', 'amount', 'date')
    list_filter = ('region', 'date')
    change_list_template = 'admin/sales_changelist.html'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('charts/', self.admin_site.admin_view(self.charts_view), name='sales-charts'),
            path('charts/filter-data/', self.admin_site.admin_view(self.filter_data), name='filter-data'),
        ]
        return custom_urls + urls
    
    @csrf_exempt
    def filter_data(self, request):
        try:
            filters = json.loads(request.body)
            qs = SalesData.objects.all()
            
            if filters.get('product'):
                qs = qs.filter(product__in=filters['product'])
            if filters.get('region'):
                qs = qs.filter(region__in=filters['region'])
            
            df = pd.DataFrame(list(qs.values()))
            
            return JsonResponse({
                'table_data': df.to_dict('records'),
                'graph_data': {
                    'products': df.groupby('product', as_index=False)['amount'].sum().to_dict('records'),
                    'regions': df.groupby('region', as_index=False)['quantity'].sum().to_dict('records'),
                }
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    def charts_view(self, request):
        context = {
            'products': SalesData.objects.values_list('product', flat=True).distinct(),
            'regions': SalesData.objects.values_list('region', flat=True).distinct(),
        }
        return render(request, 'admin/sales_interactive.html', context)