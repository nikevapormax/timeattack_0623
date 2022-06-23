from datetime import timedelta
from django.utils import timezone
from unicodedata import category
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q

from .serializers import ItemOrderSerializer, ItemSerializer

from .models import Category, Item, ItemOrder

# Create your views here.
class ItemView(APIView):
    
    def get(self, request):
        """
        1. get 요청의 param에서 카테고리값을 가져옴
        2. 해당 카테고리와 연결되어 있는 모든 아이템을 쿼리셋으로 뽑음 
           -> Item 모델에서 들고 있는 것은 카테고리의 id 값이므로 카테고리에 __로 접근해 name을 바로 사용
        3. ItemSerializer에 items를 넣어서 화면으로 값을 뿌려줌
           -> 이때 쿼리셋으로 결과가 나오니 many=True를 꼭 넣어줘야 함
        4. serialized_items를 리턴해줄 때 .data를 붙여 JSON 형식으로 보내주지 않으면 아래의 에러가 나옴
           -> TypeError: Object of type ListSerializer is not JSON serializable
        """
        category = request.GET.get('category')
        items = Item.objects.filter(category__name=category)
        serialized_items = ItemSerializer(items, many=True)

        return Response(serialized_items.data, status=status.HTTP_200_OK)
       
    def post(self, request):
        """
        1. 포스트맨에서 입력한 값을 request.data로 받아온다. 그리고 그 값을 ItemSerializer에 입력한다. 
           -> {'name': 'item3', 'category': 1, 'image_url': 'https://www.image.com/'}
        2. post의 경우 db에 요소를 생성하는 것이므로 '검증'이 필요하다. 
           -> 따라서 is_valid()를 통해 내가 넣은 데이터가 올바른지 판단해야 한다. 
           -> ItemSerializer의 fields에는 ["name", "category", "image_url"]가 들어가야 한다. 
           -> 현재 위의 값대로 포스트맨에서 데이터를 쏴주었기 때문에 검증을 통과했다. 
           -> request에서 받은 카테고리 값을 바탕으로 카테고리 오브젝트를 찾고, ItemSerializer의 필드에 해당 값을 추가해준다. 
        """
        item_serializer = ItemSerializer(data=request.data)

        if item_serializer.is_valid():
            category = Category.objects.get(id=request.data["category"])
            item_serializer.save(category=category)
            return Response(item_serializer.data, status=status.HTTP_200_OK)
            
        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ItemOrderView(APIView):
    
    def get(self, request):
        """
        url에 주의해야 함!!
        1. order_id를 받아온다. 
           -> order_id = request.GET.get("order_id") 와 같은 의미이다. 
        2. 아래의 조건에 맞는 쿼리문을 작성한다. 
           -> 조건 : 주문id가 일치하고 Order모델의 order_date 범위가 현재시간 기준으로 일주일전까지의 주문내역만 조회하도록 구현 (Q객체 사용)
        3. 찾은 orders 쿼리셋을 ItemOrderSerialzer에 넣는다. 
           -> 나는 시리얼라이저 쪽에도 아래와 같이 many=True를 넣었었다. 
              order = OrderSerializer(many=True, read_only=True)
              item = ItemSerializer(many=True, read_only=True)
           -> 이렇게 되면 에러가 나는데(TypeError: 'Order' object is not iterable), 이것의 의미는
              쿼리셋은 여러 개가 들어가는 것이 맞으나 시리얼라이저의 order와 item에는 각각 하나의 값들이 들어가기 때문에 iterable 하지 않다고 나오는 것이다. 
              각각 하나의 값을 반영하므로 아래와 같이 수정하는 것이 옳다. 
           -> order = OrderSerializer(read_only=True)
              item = ItemSerializer(read_only=True)   
        4. serialized_orders에 .data를 붙여 값을 반환한다. 
        """

        order_id = self.request.query_params.get("order_id")
        orders = ItemOrder.objects.filter(
            Q(order__id=order_id) 
          & Q(order__order_date__range=[timezone.now() - timedelta(days=7), timezone.now()]))
        
        serialized_orders = ItemOrderSerializer(orders, many=True)

        return Response(serialized_orders.data, status=status.HTTP_200_OK)