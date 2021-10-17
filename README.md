# snucem_ss_jobshop
* data: 샘플 데이터
* practice: ortool 예제
* sample: ss_js 사용 예시
* ss_js: 패키지


# Usage
## 분석환경
experiment 폴더 내 폴더 하나 = 분석환경
* 폴더 구조
```bash
experiment[최상위폴더]
├── env1
│   ├── input
│	│	├── input.xlsx
│   ├── output
│   └── result
├── env2
│   ├── input
│   ├── output
│   ├── result
│   
└── run.sh
``` 
* env1 실행 후


## 분석파일 생성
python app_tojson.py [folder_name] [interference]
* 예
```bash
python app_tojson.py env_1 true
```
* true를 입력할 때만 간섭 고려, 다른 값을 입력하거나 입력하지 않으면 간섭 고려 X

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
app_marketresult.py [folder_name] [monitoring cycle] [target_obj]
* 예
```bash
python app_marketresult.py env_1 1 1000
```
### 최적화

### 결과


## 결과시각화
python app_makeresult.py [folder_name] [solution_ctn]
* 예
```bash
python app_makeresult.py env_1 3
```
### 간트차트
* 분단위

* 일단위

### 시간별 labor 투입량
* 분단위

* 일단위