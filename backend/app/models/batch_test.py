# 이 파일은 배치 테스트 시나리오와 실행 결과를 MongoDB에 저장하기 위한 모델을 정의합니다.
# MongoDB는 애플리케이션과 함께 실행되며 내장 MongoDB를 사용합니다.
# (예: mongita - 파이썬 전용 내장형 MongoDB 호환 데이터베이스)
# 이를 통해 별도의 MongoDB 설치나 도커 의존성 없이 독립적으로 실행 가능합니다.

from import MongitaClientDisk
from datetime import datetime

# 로컬 파일 시스템에 데이터를 저장하는 클라이언트 생성
client = MongitaClientDisk()
db = client.batch_test_db

class BatchTestResult:
    """
    배치 테스트 실행 결과를 저장하는 컬렉션입니다.
    실행 결과의 상세 정보와 로그를 내장 DB에 저장합니다.
    """
    def __init__(self):
        self.collection = db.batch_test_results
    
    def save_result(self, batch_id, scenario_name, status, error_message=None, details=None):
        document = {
            "batch_id": batch_id,
            "scenario_name": scenario_name,
            "execution_date": datetime.now(),
            "status": status,
            "error_message": error_message,
            "execution_details": details or {},
            "logs": []
        }
        return self.collection.insert_one(document)

    def find_by_batch_id(self, batch_id):
        return self.collection.find({"batch_id": batch_id})

class TestScenario:
    """
    테스트 시나리오 정보를 저장하는 컬렉션입니다.
    시나리오 설정과 의존성 정보를 내장 DB에서 관리합니다.
    """
    def __init__(self):
        self.collection = db.test_scenarios
    
    def save_scenario(self, name, batch_id, dependencies=None, configuration=None):
        document = {
            "name": name,
            "batch_id": batch_id,
            "dependencies": dependencies or {},
            "configuration": configuration or {},
            "validation_rules": []
        }
        return self.collection.insert_one(document)

    def find_by_name(self, name):
        return self.collection.find_one({"name": name})

    def add_validation_rule(self, scenario_name, rule):
        """검증 규칙 추가"""
        return self.collection.update_one(
            {"name": scenario_name},
            {"$push": {"validation_rules": rule}}
        )

    def validate_scenario(self, scenario_name, actual_result):
        """시나리오 실행 결과 검증"""
        scenario = self.find_by_name(scenario_name)
        if not scenario:
            return False, "시나리오를 찾을 수 없습니다"

        validation_results = []
        for rule in scenario.get('validation_rules', []):
            is_valid = self._apply_validation_rule(rule, actual_result)
            validation_results.append(is_valid)

        return all(validation_results), validation_results
    
    def _apply_validation_rule(self, rule, actual_result):
        """개별 검증 규칙 적용"""
        rule_type = rule.get('type')
        expected = rule.get('expected')
        
        if rule_type == 'equals':
            return actual_result == expected
        elif rule_type == 'contains':
            return expected in actual_result
        elif rule_type == 'greater_than':
            return actual_result > expected
        # 필요한 검증 규칙 추가
        return False