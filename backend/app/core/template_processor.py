import random
import string
from typing import Dict, Any

class TemplateProcessor:
    def __init__(self, db_connection):
        self.saved_values = {}
        self.db = db_connection
    
    def process_template(self, template: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        result = {}
        for key, value in template.items():
            if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                result[key] = self._process_template_string(value, context)
            else:
                result[key] = value
        return result
    
    def _process_template_string(self, template: str, context: Dict[str, Any]) -> Any:
        template = template.strip("{{}}")
        if template.startswith("random_account"):
            return self._generate_random_account(10)
        elif template.startswith("random_range"):
            params = self._parse_function_params(template)
            return self._generate_random_amount(*params)
        elif template.startswith("random_invalid_account"):
            return self._generate_invalid_account()
        elif "save_as" in template:
            return self._save_value(template, context)
        return template
    
    async def _generate_random_account(self, length: int) -> str:
        account_no = ''.join(random.choices(string.digits, k=length))
        account_name = ''.join(random.choices("가나다라마바사아자차카타파하", k=3))
        
        # COM_ACCT_NO_M 테이블에 테스트 데이터 생성
        await self.db.execute("""
            INSERT INTO COM_ACCT_NO_M (ACCT_NO, ACCT_NM, ACCT_STS_CD) 
            VALUES (:1, :2, :3)
        """, [account_no, account_name, '01'])
        
        return account_no
    
    def _generate_random_amount(self, min_amount: int, max_amount: int, step: int) -> int:
        return random.randrange(min_amount, max_amount + 1, step)
    
    async def _generate_invalid_account(self) -> str:
        account_no = ''.join(random.choices(string.digits, k=10))
        account_name = ''.join(random.choices("가나다라마바사아자차카타파하", k=3))
        
        # 비정상 상태의 계좌 데이터 생성
        await self.db.execute("""
            INSERT INTO COM_ACCT_NO_M (ACCT_NO, ACCT_NM, ACCT_STS_CD)
            VALUES (:1, :2, :3)
        """, [account_no, account_name, '04'])
        
        return account_no
    
    async def _save_value(self, template: str, context: Dict[str, Any]) -> str:
        value = await self._generate_random_account(10)
        key = template.replace("save_as", "").strip()
        self.saved_values[key] = value
        return value