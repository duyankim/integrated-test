# 테스트 시나리오 설정
scenario = TestScenario()
test_result = BatchTestResult()

# 시나리오 생성
scenario.save_scenario(
    name="주문_금액_검증",
    batch_id="batch_002",
    configuration={"min_amount": 10000}
)

# 검증 규칙 추가
scenario.add_validation_rule(
    "주문_금액_검증",
    {
        "type": "greater_than",
        "expected": 10000,
        "message": "주문 금액은 10000원 이상이어야 합니다"
    }
)

# 테스트 실행 및 결과 저장
actual_result = 15000  # 실제 테스트 실행 결과
is_valid, validation_results = scenario.validate_scenario("주문_금액_검증", actual_result)

test_result.save_result(
    batch_id="batch_002",
    scenario_name="주문_금액_검증",
    status="SUCCESS" if is_valid else "FAILED",
    details={
        "actual_result": actual_result,
        "validation_results": validation_results
    }
) 