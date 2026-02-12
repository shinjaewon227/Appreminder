# flask_app.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# 보안을 위해 특정 도메인만 허용하거나 모든 도메인 허용 (*). 
# 실제 배포 시에는 프론트엔드 도메인을 넣는 것이 좋으나 개발 편의상 * 로 둡니다.
CORS(app, resources={r"/*": {"origins": "*"}})

# 간단한 인메모리 데이터베이스 (서버 재시작 시 초기화됨)
# 영구 저장을 원하시면 SQLite나 MySQL을 연동해야 합니다.
# PythonAnywhere는 파일 저장이 유지되므로 json 파일 저장 방식을 추천하지만, 
# 일단 요청하신 기능 구현을 위해 딕셔너리로 유지합니다.
PLANS = {}

@app.route('/')
def home():
    return "Study Planner API Server is Running!"

# 1. 특정 날짜 상세 데이터 가져오기
@app.route('/get-plan-detail', methods=['POST'])
def get_plan_detail():
    data = request.get_json()
    user_name = data.get('name')
    target_date = data.get('date')
    
    user_plans = PLANS.get(user_name, [])
    # 해당 날짜 데이터 찾기
    plan = next((p for p in user_plans if p["date"] == target_date), None)
    
    if plan:
        return jsonify({"success": True, "plan": plan})
    else:
        return jsonify({"success": False, "message": "데이터 없음"})

# 2. 저장하기
@app.route('/save-plan', methods=['POST'])
def save_plan():
    data = request.get_json()
    user_name = data.get('name')
    plan_data = data.get('plan')
    
    if user_name not in PLANS:
        PLANS[user_name] = []
    
    # 기존 데이터 있으면 덮어쓰기
    existing_index = next((index for (index, d) in enumerate(PLANS[user_name]) if d["date"] == plan_data["date"]), None)
    
    if existing_index is not None:
        PLANS[user_name][existing_index] = plan_data
    else:
        PLANS[user_name].append(plan_data)
        
    return jsonify({"success": True, "message": "성공적으로 저장되었습니다."})

# 3. 전체 목록 가져오기 (옵션)
@app.route('/get-plan-list', methods=['POST'])
def get_plan_list():
    data = request.get_json()
    user_name = data.get('name')
    user_plans = PLANS.get(user_name, [])
    
    summary_list = [{"date": p["date"]} for p in user_plans]
    summary_list.sort(key=lambda x: x['date'], reverse=True)
    return jsonify({"plans": summary_list})