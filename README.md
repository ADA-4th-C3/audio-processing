## Audio Processing
Guita 프로젝트에 사용되는 음원 파일 후처리 스크립트
- 무음 제거
- 소리 증폭
- note 폴더 내부는 2초 이내로 자르고 fade out 적용

### Setup
```
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

### Activate Virtual Env
```
source .venv/bin/activate
```

### Run
```
python main.py
```