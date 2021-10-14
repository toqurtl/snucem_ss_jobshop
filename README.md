# snucem_ss_jobshop
* data: 샘플 데이터
* practice: ortool 예제
* sample: ss_js 사용 예시
* ss_js: 패키지


# Usage
## 분석파일 생성
### Excel to json
```python
from ss_js import io

file_path = "data/input.xlsx"
generated_path = "data/generated.json"

io.generate_json(file_path, generated_path)

```
### json파일 형태
```json
{	
	"last_tasktype_id": "A3", 
	"labor_type": [
		{
			"labor_id": "l1",
			"labor_name": "welder",
			"number": 7
		},
		{
			"labor_id": "l2",
			"labor_name": "plumber",
			"number": 7
		},
		{
			"labor_id": "l99",
			"labor_name": "dummy",
			"number": 88
		}
	],
	"task_type": [
		{
			"task_id": "Z1",
			"workpackage_id": "Z",
			"workpackage_name": "모듈설치",
			"detail_id": 1,
			"task_name": "모듈반입",
			"is_module": true,
			"labor_set": [
				{
					"alt_id": 0,
					"required": {
						"l99": 5
					},
					"productivity": 1.0
				}
			]
		},
```

## 모델 생성
### Structure

### 변수명 규칙

## 최적화


## 결과확인
### task_list

### 시간별 task

### 시간별 labor