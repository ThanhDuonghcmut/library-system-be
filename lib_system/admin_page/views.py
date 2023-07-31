from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, BookBatch, Category
from .serializers import BookBatchSerializers, BookSerializers, CategorySerializers

# Create your views here.


@api_view(['GET'])
def dashBoard(request):
    items = list(BookBatch.objects.all())
    total = sum(map(lambda x: x.quantity, items))
    total_rented = sum(map(lambda x: x.rented, items))
    total_loss = sum(map(lambda x: x.loss, items))
    result = {'total_available': total - total_rented - total_loss,
              'total_rented': total_rented, 'total_loss': total_loss, 'status_code': 0, 'message': 'Get dashboard successfully'}
    return Response(result)


@api_view(['GET', 'POST'])
def books(request):
    if request.method == 'GET':
        id = request.query_params.get('id')
        if id:
            book_items = BookSerializers(
                [get_object_or_404(Book, id=id)], many=True).data
            num_items = 1
            num_pages = 1
        else:
            perpage = request.query_params.get('limit')
            page = request.query_params.get('page')
            if not perpage:
                perpage = 10
            if not page:
                page = 1
            search_key = request.query_params.get('key')
            items = Book.objects.all()
            if search_key:
                items = items.filter(batch_id__author__icontains=search_key) | items.filter(
                    batch_id__title__icontains=search_key) | items.filter(batch_id__description__icontains=search_key)
            paginator = Paginator(items, per_page=perpage)
            num_items = len(items)
            num_pages = paginator.num_pages
            try:
                book_items = BookSerializers(
                    paginator.page(number=page), many=True).data
            except EmptyPage:
                book_items = []

        return_items = []
        for item in book_items:
            batch_detail = BookBatchSerializers(
                BookBatch.objects.get(id=item['batch_id'])).data
            item.pop('batch_id')
            pop_list = ['id', 'quantity', 'rented', 'loss']
            [batch_detail.pop(key) for key in pop_list]
            return_items.append({**item, **batch_detail})
        return Response({'data': return_items, 'total_items': num_items, 'total_pages': num_pages, 'status_code': 0, 'message': 'Get books successfully'})

    if request.method == 'POST':
        data = request.data
        book_batch = BookBatchSerializers(data=data)
        book_batch.is_valid(raise_exception=True)
        book_batch.save()
        for _ in range(data['quantity']):
            new_book = BookSerializers(
                data={'batch_id': book_batch.data['id']})
            new_book.is_valid(raise_exception=True)
            new_book.save()
        return Response({'status_code': 0, 'message': 'Add new books successfully'})


@api_view(['GET'])
def category(request):
    items = Category.objects.all()
    return Response({'data': CategorySerializers(items, many=True).data, 'status_code': 0, 'message': 'Get category successfully'})
