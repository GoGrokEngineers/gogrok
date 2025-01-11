import time
from django.utils.deprecation import MiddlewareMixin

class PerformanceMetricsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        duration = time.time() - getattr(request, 'start_time', time.time())
        self.log_latency_to_file(request.path, duration)
        print(f"Request to {request.path} took {duration:.2f}s")
        return response

    def log_latency_to_file(self, path, duration):
        
        log_file = "/logs/latency_metrics.txt"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(log_file, "a") as file:
                file.write(f"{timestamp} - {path} - {duration:.2f}s\n")
        except Exception as e:
            print(f"Error writing to file: {e}")