import json

def calculate_accuracy(result_file):
    """
    计算 RAG 系统的 Top-1 和 Top-5 准确率。
    业务背景：用于排查系统是存在“语义带歪(Ranking)”还是“物理断供(Indexing)”。
    """
    total_queries = 0
    top_1_hits = 0
    top_5_hits = 0
    
    # 模拟读取打流测试后的结果文件 (格式: 包含目标 API 和 检索回来的 API 列表)
    print("开始加载 AscendC API 检索结果数据...\n")
    
    try:
        with open(result_file, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line.strip())
                ground_truth = data.get("ground_truth_api", "")
                retrieved_list = data.get("retrieved_apis", [])
                
                if not ground_truth or not retrieved_list:
                    continue
                    
                total_queries += 1
                
                # Top-1 命中逻辑 (门面指标)
                if retrieved_list[0] == ground_truth:
                    top_1_hits += 1
                    
                # Top-5 命中逻辑 (底座指标)
                if ground_truth in retrieved_list[:5]:
                    top_5_hits += 1
                    
    except FileNotFoundError:
        print(f"Warning: 评测结果文件 {result_file} 不存在，请先执行 api_evaluation_v2.py 打流。")
        return

    if total_queries == 0:
        print("未检测到有效评测数据。")
        return
        
    top_1_acc = (top_1_hits / total_queries) * 100
    top_5_acc = (top_5_hits / total_queries) * 100
    
    print("-" * 30)
    print(f"评测总数: {total_queries} 条")
    print(f"Top-1 准确率: {top_1_acc:.2f}% (精确命中)")
    print(f"Top-5 准确率: {top_5_acc:.2f}% (召回兜底)")
    print("-" * 30)
    
    # 业务归因诊断
    if top_1_acc == top_5_acc and top_1_acc < 70:
        print("🚨 架构诊断: Top-1 与 Top-5 持平且分值偏低，系统存在严重『物理断层』，建议排查索引库缺失问题。")

if __name__ == "__main__":
    # 执行评测计算
    calculate_accuracy('eval_results_mock.jsonl')
