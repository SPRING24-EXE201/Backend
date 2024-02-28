import os

from django.http import FileResponse, HttpResponse


def get_json_file(request):
    # Đường dẫn tới tệp JSON
    json_file_path = os.path.join(os.path.dirname(__file__), 'assetlinks.json')

    # Kiểm tra xem tệp có tồn tại hay không
    if os.path.exists(json_file_path):
        # Mở tệp và trả về dưới dạng FileResponse
        return FileResponse(open(json_file_path, 'rb'), content_type='application/json')
    else:
        # Trả về một HttpResponse lỗi nếu tệp không tồn tại
        return HttpResponse("File not found", status=404)