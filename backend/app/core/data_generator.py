class TestDataGenerator:
    def __init__(self, db_connection):
        self.db = db_connection
    
    async def generate_bulk_test_data(self, scenario):
        all_test_data = []
        
        for data_set in scenario['data_sets']:
            generated_data = await self._generate_data_set(
                template=data_set['template'],
                count=data_set['count'],
                variations=data_set.get('variations', [])
            )
            all_test_data.extend(generated_data)
            
        return all_test_data
    
    async def _generate_data_set(self, template, count, variations):
        result = []
        # 변형 케이스 먼저 처리
        for variation in variations:
            data = template.copy()
            data.update(variation)
            result.append(data)
        
        # 나머지 건수만큼 템플릿으로 생성
        remaining_count = count - len(variations)
        for _ in range(remaining_count):
            result.append(template.copy())
            
        return result 