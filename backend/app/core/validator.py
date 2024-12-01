class BatchResultValidator:
    def __init__(self, db_connection):
        self.db = db_connection
    
    async def validate_results(self, scenario, execution_results):
        validation_results = {
            'success': True,
            'details': []
        }
        
        # DB 검증
        for check in scenario['validations']['db_checks']:
            db_result = await self._validate_db_results(check)
            validation_results['details'].append(db_result)
            if not db_result['success']:
                validation_results['success'] = False
        
        # 파일 검증
        file_result = await self._validate_output_file(
            scenario['validations']['file_checks']
        )
        validation_results['details'].append(file_result)
        
        return validation_results
    
    async def _validate_db_results(self, check):
        results = {}
        for case_name, conditions in check['conditions'].items():
            query_result = await self.db.execute(
                f"""
                SELECT COUNT(*) as count 
                FROM {check['table']} 
                WHERE status = :status 
                AND error_code = :error_code
                """,
                conditions
            )
            
            results[case_name] = {
                'success': query_result['count'] == conditions['expected_count'],
                'actual_count': query_result['count'],
                'expected_count': conditions['expected_count']
            }
            
        return results 