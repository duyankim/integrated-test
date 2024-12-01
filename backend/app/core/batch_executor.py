class BatchExecutor:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    async def execute_batch(self, batch_id):
        try:
            # 의존성 체크
            self.logger.info(f"배치 {batch_id}의 의존성 체크를 시작합니다.")
            if not await self._check_dependencies(batch_id):
                self.logger.error(f"배치 {batch_id}의 의존성 체크에 실패했습니다.")
                raise BatchDependencyError()
                
            # 배치 실행
            self.logger.info(f"배치 {batch_id} 실행을 시작합니다.")
            try:
                response = await self._call_batch_api(batch_id)
                self.logger.info(f"배치 {batch_id} 실행이 완료되었습니다.")
            except Exception as e:
                self.logger.error(f"배치 {batch_id} 실행 중 오류가 발생했습니다: {str(e)}")
                raise
            
            # 결과 저장
            self.logger.info(f"배치 {batch_id}의 실행 결과를 저장합니다.")
            await self._save_execution_result(batch_id, response)
            
            return response
            
        except Exception as e:
            self.logger.error(f"배치 {batch_id} 처리 중 오류가 발생했습니다: {str(e)}")
            raise BatchExecutionError(str(e))