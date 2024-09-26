from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .myscript import run_script

class RunScriptView(APIView):
    def get(self, request):
        param = request.query_params.get('param', 'default_value')
        try:
            # Call the Python script and pass the parameter
            # result = run_script(param)
            return Response({"message": param}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
