class ExampleService:
    @classmethod
    def example_method(cls) -> str:
        
        return "example_method"

if __name__=='__main__':
    # 无依赖，可以支持单文件测试功能
    print(ExampleService.example_method())
