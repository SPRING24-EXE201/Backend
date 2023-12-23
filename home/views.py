from rest_framework.response import Response
from rest_framework.decorators import api_view
from home.models import AdministrativeRegion
from home.serializers import AdministrativeRegionSerializer

@api_view(['GET'])
def getData(request):
    items = AdministrativeRegion.objects.all()
    print(items)
    serializer = AdministrativeRegionSerializer(items, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def createData(request):
    # If primary key attribute is set to a value and such primary key already exists, then Model.save() performs UPDATE, 
    # but Model.objects.create() raises IntegrityError.
    AdministrativeRegion.objects.create(id = request.data.get('id'),
                                            code_name = request.data.get('code_name'),
                                            name = request.data.get('name'),
                                            name_en = request.data.get('name_en'),
                                            code_name_en = request.data.get('code_name_en'))


    return Response()

@api_view(['PUT'])
def updateData(request):
    item = AdministrativeRegion.objects.get(id = request.data.get('id'))
    if item != False:
        item.code_name = request.data.get('code_name')
    item.save()

    serializer = AdministrativeRegionSerializer(item, many = True)

    return Response(serializer.data)


@api_view(['DELETE']) 
def deleteData(request):
    try:
        item = AdministrativeRegion.objects.delete(id = request.data.get('id'))
        serializer = AdministrativeRegionSerializer(item, many = True)
        return Response(serializer.data)
        
    except:
        return Response("Co loi xay ra")
